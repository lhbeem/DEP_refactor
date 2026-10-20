# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 16:14:24 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'..','..','lookup'))
sys.path.append(os.path.join(base_folder,'..','..',))

import paths
import geo_utils
import numpy as np
import geopandas as gpd
import pandas as pd
import pylab as pl
from matplotlib.patches import Patch
import rioxarray
#%% import maine outline
outline = gpd.read_file(paths.me_outline)
outline_bounds = outline.total_bounds
lo_res = gpd.read_file(paths.me_outline_lo)

dd = 1000# grid spacing in meters
x,y = np.meshgrid(np.arange(outline_bounds[0],outline_bounds[2],dd), np.arange(outline_bounds[1],outline_bounds[3],dd))
y = np.flipud(y)

#%%import gw results both lD1600 and non-LD1600
threshold = 1.92
compound = 'PFOS'

gw = gpd.read_file(paths.sample_locations)
non_gw = gpd.read_file(paths.nonLD_gw)
# combine gw results 
all_gw = gpd.GeoDataFrame(pd.concat([gw, non_gw], ignore_index=True), crs=gw.crs)
all_gw.fillna('')
all_gw.replace(to_replace=[None], value='', inplace=True)


if compound == '6':
    if threshold == 0:
        background = all_gw[all_gw.SUM_OF_6_P.str.startswith('ND')]
else:
    background = pd.DataFrame()
    
    for i in all_gw.iterrows():
        i = i[1]
        if i[compound] == '':
            continue
        elif i[compound].startswith('ND'):
            background = pd.concat([background, pd.DataFrame(i)], ignore_index=True, axis = 1)
        else:
            con = float(i[compound].split(' ')[0])
            if con < threshold:
                background = pd.concat([background, pd.DataFrame(i)], ignore_index=True, axis = 1 ) 
        
background = background.T
    


#%%  calculate distance to nearest subthreshold location
dist = np.ones(x.shape) * 1e6
il = np.ones(x.shape) * np.nan

for i,pt in enumerate(background.iterrows()):
    pt = pt[1]
    d = np.sqrt( ( pt.geometry.x - x) **2 + ( pt.geometry.y - y ) ** 2)
    ind = d < dist
    
    dist[ind] = d[ind]
    il[ind] = pt.EGAD_SITE_
      

#%%
# clip raster
temp_file = base_folder+'/temp.tif'
geo_utils.arr2geotiff( dist , temp_file, 26919, outline_bounds[0], outline_bounds[3], dd,-dd )

raster = rioxarray.open_rasterio(temp_file)
dist_clip = raster.rio.clip(lo_res.geometry)



fig = pl.figure(1)
fig.clf()
ax = fig.add_subplot(111)
pl.imshow(dist_clip[0,:,:]/1000,extent=outline_bounds[[0,2,1,3]],vmax=120)


outline.plot(ax=ax,lw=.5,color='black')

cb = pl.colorbar()
cb.set_label('Distance to nearest {} ND (km)'.format(compound))
pl.plot(color='r',ax=ax,markersize=1) 

pl.xlabel('Easting (m)')
pl.ylabel('Northing (m)')

fig.savefig(base_folder + '/distance2ND.png',dpi=300)

#%% calculate distance to nearest observation

all_dist = np.ones(x.shape) * 1e6
all_il = np.ones(x.shape) * np.nan

for i,pt in enumerate(all_gw.iterrows()):
    pt = pt[1]
    d = np.sqrt( ( pt.geometry.x - x) **2 + ( pt.geometry.y - y ) ** 2)
    ind = d < all_dist
    
    all_dist[ind] = d[ind]
    il[ind] = pt.EGAD_SITE_

#%%
rd_stats = []

for rd in [1000,2000,4000,8000,16000]: # representative distance 
    dist2 = np.ones(dist.shape) * .5
    dist2[dist < rd] = 0
    dist2[ (dist > 0) & (all_dist > rd) ] = 1
    
    # clip raster
    temp_file = base_folder+'/temp.tif'
    geo_utils.arr2geotiff( dist2 , temp_file, 26919, outline_bounds[0], outline_bounds[3], dd,-dd )
    
    raster = rioxarray.open_rasterio(temp_file)
    clipped_raster = raster.rio.clip(lo_res.geometry)
    
    rd_stats.append( [ rd, np.sum(clipped_raster.values[0,:,:] == 1) , np.sum(clipped_raster.values[0,:,:] == 0.5),  np.sum(clipped_raster.values[0,:,:] == 0) ])
    
    
    
    
    
    fig = pl.figure(2)
    fig.clf()
    ax = fig.add_axes([0.01,0.1,.6,.88])
    ax.imshow(clipped_raster[0,:,:],extent=outline_bounds[[0,2,1,3]])
    
    outline.plot(ax=ax,lw=.5,color='black')
    # lo_res.plot(ax=ax, lw=.5, color='black')
    
    ax.set_xlabel('Easting (m)')
    ax.set_ylabel('Northing (m)')
    
    handles = [Patch(facecolor=[0.267, 0.004, 0.329], edgecolor='none', label='ND within distance',),
               Patch(facecolor=[0.127, 0.566, 0.550], edgecolor='none', label='Samples exist but no ND'),
               Patch(facecolor=[0.993, 0.906, 0.143], edgecolor='none', label='No sample within distance')]
                     
    
    ax.legend(handles=handles, title="Distance = {} km".format(dd/1000), loc='right',bbox_to_anchor = (1.95,0.5))                

    fig.savefig(base_folder+'/state_distance_{}.png'.format(rd),dpi=300,)


#%%

rd_stats = []
for rd in range(200,20001,100): # representative distance 
    dist2 = np.ones(dist.shape) * .5
    dist2[dist < rd] = 0
    dist2[ (dist > 0) & (all_dist > rd) ] = 1
    
    # clip raster
    temp_file = base_folder+'/temp.tif'
    geo_utils.arr2geotiff( dist2 , temp_file, 26919, outline_bounds[0], outline_bounds[3], dd,-dd )
    
    raster = rioxarray.open_rasterio(temp_file)
    clipped_raster = raster.rio.clip(lo_res.geometry)
    
    rd_stats.append( [ rd, np.sum(clipped_raster.values[0,:,:] == 1) , np.sum(clipped_raster.values[0,:,:] == 0.5),  np.sum(clipped_raster.values[0,:,:] == 0) ])



#%%

rd_stats = np.array(rd_stats)
no_pix = np.sum(rd_stats[0,1:])

per_ND = rd_stats[:,3] / (rd_stats[:,2] + rd_stats[:,3]) * 100
# per_samp
per_too_far = rd_stats[:,1] / no_pix * 100


fig = pl.figure(1)
fig.clf()
ax = fig.add_subplot(111)
ax.plot(rd_stats[:,0],per_ND)
ax2 = ax.twinx()
ax2.plot(rd_stats[:,0],per_too_far,color='tab:orange')
ax.set_xlabel('Representative Distance (m)')

ax.set_ylabel('Percent of area with samples with ND closer than rep Dist')
ax2.set_ylabel('Percent of area with samples closer than rep Dist')



