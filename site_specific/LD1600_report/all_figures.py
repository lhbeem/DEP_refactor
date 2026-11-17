# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 08:27:24 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'../../lookup'))

import numpy as np
import matplotlib.pylab as pl
from matplotlib.lines import Line2D
import pandas as pd
import geopandas as gpd
import math 
import pyproj
from pypdf import PdfWriter
import glob
import tqdm



''' 
LD1600 Report General Figures
'''

class palette:
    blue = '#557fba'
    red = '#bf5550'
    green = '#99bb62'
    purple = '#82649f'
    orange = 'tab:orange'

class pie_color:
    nd = palette.orange
    lt20 = palette.blue
    bt20_100 = palette.red
    bt100_1k = palette.green
    gt1k = palette.purple


class avg_color:
    longSA = '#6e96fa'
    shortSA = '#a1bdfb'
    preSA = '#cddafd'
    longCA = '#94ca97'
    shortCA = '#c2e1c4'
    preCA = '#e4f0e5'


def representative_concentration(df,params=True):
    
    if params == True:
        use_params = set(df.PARAMETER)
    else:
        use_params = params
    
    out_data = pd.DataFrame(columns = df.columns)
    unique_locations = set(df.SAMPLE_POINT_SEQ)
    for loc in tqdm.tqdm(unique_locations):
        loc_data2 = df[df.SAMPLE_POINT_SEQ == loc] 
        for param in use_params:
            loc_data = loc_data2[loc_data2.PARAMETER == param]
            if len(loc_data) == 0:
                continue
            elif len(loc_data) == 1:
                out_data.loc[len(out_data)] = loc_data.iloc[0]
            elif len(loc_data) > 1:
                out_data.loc[len(out_data)] = loc_data.loc[loc_data.CONCENTRATION.idxmax()] 

    return out_data

# todo representative_concentration. try Building a list of dictionarys then make dataframe adding to a bif dataframe gets slow




P = pyproj.Proj('EPSG:26919')

save_folder = base_folder +'/all_figures'

#%%
gw_data_path = r"C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\data\LD1600_report\DRAFT_LD1600Dataset_Cleaned_08Oct2026.xlsx"
ref_table_path = r"C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\data\LD1600_report\Reference Table.xlsx"


gw = pd.read_excel(gw_data_path,sheet_name='Sheet 1')

# load maine outline
outline = gpd.read_file(r"C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\data\geo_files\lo_res_maine.gpkg")


# extract specific parameters
gw_sum6 = gw[gw.PARAMETER == 'SUM OF 6 PFAS']
gw_PFOS = gw[gw.PARAMETER == 'PFOS']
gw_PFOA = gw[gw.PARAMETER == 'PFOA']
gw_haz  = gw[gw.PARAMETER == 'HAZARD_INDEX']

unique_locations = set(gw.SAMPLE_POINT_SEQ)
unique_sources = list(set(gw.LICENSEE))
# remove nan
unique_sources = [x for x in unique_sources if not (isinstance(x, float) and math.isnan(x))]

unique_sites = set(gw.SITE_SEQ)



#%% pie chart Fig 2 in 2025 report

# do we count resamples as indepentant
# if not, which value do we choose for the location (highest?, lowest?, mean?)


pie_data = representative_concentration(gw[gw.PARAMETER == 'SUM OF 6 PFAS'])
#%%
size = [len(pie_data[pie_data.CONCENTRATION >= 1000]),
        len(pie_data[(pie_data.CONCENTRATION < 1000) & (pie_data.CONCENTRATION >= 100)]),
        len(pie_data[(pie_data.CONCENTRATION < 100) & (pie_data.CONCENTRATION >=20)]),
        len(pie_data[pie_data.CONCENTRATION < 20]),
        ]

percent = np.round(np.array(size) / len(pie_data) * 100).astype(int)
labels = []
for per in percent:
    labels.append('{}%'.format(per))



