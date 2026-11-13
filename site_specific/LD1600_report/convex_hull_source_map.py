# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 13:17:29 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'lookup'))

# import paths
# import argparse
import numpy as np
import pandas as pd
import math
import pyproj
import matplotlib.pylab as pl 
import geopandas as gpd
import scipy.spatial as spat 
'''
convex hull source map
'''

class palette:
    blue = '#557fba'
    red = '#bf5550'
    green = '#99bb62'
    purple = '#82649f'
    orange = 'tab:orange'

save_folder = base_folder +'/all_figures'

P = pyproj.Proj('EPSG:26919')
#%% laod data
outline = gpd.read_file(r"C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\data\geo_files\lo_res_maine.gpkg")


gw_data_path = r"C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\data\LD1600_report\DRAFT_LD1600Dataset_Cleaned_08Oct2026.xlsx"
gw = pd.read_excel(gw_data_path,sheet_name='Sheet 1')
gw_sum6 = gw[gw.PARAMETER == 'SUM OF 6 PFAS']


pie_data = pd.DataFrame(columns = gw.columns)


unique_locations = set(gw.SAMPLE_POINT_SEQ)
unique_sources = list(set(gw.LICENSEE))
# remove nan
unique_sources = [x for x in unique_sources if not (isinstance(x, float) and math.isnan(x))]


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




src_table = pd.DataFrame(columns = ['Generator','Number of Locations','Number of > 20','Number of Sites'])
for src in unique_sources:
    num = pie_data[pie_data.LICENSEE == src]
    gt = pie_data[(pie_data.LICENSEE == src) & (pie_data.CONCENTRATION > 20)]
    site = set(num.SITE_SEQ)
    src_table.loc[len(src_table)] = [src,len(num), len(gt), len(site)]



#%% source geographic distribution 

# make list of hulls
hulls = []
for i,src in enumerate(src_table.iterrows()):
    num = pie_data[pie_data.LICENSEE == src[1].Generator]
    x,y = P(num.SAMPLE_POINT_LONGITUDE,num.SAMPLE_POINT_LATITUDE)
    
    
    pts = np.array((x,y)).T
    # remove nan
    pts = pts[~np.isnan(pts).any(axis=1)]
    if len(pts) < 4:
        continue
    print(len(pts), src[1].Generator)
    hulls.append( [src[1].Generator, len(pts) , spat.ConvexHull(pts), pts ])

#%%
gt = []
for hull in hulls:
    gt.append(hull[1] < 58)
print(np.array(gt).sum())

#%% 

colors = pl.colormaps['viridis'](np.linspace(0,1,43))


fig = pl.figure(1)
fig.clf()
ax = fig.add_subplot(111)

i = 0
for hull in hulls:
    if hull[1] < 58:
        ax.fill(hull[3][hull[2].vertices,0], hull[3][hull[2].vertices,1], lw=2,
                alpha=.3,color=colors[i],edgecolor=None)
        # rp = np.mean(hull[3][hull[2].vertices], axis=0)
        # ax.text(rp[0],rp[1],str(i))
        ax.text[hull[3][hull[2][0,0]], hull[3][hull[2][0,1]] ]
        # if i == 30:
        #     ax.plot(hull[3][:,0],hull[3][:,1],'.')
        i += 1
        

ax.plot( outline.geometry.get_coordinates().x,outline.geometry.get_coordinates().y,'k')
ax.axis('equal')    
    
    
    # fig = pl.figure(1)
    # fig.clf()
    # ax = fig.add_subplot(111)
    
    # ax.plot( outline.geometry.get_coordinates().x/1000,outline.geometry.get_coordinates().y/1000,'k')
        
        
    # ax.plot(x/1000,y/1000,'.', color=palette.orange,ms=2)
    # ax.set_title(src[1].Generator)

    # ax.set_xlabel('Easting (km)')
    # ax.set_ylabel('Northing (km)')
    # ax.axis('equal')
    
    # src_name = src[1].Generator
    # if '/' in src_name:
    #     src_name = src_name.replace('/','&')
    
    # fig.savefig(save_folder+'/source{:02}_{}.pdf'.format(i,src_name),bbox_inches='tight')