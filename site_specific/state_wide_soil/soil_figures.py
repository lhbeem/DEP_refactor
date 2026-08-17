# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 16:47:09 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'../../lookup'))
sys.path.append(os.path.join(base_folder,'../../pfas_utils'))

import paths
from pfas_map import layer_compounds as compounds
import numpy as np
import geopandas as gpd
import pandas as pd
import pylab as pl
import pyproj
import rasterio

soil = gpd.read_file(paths.soil_polygons)

PFOS = []
for i in range(len(soil)):
    data = soil.iloc[i].PFOS
    if data is None:
        continue
    data = data.split(' ')[0]
    if data == 'ND':
        data = 0
    PFOS.append(float(data))


fig1 = pl.figure(1)
fig1.clf()

ax1 = fig1.add_subplot(311)
hist = ax1.hist(PFOS,np.arange(0,100))

pl.ylabel('count')
pl.text(80,150,'n={} of {}'.format(int(sum(hist[0])),len(PFOS)))



ax2 = fig1.add_subplot(312)
hist = ax2.hist(PFOS,np.arange(0,20,.5))

pl.ylabel('count')
pl.text(12,100,'n={} of {}\n{}% < 0.5 ng/g'.format(int(sum(hist[0])),len(PFOS),np.round(hist[0][0]/len(PFOS)*100,decimals=1)))


ax3 = fig1.add_subplot(313)
hist = ax3.hist(PFOS,np.arange(0,1.01,.05))
pl.xlabel('PFOS concentration (ng/g)')
pl.ylabel('count')
pl.text(0.6,30,'n={} of {}'.format(int(sum(hist[0])),len(PFOS)))


fig1.savefig(base_folder+'/pfos_soil_historgram.pdf')

#%% PFOA 

PFOA = []
for i in range(len(soil)):
    data = soil.iloc[i].PFOA
    if data is None:
        continue
    data = data.split(' ')[0]
    if data == 'ND':
        data = 0
    PFOA.append(float(data))


fig2 = pl.figure(2)
fig2.clf()

ax1 = fig2.add_subplot(311)
hist = ax1.hist(PFOA,np.arange(0,63))
pl.ylabel('count')
pl.text(40,150,'n={} of {}'.format(int(sum(hist[0])),len(PFOA)))



ax2 = fig2.add_subplot(312)
hist = ax2.hist(PFOA,np.arange(0,20,.4))
pl.ylabel('count')
pl.text(12,100,'n={} of {}\n{}% < 0.4 mg/g'.format(int(sum(hist[0])),len(PFOA),np.round(hist[0][0]/len(PFOA)*100,decimals=1)))


ax3 = fig2.add_subplot(313)
hist = ax3.hist(PFOA,np.arange(0,1.01,.05))
pl.xlabel('PFOA concentration (ng/g)')
pl.ylabel('count')
pl.text(0.6,30,'n={} of {}'.format(int(sum(hist[0])),len(PFOA)))

fig2.savefig(base_folder+'/pfoa_soil_historgram.pdf')
#%%

pfoa_pred = rasterio.open(paths.PFOA_soil_pred)
pfoa_data = pfoa_pred.read(1)
dx,dy = pfoa_pred.res # same for both maps
ulx = pfoa_pred.transform[2]
uly = pfoa_pred.transform[5]
lrx = pfoa_pred.width * pfoa_pred.transform[0] + ulx
lry = pfoa_pred.height * pfoa_pred.transform[4] + uly
ll = [ulx,lrx,lry,uly] # same for both maps
proj = pfoa_pred.crs.to_authority() # same for both maps 

pfos_pred = rasterio.open(paths.PFOS_soil_pred)
pfos_data = pfos_pred.read(1)

P = pyproj.Transformer.from_crs( 'EPSG:26919', '{}:{}'.format(proj[0],proj[1]), always_xy=True)


pfoa = []
pfoa_pos = []
pfos = []
pfos_pos = []

pfos_thres = 0.5 # NH threshold is 0.5 for pfos
pfoa_thres = 0.4 # NH threshold is 0.4 for pfoa

