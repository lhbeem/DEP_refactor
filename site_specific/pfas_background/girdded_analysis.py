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
import rasterio
import numpy as np
import geopandas as gpd
import pandas as pd
import pyproj 
import pylab as pl


#import grid
pfoa_pred = rasterio.open(paths.PFOA_soil_pred)
pfoa_data = pfoa_pred.read(1)
dx,dy = pfoa_pred.res # same for both maps
ulx = pfoa_pred.transform[2]
uly = pfoa_pred.transform[5]
lrx = pfoa_pred.width * pfoa_pred.transform[0] + ulx
lry = pfoa_pred.height * pfoa_pred.transform[4] + uly
ll = [ulx,lrx,lry,uly] # same for both maps
proj = pfoa_pred.crs.to_authority() # same for both maps 

P = pyproj.Transformer.from_crs('{}:{}'.format(proj[0],proj[1]), 'EPSG:26919',always_xy=True)


x,y = np.meshgrid(np.arange(ulx+500,lrx,dx), np.arange(lry+500,uly,dy))# midpoint of grid
# y = np.flipud(y)

# convert to 26919
# P = pyproj.Transformer.from_crs('{}:{}'.format(proj[0],proj[1]), 'EPSG:26919',always_xy=True)
# x,y = P.transform(x,y)
#%% import maine outline
# outline = gpd.read_file(paths.me_outline)
# outline_bounds = outline.total_bounds
# # crop x,y mesh to match extent of maine
# x_mask = (x>outline_bounds[0]) & (x<outline_bounds[2])
# y_mask = (y>outline_bounds[1]) & (y<outline_bounds[3])
# me_mask = x_mask & y_mask

#%%import gw results both lD1600 and non-LD1600 
gw = gpd.read_file(paths.sample_locations)
non_gw = gpd.read_file(paths.nonLD_gw)

# combine gw results 
all_gw = gpd.GeoDataFrame(pd.concat([gw, non_gw], ignore_index=True), crs=gw.crs)

all_gw.fillna('')
all_gw.replace(to_replace=[None], value='', inplace=True)

sum6_ND = all_gw[all_gw.SUM_OF_6_P.str.startswith('ND')]



#%%
P = pyproj.Transformer.from_crs( 'EPSG:26919','{}:{}'.format(proj[0],proj[1]),always_xy=True)
dist = np.ones(x.shape) * 1e6
il = np.ones(x.shape) * np.nan

for i,pt in enumerate(sum6_ND.iterrows()):
    pt = pt[1]
    px,py = P.transform(pt.geometry.x,pt.geometry.y)
    d = np.sqrt( ( x - px) **2 + ( y - py ) ** 2)
    ind = d < dist
    
    dist[ind] = d[ind]
    il[ind] = pt.EGAD_SITE_
     
# pfoa_data_mask
ii = pfoa_data == pfoa_data[0,0]
dist[ii] = np.nan

    
# mask
# dist[~me_mask] = np.nan          

#%%
fig = pl.figure(1)
fig.clf()
pl.imshow(dist,extent=ll)
# for out in outline.iterrows():
#     xy = np.array(out[1].geometry.coords)
#     pl.plot(xy[:,0],xy[:,1],'k')

pl.colorbar()           
            
