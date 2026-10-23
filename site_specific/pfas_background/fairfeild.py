# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 15:30:49 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'../../lookup'))

import paths
import shapely
import numpy as np
import geopandas as gpd
import pandas as pd
from matplotlib import pylab as pl

#%% load data

# ROI fairfield
x1 = 439710
x2 = 454158
y1 = 4949607
y2 = 4934696
x = [x1 , x2 , x2, x1 , x1]
y = [y2 , y2 , y1 , y1 , y2]
ROI = np.array(np.vstack((x,y))).T 
ROI = shapely.Polygon( ROI )

gw = gpd.read_file(paths.sample_locations, mask=ROI)
non_gw = gpd.read_file(paths.nonLD_gw,mask=ROI)
# combine gw results 
all_gw = gpd.GeoDataFrame(pd.concat([gw, non_gw], ignore_index=True), crs=gw.crs)
all_gw.fillna('')
all_gw.replace(to_replace=[None], value='', inplace=True)


sum6_ND = all_gw[all_gw['SUM_OF_6_P'].str.startswith('ND')]
pfos_ND = all_gw[all_gw['PFOS'].str.startswith('ND')]
pfoa_ND = all_gw[all_gw['PFOA'].str.startswith('ND')]


fig = pl.figure(1,figsize=[11,8])
fig.clf()
ax1 = pl.subplot(131)
all_gw.plot(markersize=1,ax=ax1,label='All samples')
pfos_ND.plot(markersize=1,color='r',ax=ax1,label='PFOS ND')
pl.title ('Fairfield PFOS - {:.0f}%'.format(round(len(pfos_ND)/len(all_gw) * 100 , 0)))

pl.legend()




ax2 = pl.subplot(132)
all_gw.plot(markersize=1,ax=ax2,label='All samples')
sum6_ND.plot(markersize=1,color='r',ax=ax2,label='Sum6 ND')
pl.title ('Fairfield Sum6 - {:.0f}%'.format(round(len(sum6_ND)/len(all_gw) * 100 , 0)))

pl.legend()


ax3 = pl.subplot(133)
all_gw.plot(markersize=1,ax=ax3,label='All samples')
pfoa_ND.plot(markersize=1,color='r',ax=ax3,label='PFOA ND')
pl.title ('Fairfield PFOA - {:.0f}%'.format(round(len(pfoa_ND)/len(all_gw) * 100 , 0)))

pl.legend()

fig.savefig(base_folder+'/fairfield.png',dpi=300)