# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 16:14:24 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'..','..','lookup'))

import paths
import numpy as np
import geopandas as gpd
import pandas as pd
import pylab as pl
from matplotlib.patches import Patch

#%% import maine outline
outline = gpd.read_file(paths.me_outline)
outline_bounds = outline.total_bounds

x,y = np.meshgrid(np.arange(outline_bounds[0],outline_bounds[2],1000), np.arange(outline_bounds[1],outline_bounds[3],1000))
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
        if i[compound].startswith('ND'):
            background = pd.concat([background, pd.DataFrame(i)], ignore_index=True)
            continue
        con = float(i[compound].split(' ')[0])
        if con < threshold:
           background = pd.concat([background, pd.DataFrame(i)], ignore_index=True) 
        
    
    


#%%
dist = np.ones(x.shape) * 1e6
il = np.ones(x.shape) * np.nan

for i,pt in enumerate(background.iterrows()):
    pt = pt[1]
    d = np.sqrt( ( pt.geometry.x - x) **2 + ( pt.geometry.y - y ) ** 2)
    ind = d < dist
    
    dist[ind] = d[ind]
    il[ind] = pt.EGAD_SITE_
      

#%%
fig = pl.figure(1)
fig.clf()
ax = fig.add_subplot(111)
pl.imshow(dist/1000,extent=outline_bounds[[0,2,1,3]],vmax=100)
for out in outline.iterrows():
    xy = np.array(out[1].geometry.coords)
    pl.plot(xy[:,0],xy[:,1],'k')

cb = pl.colorbar()
cb.set_label('Distance from nearest Sum of 6 ND (m)')
pl.plot(color='r',ax=ax,markersize=1) 

pl.xlabel('Easting (m)')
pl.ylabel('Northing (m)')

#%% fig 2

all_dist = np.ones(x.shape) * 1e6
all_il = np.ones(x.shape) * np.nan

for i,pt in enumerate(all_gw.iterrows()):
    pt = pt[1]
    d = np.sqrt( ( pt.geometry.x - x) **2 + ( pt.geometry.y - y ) ** 2)
    ind = d < all_dist
    
    all_dist[ind] = d[ind]
    il[ind] = pt.EGAD_SITE_

#%%
dd = 200 # representative distance 
dist2 = np.ones(dist.shape) * .5
dist2[dist < dd] = 0
dist2[ (dist > 0) & (all_dist > dd) ] = 1


pl.figure(2)
pl.clf()
ax = pl.subplot(111)
pl.imshow(dist2,extent=outline_bounds[[0,2,1,3]]/1000)
for out in outline.iterrows():
    xy = np.array(out[1].geometry.coords)/1000
    pl.plot(xy[:,0],xy[:,1],'k')

pl.xlabel('Easting (km)')
pl.ylabel('Northing (km)')

handles = [Patch(facecolor=[0.267, 0.004, 0.329], edgecolor='none', label='ND within distance',),
           Patch(facecolor=[0.127, 0.566, 0.550], edgecolor='none', label='Samples exist but no ND'),
           Patch(facecolor=[0.993, 0.906, 0.143], edgecolor='none', label='No sample within distance')]
                 

ax.legend(handles=handles, title="Distance = {} km".format(dd/1000), loc='right',bbox_to_anchor = (1.55,0.5))                

            