colors = [pie_color.gt1k,pie_color.bt100_1k,pie_color.bt20_100,pie_color.lt20]


fig = pl.figure(1)
fig.clf()
ax = fig.add_subplot(111)
ax.pie(size,labels=labels,colors=colors, startangle = 90,wedgeprops = {'edgecolor':'w'})


leg = [Line2D([0], [0], color=pie_color.lt20, lw=4),
       Line2D([0], [0], color=pie_color.bt20_100, lw=4),
       Line2D([0], [0], color=pie_color.bt100_1k, lw=4),
       Line2D([0], [0], color=pie_color.gt1k, lw=4)]

leg_text = ['Wells less than 20 ppt',
            'Wells between 20 and 100 ppt',
            'Wells between 100 and 1000 ppt',
            'Wells greater than 1000 ppt']

ax.legend(leg, leg_text,bbox_to_anchor=(1.05, 0.5), loc='center left',frameon=False)
ax.text(.72,.72,'n = {}'.format(len(pie_data)))

fig.savefig(save_folder+'/01_pie_chart.pdf',bbox_inches='tight')


#%% Fig 2 alternative , include ND.

size = [len(pie_data[pie_data.CONCENTRATION >= 1000]),
        len(pie_data[(pie_data.CONCENTRATION < 1000) & (pie_data.CONCENTRATION >= 100)]),
        len(pie_data[(pie_data.CONCENTRATION < 100) & (pie_data.CONCENTRATION >=20)]),
        len(pie_data[(pie_data.CONCENTRATION < 20) & (pie_data.CONCENTRATION > 0)]),
        len(pie_data[pie_data.CONCENTRATION == 0])
            ]

percent = np.round(np.array(size) / len(pie_data) * 100).astype(int)
labels = []
for per in percent:
    labels.append('{}%'.format(per))



colors = [pie_color.gt1k,pie_color.bt100_1k,pie_color.bt20_100,pie_color.lt20,pie_color.nd]


fig = pl.figure(1)
fig.clf()
ax = fig.add_subplot(111)
ax.pie(size,labels=labels,colors=colors, startangle = 90,wedgeprops = {'edgecolor':'w'})


leg = [Line2D([0], [0], color=pie_color.nd, lw=4),
       Line2D([0], [0], color=pie_color.lt20, lw=4),
       Line2D([0], [0], color=pie_color.bt20_100, lw=4),
       Line2D([0], [0], color=pie_color.bt100_1k, lw=4),
       Line2D([0], [0], color=pie_color.gt1k, lw=4)]

leg_text = ['Wells with Non-Detect',
            'Wells between Non-Detect and 20 ppt',
            'Wells between 20 and 100 ppt',
            'Wells between 100 and 1000 ppt',
            'Wells greater than 1000 ppt']

ax.legend(leg, leg_text,bbox_to_anchor=(1.05, 0.5), loc='center left',frameon=False)
ax.text(.72,.72,'n = {}'.format(len(pie_data)))

fig.savefig(save_folder+'/01_pie_chart_b.pdf',bbox_inches='tight')

#%% figure 2 alternative probability distribution of concentration 

hist_data = pie_data[pie_data.CONCENTRATION < 20000].CONCENTRATION
count, edge = np.histogram(hist_data,bins=20000)

hist_cum = np.cumsum(count) / len(hist_data)

fig = pl.figure(1)
fig.clf() 
ax = fig.add_subplot(111)
ax.plot(hist_cum,'k')
ax.set_xscale('log')    
ax.set_xlim([1,20000])
ax.set_xlabel('Sum6 Concentration (ppt)')
ax.set_ylabel('Cumulative Fraction')

fig.savefig(save_folder+'/01_concentration_cdf_log.pdf')


fig = pl.figure(2)
fig.clf() 
ax = fig.add_subplot(111)
ax.plot(hist_cum,'k')    
ax.set_xlim([1,20000])
ax.set_xlabel('Sum6 Concentration (ppt)')
ax.set_ylabel('Cumulative Fraction')

