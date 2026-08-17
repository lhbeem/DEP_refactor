# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 11:43:05 2026

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
# from matplotlib.patches import Patch



#%% import maine outline
outline = gpd.read_file(paths.me_outline)
outline_bounds = outline.total_bounds

# x,y = np.meshgrid(np.arange(outline_bounds[0],outline_bounds[2],1000), np.arange(outline_bounds[1],outline_bounds[3],1000))
# y = np.flipud(y)


#%% load data
gw = gpd.read_file(paths.sample_locations)
non_gw = gpd.read_file(paths.nonLD_gw)
# combine gw results 
all_gw = gpd.GeoDataFrame(pd.concat([gw, non_gw], ignore_index=True), crs=gw.crs)
all_gw.fillna('')
all_gw.replace(to_replace=[None], value='', inplace=True)


sum6_ND = all_gw[all_gw['SUM_OF_6_P'].str.startswith('ND')]
pfos_ND = all_gw[all_gw['PFOS'].str.startswith('ND')]
pfoa_ND = all_gw[all_gw['PFOA'].str.startswith('ND')]

#%% maps
fig = pl.figure(1,figsize=[9.5,6.5])

fig.clf()
ax1 = fig.add_subplot(131)


all_gw.plot(markersize=1,ax=ax1,label='All samples')
sum6_ND.plot(markersize=1,color='r',ax=ax1,label='Sum of 6 ND')


for out in outline.iterrows():
    xy = np.array(out[1].geometry.coords)
    pl.plot(xy[:,0],xy[:,1],'k',lw=1)

pl.text(321000,5421000,'a)',ha='left',va='top')
pl.legend()
pl.axis('equal')
pl.xlabel('Easting (m)')
pl.ylabel('Northing (m)')

ax2= fig.add_subplot(132)


all_gw.plot(markersize=1,ax=ax2,label='All samples')
pfos_ND.plot(markersize=1,color='r',ax=ax2,label='PFOS ND')


for out in outline.iterrows():
    xy = np.array(out[1].geometry.coords)
    pl.plot(xy[:,0],xy[:,1],'k')

pl.text(321000,5421000,'b)',ha='left',va='top')
pl.legend()
pl.axis('equal')
pl.xlabel('Easting (m)')
# pl.ylabel('Northing (m)')

ax3= fig.add_subplot(133)


all_gw.plot(markersize=1,ax=ax3,label='All samples')
pfoa_ND.plot(markersize=1,color='r',ax=ax3,label='PFOA ND')


for out in outline.iterrows():
    xy = np.array(out[1].geometry.coords)
    pl.plot(xy[:,0],xy[:,1],'k')

pl.text(321000,5421000,'c)',ha='left',va='top')
pl.legend()
pl.axis('equal')
pl.xlabel('Easting (m)')
# pl.ylabel('Northing (m)')

fig.savefig(base_folder+'/basic_map.png',dpi=300)