def get_pred(pred_data,ll,soil,dx,dy,i):
    geo = soil.iloc[i].geometry.geoms[0].representative_point()
    x,y = P.transform(geo.x,geo.y)
    
    # index_i = int((y - ll[2]) / dy) 
    # index_j = int((x - ll[0]) / dx) 

    index_i = int( (ll[3]-y) / dy) 
    index_j = int((x - ll[0]) / dx) 
    
    return pred_data[index_i,index_j],[x,y]

for i in range(len(soil)):
    if soil.iloc[i].geometry is None:
        continue
    
    if soil.iloc[i].PFOS is not None:
        if soil.iloc[i].PFOS.startswith('ND') :
            pred,xy = get_pred(pfos_data,ll,soil,dx,dy,i)
            pfos.append( pred )
            pfos_pos.append( xy )
            
        elif float(soil.iloc[i].PFOS.split(' ')[0]) <= pfos_thres:
            pred,xy = get_pred(pfos_data,ll,soil,dx,dy,i)
            pfos.append( pred )
            pfos_pos.append( xy )
    if soil.iloc[i].PFOA is not None:
        if soil.iloc[i].PFOA.startswith('ND') :
            pred, xy = get_pred(pfoa_data,ll,soil,dx,dy,i)
            pfoa.append( pred ) 
            pfoa_pos.append( xy )
            
        elif float(soil.iloc[i].PFOA.split(' ')[0]) <= pfoa_thres:
            pred, xy = get_pred(pfoa_data,ll,soil,dx,dy,i)
            pfoa.append( pred ) 
            pfoa_pos.append( xy )
    
        

fig3 = pl.figure(3)
fig3.clf()

pl.hist(pfoa)
pl.xlabel('Model Exceedance Probability')
pl.ylabel('count')
pl.title('PFOA < {} ppb'.format(pfoa_thres))
pl.ylim([0,80])
fig3.savefig(base_folder+'/pfoa_model_comapare_hist_{}.pdf'.format(pfoa_thres))

fig4 = pl.figure(4)
fig4.clf()

pl.hist(pfos)
pl.xlabel('Model Exceedance Probability')
pl.ylabel('count')
pl.title('PFOS < {} ppb'.format(pfos_thres))
pl.ylim([0,40])
fig4.savefig(base_folder+'/pfos_model_comapare_hist_{}.pdf'.format(pfos_thres))



#%% make maps 

fig5 = pl.figure(5)
fig5.clf()

pl.imshow(pfoa_data, extent= ll,cmap='gray')

for pt in pfoa_pos:
    pl.plot(pt[0],pt[1],'.r',ms=1)
pl.colorbar()
pl.title('PFOA')
fig5.savefig(base_folder+'/pfoa_map.pdf')


fig6 = pl.figure(6)
fig6.clf()

pl.imshow(pfos_data, extent= ll,cmap='gray')

for pt in pfos_pos:
    pl.plot(pt[0],pt[1],'.r',ms=1)

pl.title('PFOS')
pl.colorbar()
fig6.savefig(base_folder+'/pfos_map.pdf')


#%% compound based positive 

all_results = np.ones(( len(soil),28 ))

compounds['HFPO-DA'] = 'HFPO_DA'

columns = list(compounds.keys())
columns.remove('Sum of 6')


for n,row in enumerate(soil.iterrows()):
    row = row[1]
    for j in range(15,44):
        if row.iloc[j] is None:
            soil.iloc[n,j] = np.nan
        elif isinstance(row.iloc[j],str):
            if row.iloc[j] in ['E537M','','E537.1','E1633_DR']:
                soil.iloc[n,j] = np.nan
            elif row.iloc[j].startswith('ND'):
                soil.iloc[n,j] = 0 
            else:
                soil.iloc[n,j] = float (row.iloc[j].split(' ')[0])
        

for n,row in enumerate(soil.iterrows()):
    row = row[1]
    for i,key in enumerate(columns):
        all_results[n,i] = row[compounds[key]]

#%%
percent = np.sum((all_results > 0),axis = 0)/ (len(soil) - np.sum(np.isnan(all_results),axis=0))

sort_i = np.argsort(percent)[::-1]
pp = percent[sort_i]
cc = np.array(columns)[sort_i]