fig.savefig(save_folder+'/01_concentration_cdf.pdf')




#%% Figure 6: Stackage bar average groundwater


params = ['TOTAL PFCA Precursors','TOTAL Short-Chain PFCAs','TOTAL Long-Chain PFCAs',
          'TOTAL PFSA Precursors','TOTAL Short-Chain PFSAs','TOTAL Long-Chain PFSAs',]

sludge = representative_concentration(gw[gw.SITE_TYPE == 'SLUDGE'], params)
landfill = representative_concentration(gw[gw.SITE_TYPE == 'LANDFILL'], params)
#remove monitoring wells 
landfill =landfill[landfill.SAMPLE_POINT_TYPE != 'MONITORING WELL']

septage = representative_concentration(gw[gw.SITE_TYPE == 'SEPTAGE'], params)
#%%
n_sludge = len(set(sludge.SAMPLE_POINT_SEQ))
n_landfill = len(set(landfill.SAMPLE_POINT_SEQ))
n_septage = len(set(septage.SAMPLE_POINT_SEQ))


bar_x = ['Sludge\nn = {}'.format(n_sludge), 'Landfill\nn = {}'.format(n_landfill),
         'Septage\nn = {}'.format(n_septage)]

bar_data = []

for param in params:
    bar_data.append( [ sludge[sludge.PARAMETER == param].CONCENTRATION.mean(),
                       landfill[landfill.PARAMETER == param].CONCENTRATION.mean(),
                       septage[septage.PARAMETER == param].CONCENTRATION.mean(),
                       ])

bar_data = np.array(bar_data)

fig = pl.figure(1)
fig.clf()
pl.bar(bar_x,bar_data[0],color = avg_color.preCA,label= 'Precursor PFCA')
pl.bar(bar_x,bar_data[1],bottom = bar_data[0],color = avg_color.shortCA,label= 'Short-Chain PFCA')
pl.bar(bar_x,bar_data[2],bottom = np.sum(bar_data[:2,:],axis=0),color = avg_color.longCA,label= 'Long-Chain PFCA')
pl.bar(bar_x,bar_data[3],bottom = np.sum(bar_data[:3,:],axis=0),color = avg_color.preSA,label= 'Precursor PFSA')
pl.bar(bar_x,bar_data[4],bottom = np.sum(bar_data[:4,:],axis=0),color = avg_color.shortSA,label= 'Short-Chain PFSA')
pl.bar(bar_x,bar_data[5],bottom = np.sum(bar_data[:5,:],axis=0),color = avg_color.longSA,label= 'Long-Chain PFSA')

pl.legend(reverse=True)



fig.savefig(save_folder+'/02_concentration_bar.pdf',bbox_inches='tight')

#%% fig 6 alternative pdf



filename = ['sludge', 'landfill','septage']

for j,data in enumerate([sludge,landfill,septage]):
    pl.close(fig)
    fig = pl.figure(1,figsize=[20,8.5])
    fig.clf() 
    for i,param in enumerate(params):
        hist_data = data[data.PARAMETER == param].CONCENTRATION
        bins = np.logspace(-1, 5.5)
        bins = np.insert(bins,0,0)
        
        count, edge = np.histogram(hist_data,bins=bins)
        
        fraction = count / len(hist_data)
        cuml = np.cumsum(count)/ len(hist_data)
        
        ax = fig.add_subplot(2,3,i+1)
        ax.plot(edge[:-1],fraction,'k', label = 'concentration')
        ax.set_xscale('log')   
        ax2 = ax.twinx()
        ax2.plot(edge[:-1],cuml, label='cumulative fraction') 
        
        ylim1 = max(fraction[1:])+.01 
        ylim = min(cuml)
        
        ax2.vlines(hist_data.mean(),ylim,1,color='tab:orange',label='mean')
        ax2.vlines(hist_data.median(),ylim,1,'r',label='median')
        
        if i == 0:
            handles1, labels1 = ax.get_legend_handles_labels()
            handles2, labels2 = ax2.get_legend_handles_labels()
            ax2.legend(handles1 + handles2, labels1 + labels2, loc="upper left")
            
        ax.set_title(param)
        
        if hist_data.median() == 0:
            ax.text(1000,.01,'median = 0')
        
        ax.set_xlabel('Concentration (ppt)')
        ax.set_ylabel('Fraction')
        ax2.set_ylabel('Cumulative Fraction')
        ax.set_ylim([0,ylim1])
    
    fig.savefig(save_folder+'/02_concentration_{}_cdf.pdf'.format(filename[j]),bbox_inches='tight')


