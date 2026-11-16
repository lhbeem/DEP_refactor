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


P = pyproj.Proj('EPSG:26919')

save_folder = base_folder +'/all_figures'

#%%
gw_data_path = r"C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\data\LD1600_report\DRAFT_LD1600Dataset_Cleaned_08Oct2026.xlsx"

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

pie_data = pd.DataFrame(columns = gw.columns)

# for each unique location determine if there is data. 
# if data is present take the highest concentration observed
for loc in unique_locations:
    loc_data = gw_sum6[gw_sum6.SAMPLE_POINT_SEQ == loc]
    if len(loc_data) == 0:
        continue
    elif len(loc_data) == 1:
        pie_data.loc[len(pie_data)] = loc_data.iloc[0]
    elif len(loc_data) > 1:
        pie_data.loc[len(pie_data)] = loc_data.loc[loc_data.CONCENTRATION.idxmax()]

# number of locations that fall into concentration bins
# ordered from highest to lowest concentation
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


#%% bar average by source type
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
#%% fig 6 alternative pdf
fig = pl.figure(1)
fig.clf() 

 
for i,param in enumerate(params):
    hist_data = sludge[sludge.PARAMETER == param].CONCENTRATION
    bins = np.logspace(-1, 5.5)
    bins = np.insert(bins,0,0)
    
    count, edge = np.histogram(hist_data,bins=bins)
    
    fraction = count / len(hist_data)
    cuml = np.cumsum(count)/ len(hist_data)
    
    ax = fig.add_subplot(2,3,i+1)
    ax.plot(edge[:-1],fraction,'k')
    ax.set_xscale('log')   
    ax2 = ax.twinx()
    ax2.plot(edge[:-1],cuml) 
    
    ylim = max(fraction[1:])+.01
    
    ax.vlines(hist_data.mean(),0,ylim)
    ax.vlines(hist_data.median(),0,ylim,'r')
    # ax.set_xlim([1,20000])
    
    ax.set_title(param)
    
    if hist_data.median() == 0:
        ax.text(1000,.01,'median = 0')
    
    ax.set_xlabel('Sum6 Concentration (ppt)')
    ax.set_ylabel('Fraction')
    ax2.set_ylabel('Cumulative Fraction')
    ax.set_ylim([0,ylim])
    # fig.savefig(save_folder+'/long_pfsa_pdf.pdf')





#%% MCL for each location determine if there is ever sum6 < 20 and other compound greater than MCL

MCL_data = pd.DataFrame(columns = gw.columns)
for loc in unique_locations: 
    mcl = gw[gw.SAMPLE_POINT_SEQ == loc]
    for compound,thres in zip(['PFOS','PFOA','HAZARD_INDEX'], [4,4,1]):
        if np.any(mcl[mcl.PARAMETER == 'SUM OF 6 PFAS'].CONCENTRATION < 20) and np.any(mcl[mcl.PARAMETER == compound].CONCENTRATION > 4):
            MCL_data.loc[len(MCL_data)] = mcl.loc[mcl[mcl.PARAMETER == compound].CONCENTRATION.idxmax()]



#%% sort haz by locations
haz_data = pd.DataFrame(columns = gw.columns)
for loc in unique_locations:
    loc_data = gw_haz[gw_haz.SAMPLE_POINT_SEQ == loc]
    if len(loc_data) == 0:
        continue
    elif len(loc_data) == 1:
        haz_data.loc[len(haz_data)] = loc_data.iloc[0]
    elif len(loc_data) > 1:
        haz_data.loc[len(haz_data)] = loc_data.loc[loc_data.CONCENTRATION.idxmax()]
    
#%% print basic data

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



#%%


#%% probability distribution of concentration 

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
ax.set_ylabel('Cumlative Fraction')

fig.savefig(save_folder+'/02_concentration_cdf1.pdf')


fig = pl.figure(2)
fig.clf() 
ax = fig.add_subplot(111)
ax.plot(hist_cum,'k')    
ax.set_xlim([1,20000])
ax.set_xlabel('Sum6 Concentration (ppt)')
ax.set_ylabel('Cumlative Fraction')

fig.savefig(save_folder+'/03_concentration_cdf2.pdf')


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

fig.savefig(save_folder+'/04_source_table.pdf',bbox_inches='tight')

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
fig.savefig(save_folder+'/05_occurance_percent.pdf',bbox_inches='tight')
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