fig6 = pl.figure(7)
fig6.add_axes([.125,.25,.8,.65])
pl.bar(cc,pp) 
pl.xticks(rotation=-90, ha='right') 
pl.ylabel('Fraction of sites with positive detection')

fig6.savefig(base_folder+'/occurance.pdf')
#%%

df = pd.DataFrame(all_results[:,sort_i],columns = np.array(columns)[sort_i])

df = df.replace(0,np.nan)

fig10 = pl.figure(10)
pl.clf()
fig10.add_axes([.125,.25,.8,.65])
custom_markers = dict(marker='.', markerfacecolor='tab:orange', markersize=2, markeredgecolor='tab:orange')
df.boxplot(rot=-90,whis=3.0,showfliers=False,flierprops=custom_markers)
pl.ylabel('Concentration (ng/g)')


fig10.savefig(base_folder+'/box.pdf')

pl.yscale('log')
fig10.savefig(base_folder+'/box_log_noOut.pdf')

df.boxplot(rot=-90,whis=3.0,showfliers=True,flierprops=custom_markers)
fig10.savefig(base_folder+'/box_log.pdf')


#%%

aa = all_results
aa[aa == 0] = np.nan

all_mean = np.nanmean(aa,axis=0)
all_med = np.nanmedian(aa,axis=0)

all_mean = all_mean[sort_i]
all_med = all_med[sort_i]


fig7 = pl.figure(6)
fig7.clf()
ax1 = fig7.add_axes([.125,.25,.75,.65])

pl.xticks(rotation=-90, ha='right')
ax2 = ax1.twinx()
ax1.bar(cc,all_mean,label='Mean')
ax1.bar(cc,all_med,label='Median')
ax2.plot(pp*100,'+',label='Occurance')
ax2.set_ylim([0,100])

handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()


ax1.legend(handles1 + handles2, labels1 + labels2, loc='upper right')
ax1.set_ylabel('Concentration (ng/g)')
ax2.set_ylabel('Percent Occurance')

fig7.savefig(base_folder+'/mean_median.pdf')

#%% Random numbers for pfas_pred
pfos_data[pfos_data == pfos_data[0,0]] = np.nan
pfoa_data[pfoa_data == pfoa_data[0,0]] = np.nan



pl.figure(100)
pl.clf()
pl.hist(pfoa_data.flatten(),bins=100,label='PFOA')
pl.hist(pfos_data.flatten(),bins=100,alpha=.5,label='PFOS')
pl.legend()


import random

nn=0
pfos_random = []
pfoa_random = []
while nn < 300:
    i = random.randint(0,598)
    j = random.randint(0,490)
    if not np.isnan(pfos_data[i,j]):
        pfos_random.append(pfos_data[i,j])
        nn += 1 
nn = 0
while nn < 300:
    i = random.randint(0,598)
    j = random.randint(0,490)
    if not np.isnan(pfoa_data[i,j]):
        pfoa_random.append(pfoa_data[i,j])
        nn += 1       

fig101 = pl.figure(101)
pl.clf()
pl.hist(pfoa_random,bins=20,label='PFOA')
pl.hist(pfos_random,bins=20,alpha=.5,label='PFOS')
pl.legend()
fig101.savefig(base_folder+'/random.pdf')
#%%
# fig8 = pl.figure(8)


# for j,i in enumerate(sort_i):
#     pl.subplot(7,4,j+1)
#     data = all_results[:,i]
#     data = data[~np.isnan(data)]
#     pl.epdf(data)
    

# #%%
# fig9 = pl.figure(9)
# fig9.clf()

# for j,i in enumerate(sort_i):
#     pl.subplot(7,4,j+1)
#     data = all_results[:,i]
#     data = data[~np.isnan(data)]
#     pl.hist(data,100)



# #%%
# data = all_results[:,19]
# data = data[~np.isnan(data)] 
# pl.hist(data,np.arange(0,200,5))
# pl.yscale('log')


#%% test index for pred_data indexing with i=10
# pl.figure(1)
# pl.clf()
# pl.subplot(121)
# pl.imshow(pfos_data,extent= ll)
# pl.plot(2059515.1626703418, 2690088.025430553,'.',ms=10,color='r')

# pl.subplot(122)
# pl.imshow(pfos_data)
# pl.plot(292,323,'.',ms=10,color='r')