#%% 

color = ['tab:blue','tab:orange','tab:green']
pl.close(fig)
fig = pl.figure(1,figsize=[20,8.5])
fig.clf() 


for i,param in enumerate(params):
    ax = fig.add_subplot(2,3,i+1)
    ax.set_xscale('log')
    # ax2 = ax.twinx()
    medi = []
    for j,data in enumerate([sludge,landfill,septage]):

    
        hist_data = data[data.PARAMETER == param].CONCENTRATION
        bins = np.logspace(-1, 5.5)
        bins = np.insert(bins,0,0)
        
        count, edge = np.histogram(hist_data,bins=bins)
        
        fraction = np.array( count / len(hist_data) )
        cuml = np.cumsum(count)/ len(hist_data)
        
        ax.plot(edge[:-1],fraction / fraction[1:].max(),color=color[j], label = 'concentration')
           
        
        ax.plot(edge[:-1],cuml,color=color[j], label='cumulative fraction') 
        
        # ylim1 = max(fraction[1:])+.01 
        # ylim = min(cuml)
        
        ax.vlines(hist_data.mean(),0,1,color=color[j],label='mean')
        # ax2.vlines(hist_data.median(),.4,1,color=color[j],label='median')
        
        medi.append(round(hist_data.median(),3))
        if (i == 0) and (j == 0):
            leg = [Line2D([0], [0], color=color[0], lw=4),
                   Line2D([0], [0], color=color[1], lw=4),
                   Line2D([0], [0], color=color[2], lw=4),]

            leg_text = ['Sludge',
                        'Landfill',
                        'Septage',]

            ax.legend(leg, leg_text,bbox_to_anchor=(.6, 0.6), loc='center left',frameon=False)
            
    ax.set_title(param)
    ax.text(100,.8,'medians:{},{},{}'.format(medi[0],medi[1],medi[2]))
# if hist_data.median() == 0:
#     ax.text(1000,.01,'median = 0')


    ax.set_xlabel('Concentration (ppt)')
    ax.set_ylabel('Fraction / Cumulative Fraction')
    ax.set_ylim([0,1.05])

fig.savefig(save_folder+'/02_concentration_all_cdf.pdf',bbox_inches='tight')

#%% figure 8 from 2025 report distance 
# load distance
dist = pd.read_excel(ref_table_path, sheet_name='DISTANCE')
dist = dist[['SAMPLE_POINT_NUMBER','NEAR_DIST']]

scatter = []
for row in pie_data.iterrows():
    row = row[1]
    d = dist[dist.SAMPLE_POINT_NUMBER == row.SAMPLE_POINT_SEQ].NEAR_DIST.tolist()
    if len(d) == 1:
        scatter.append([ d[0], row.CONCENTRATION ])

#%%
scatter = np.array(scatter)

I = scatter[:,1] >= 20

fig = pl.figure(1)
fig.clf()
ax = fig.add_subplot(111)
ax.plot(scatter[I,0],scatter[I,1],'.',color=avg_color.longSA,label='Sum of 6 PFAS > 20 ppt')
ax.set_xlim([0,5000])
ax.set_xlabel('Distance (feet)')
ax.set_ylabel('Sum of 6 Concentration (ppt)')

ax.legend()
fig.savefig(save_folder+'/03_distance.pdf',bbox_inches='tight')

#%% figure 8 alternative (there is no relationship)

ax.set_ylim([0,300])
ax.legend()
fig.savefig(save_folder+'/03_distance_b.pdf',bbox_inches='tight')



#%% figure 8 alternative cdf by distribution bin
bins = np.arange(0,5000,100)
I = scatter[:,1] == 0 
I2 = (scatter[:,1] < 20) & (scatter[:,1] > 0)
I3 = scatter[:,1] >= 20
count, edge = np.histogram(scatter[I,0],bins=bins)
cuml = np.cumsum(count)/ sum(I)
count2, edge2 = np.histogram(scatter[I2,0],bins=bins)
cuml2 = np.cumsum(count2)/ sum(I2)
count3, edge3 = np.histogram(scatter[I3,0],bins=bins)
cuml3 = np.cumsum(count3)/ sum(I3)
count4, edge4 = np.histogram(scatter[:,0],bins=bins)
cuml4 = np.cumsum(count4)/ len(scatter[:,0])


fig = pl.figure(1)
fig.clf()
ax = fig.add_subplot(111)
ax.plot(edge[1:],count / max(count),label = 'SUM of 6 PFAS == 0')
ax.plot(edge2[1:],count2/ max(count2),label = 'SUM of 6 PFAS < 20 and >0')
ax.plot(edge3[1:],count3/ max(count3),label = 'SUM of 6 PFAS > 20')
ax.plot(edge4[1:],count4/ max(count4),label = 'All Samples')   

ax.legend(loc='right')
ax.set_prop_cycle(None)
ax.plot(edge[1:],cuml)
ax.plot(edge2[1:],cuml2)
ax.plot(edge3[1:],cuml3)
ax.plot(edge4[1:],cuml4)
ax.set_xlabel('Distance (feet)')
ax.set_ylabel('Normalized Count / Cumulative Fraction')

fig.savefig(save_folder+'/03_distance_c.pdf',bbox_inches='tight')


#%% figure 8 alternative d , probability by distance bin
bins = np.arange(0,5001,200)

nd = []
lt20 = []
gt20 = []

for ii in range(len(bins)-1):
    I = (scatter[:,0] > bins[ii]) & (scatter[:,0] < bins[ii+1])
    
    nd.append( sum(scatter[I,1] == 0) / sum(I) )
    lt20.append( sum((scatter[I,1] > 0) & (scatter[I,1] < 20) ) / sum(I) )
    gt20.append( sum(scatter[I,1] >= 20) / sum(I))




fig = pl.figure(1)
fig.clf()
ax = fig.add_subplot(111)

ax.fill_between(bins[1:], nd)
ax.fill_between(bins[1:], np.array(lt20) + np.array(nd), y2=nd)
ax.fill_between(bins[1:], 1, y2=np.array(lt20) + np.array(nd))

ax.text(200,.15,'Non Detect',color='w')
ax.text(200,.6,'Non-Zero and Less Than 20 ppt',color='w')
ax.text(200,.95,'Greater than 20 ppt',color='w')
ax.set_ylabel('Fraction of Distance Bin')
ax.set_xlabel('Distance (feet)')

fig.savefig(save_folder+'/03_distance_d.pdf',bbox_inches='tight')

#%% figure 9 from 2025 avg concetrations by tier
params = ['TOTAL PFCA Precursors','TOTAL Short-Chain PFCAs','TOTAL Long-Chain PFCAs',
          'TOTAL PFSA Precursors','TOTAL Short-Chain PFSAs','TOTAL Long-Chain PFSAs',]

T1 = representative_concentration(gw[gw.SITE_TIER == 'TIER I'], params)
T2 = representative_concentration(gw[gw.SITE_TIER == 'TIER II'], params)
T3 = representative_concentration(gw[gw.SITE_TIER == 'TIER III'], params)
T4 = representative_concentration(gw[gw.SITE_TIER == 'TIER IV'], params)
TA = representative_concentration(gw[gw.SITE_TIER.isin(['CLASS A', 'TIER NA'])], params)

n_T1 = len(set(T1.SAMPLE_POINT_SEQ))
n_T2 = len(set(T2.SAMPLE_POINT_SEQ))
n_T3 = len(set(T3.SAMPLE_POINT_SEQ))
n_T4 = len(set(T4.SAMPLE_POINT_SEQ))
n_TA = len(set(TA.SAMPLE_POINT_SEQ))
                                     
bar_x = ['Tier I\nn = {}'.format(n_T1), 'Tier II\nn = {}'.format(n_T2),
         'Tier III\nn = {}'.format(n_T3), 'Tier IV\nn = {}'.format(n_T4),
         'Tier NA\nn = {}'.format(n_TA),]

bar_data = []

for param in params:
    bar_data.append( [ T1[T1.PARAMETER == param].CONCENTRATION.mean(),
                       T2[T2.PARAMETER == param].CONCENTRATION.mean(),
                       T3[T3.PARAMETER == param].CONCENTRATION.mean(),
                       T4[T4.PARAMETER == param].CONCENTRATION.mean(),
                       TA[TA.PARAMETER == param].CONCENTRATION.mean(),
                       ])

bar_data = np.array(bar_data)

fig = pl.figure(1)
fig.clf()
pl.bar(bar_x,bar_data[0],color = avg_color.preCA,label= 'Precursor PFCA')
pl.bar(bar_x,bar_data[1],bottom = bar_data[0],color = avg_color.shortCA,label= 'Short-Chain PFCA')
pl.bar(bar_x,bar_data[2],bottom = np.sum(bar_data[:2,:],axis=0),color = avg_color.longCA,label= 'Long-Chain PFCA')
pl.bar(bar_x,bar_data[3],bottom = np.sum(bar_data[:3,:],axis=0),color = avg_color.preSA,label= 'Precursor PFSA')
pl.bar(bar_x,bar_data[4],bottom = np.sum(bar_data[:4,:],axis=0),color = avg_color.shortSA,label= 'Short-Chain PFSA')
pl.bar(bar_x,bar_data[5],bottom = np.sum(bar_data[:5,:],axis=0),color = avg_color.longSA,label= 'Long-Chain PFSA')

pl.legend(reverse=True)



fig.savefig(save_folder+'/04_concentration_by_tier.pdf',bbox_inches='tight')

#%% figure 9 alternative cdf 

bins = np.arange(0,1000,1)
bins = np.append( bins , np.arange(1000,30000,100) )

# bins = np.logspace(0, 5)
count1, edge = np.histogram(pie_data[pie_data.SITE_TIER == 'TIER I'].CONCENTRATION,bins=bins)
count2, _ = np.histogram(pie_data[pie_data.SITE_TIER == 'TIER II'].CONCENTRATION,bins=bins)
count3, _ = np.histogram(pie_data[pie_data.SITE_TIER == 'TIER III'].CONCENTRATION,bins=bins)
count4, _ = np.histogram(pie_data[pie_data.SITE_TIER == 'TIER IV'].CONCENTRATION,bins=bins)
countA, _ = np.histogram(pie_data[pie_data.SITE_TIER.isin(['CLASS A', 'TIER NA'])].CONCENTRATION,bins=bins)

cuml1 = np.cumsum(count1) / sum(count1)
cuml2 = np.cumsum(count2) / sum(count2)
cuml3 = np.cumsum(count3) / sum(count3)
cuml4 = np.cumsum(count4) / sum(count4)
cumlA = np.cumsum(countA) / sum(countA)

fig = pl.figure(1)
fig.clf()
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.plot(edge[1:],cuml1,label='Tier I')
ax.plot(edge[1:],cuml2,label='Tier II')
ax.plot(edge[1:],cuml3,label='Tier III')
ax.plot(edge[1:],cuml4,label='Tier IV')
ax.plot(edge[1:],cumlA,label='Class A, Unconfirmed')

ax.legend()
ax.set_xlabel('Concentration (ppt)')
ax.set_ylabbel('Cumulative Fraction')
fig.savefig(save_folder+'/04_concentration_by_tier_b.pdf',bbox_inches='tight')


#%% MCL for each location determine if there is ever sum6 < 20 and other compound greater than MCL

MCL_data = pd.DataFrame(columns = gw.columns)
for loc in unique_locations: 
    mcl = gw[gw.SAMPLE_POINT_SEQ == loc]
    for compound,thres in zip(['PFOS','PFOA','HAZARD_INDEX'], [4,4,1]):
        if np.any(mcl[mcl.PARAMETER == 'SUM OF 6 PFAS'].CONCENTRATION < 20) and np.any(mcl[mcl.PARAMETER == compound].CONCENTRATION > 4):
            MCL_data.loc[len(MCL_data)] = mcl.loc[mcl[mcl.PARAMETER == compound].CONCENTRATION.idxmax()]



# sort haz by locations
haz_data = pd.DataFrame(columns = gw.columns)
for loc in unique_locations:
    loc_data = gw_haz[gw_haz.SAMPLE_POINT_SEQ == loc]
    if len(loc_data) == 0:
        continue
    elif len(loc_data) == 1:
        haz_data.loc[len(haz_data)] = loc_data.iloc[0]
    elif len(loc_data) > 1:
        haz_data.loc[len(haz_data)] = loc_data.loc[loc_data.CONCENTRATION.idxmax()]
    
# print basic data

table = pd.DataFrame(columns = ['Detail', 'Magnitude'])
table.loc[len(table)] = ['Number of sites', len(unique_sites) ]
table.loc[len(table)] = ['Number of locations', len(unique_locations) ]                    
table.loc[len(table)] = ['Number of sum6 ND', len(pie_data[pie_data.CONCENTRATION == 0]) ]
table.loc[len(table)] = ['Number of sum6 > 20', len(pie_data[pie_data.CONCENTRATION > 20 ]) ]              
table.loc[len(table)] = ['Number of locations without position', pie_data.SAMPLE_POINT_LONGITUDE.isna().sum() ] 
table.loc[len(table)] = ['Number of generators', len(unique_sources) ] 
table.loc[len(table)] = ['Number of locations without a generator', pie_data.LICENSEE.isna().sum() ] 

table.loc[len(table)] = ['', '' ] 
table.loc[len(table)] = ['MCL', '' ] 
table.loc[len(table)] = ['PFOA > 4 ppt and sum6 < 20 ppt', len(MCL_data[MCL_data.PARAMETER == 'PFOA'])  ]
table.loc[len(table)] = ['PFOS > 4 ppt and sum6 < 20 ppt', len(MCL_data[MCL_data.PARAMETER == 'PFOS'])  ]
pp = MCL_data[(MCL_data.PARAMETER == 'PFOS') |( MCL_data.PARAMETER == 'PFOA')]
table.loc[len(table)] = ['PFOS and/or PFOS > 4 ppt and sum6 < 20 ppt', len(set(pp.SAMPLE_POINT_SEQ))  ]
table.loc[len(table)] = ['Hazard Index > 1 and sum6 < 20 ppt' , len(MCL_data[MCL_data.PARAMETER == 'HAZARD_INDEX'])  ]
table.loc[len(table)] = ['Hazard Index > 1' , len(haz_data[haz_data.CONCENTRATION > 1])  ]



fig = pl.figure(1)
fig.clf()
ax = fig.add_subplot(111)
ax.axis('off')
tbl = ax.table(cellText=table.values, colLabels=None, loc='center',cellLoc='center')

fig.savefig(save_folder+'/00_basic_stats.pdf',bbox_inches='tight')


#%% source stats 
src_table = pd.DataFrame(columns = ['Generator','Number of Locations','Number of > 20','Number of Sites'])
for src in unique_sources:
    num = pie_data[pie_data.LICENSEE == src]
    gt = pie_data[(pie_data.LICENSEE == src) & (pie_data.CONCENTRATION > 20)]
    site = set(num.SITE_SEQ)
    src_table.loc[len(src_table)] = [src,len(num), len(gt), len(site)]

num = pie_data[pie_data.LICENSEE.isna()]
gt = pie_data[ (pie_data.LICENSEE.isna()) & (pie_data.CONCENTRATION > 20) ] 
site = set(num.SITE_SEQ)
src_table.loc[len(src_table)] = ['Not Specified',len(num), len(gt), len(site)]


src_table.sort_values(by='Number of Locations',inplace= True,ascending=False)

fig = pl.figure(1)
fig.clf()
ax = fig.add_subplot(111)
ax.axis('off')
tbl = ax.table(cellText=src_table.values, colLabels=src_table.columns, loc='center',cellLoc='center')

fig.savefig(save_folder+'/00_source_table.pdf',bbox_inches='tight')

#%% source geographic distribution 

# if there are more than 10 samples

for i,src in enumerate(src_table.iterrows()):
    num = pie_data[pie_data.LICENSEE == src[1].Generator]
    if len(num) < 10:
        continue
    x,y = P(num.SAMPLE_POINT_LONGITUDE,num.SAMPLE_POINT_LATITUDE)
    
    fig = pl.figure(1)
    fig.clf()
    ax = fig.add_subplot(111)
    
    ax.plot( outline.geometry.get_coordinates().x/1000,outline.geometry.get_coordinates().y/1000,'k')
        
        
    ax.plot(x/1000,y/1000,'.', color=palette.orange,ms=2)
    ax.set_title(src[1].Generator)

    ax.set_xlabel('Easting (km)')
    ax.set_ylabel('Northing (km)')
    ax.axis('equal')
    
    src_name = src[1].Generator
    if '/' in src_name:
        src_name = src_name.replace('/','&')
    
    fig.savefig(save_folder+'/source{:02}_{}.pdf'.format(i,src_name),bbox_inches='tight')


#%% individual compounds %detected %sources

parameters = set(gw.PARAMETER)

name = []
detect = []
source = []
for parameter in parameters:
    if parameter.startswith('AVERAGE') or parameter.startswith('HAZARD') or parameter.startswith('TOTAL') or parameter.startswith('SUM'):
        continue
    
    data = gw[gw.PARAMETER == parameter]
    data = data[data.CONCENTRATION > 0]
    det = len(set(data.SAMPLE_POINT_SEQ))
    src  = len(set(data.LICENSEE)) 
    
    name.append(parameter)
    detect.append(det / len(unique_locations) * 100 )
    source.append( src )


index = np.argsort(detect)[::-1]
name = np.array(name)[index]
detect = np.array(detect)[index]
source = np.array(source)[index]

fig = pl.figure(1)
fig.clf()
ax = fig.add_subplot(111)
# ax2 = ax.twinx() 
x = np.arange(len(detect))
ax.bar(x-0.3 / 2, detect, width = .3,label='Detection')
ax.bar(x+0.3 / 2, source,width = .3, label='Source',color=palette.orange)



ax.legend()
ax.set_ylabel('Percent Detected\nNumber of Sources')
ax.set_xticks(x,labels=name,rotation=90)
fig.savefig(save_folder+'/00_occurance_percent.pdf',bbox_inches='tight')
#%% 
merger = PdfWriter()
pdfs = glob.glob(save_folder+'/*.pdf')
mergered_file = save_folder+"/all_figures.pdf"
for pdf in pdfs:
    merger.append(pdf)

merger.write(mergered_file)
merger.close()

for pdf in pdfs:
    os.remove(pdf)

