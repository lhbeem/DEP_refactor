# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 13:28:41 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'../../lookup'))
sys.path.append(os.path.join(base_folder,'../../pfas_utils'))

import paths
# from pfas_map import layer_compounds as compounds
import numpy as np
import geopandas as gpd
import pandas as pd
import pylab as pl
# import pyproj
# import rasterio


soil = gpd.read_file(paths.soil_polygons)

F82 = []
for i in range(len(soil)):
    data = FTS82 = soil.iloc[i].F8_2_FTS
    if data is None:
        continue
    data = data.split(' ')[0]
    if data == 'ND':
        data = 0
    
    geos = soil.iloc[i].geometry
    if geos is None:
        x = np.nan
        y = np.nan
    else:
        geo = geos.geoms[0].representative_point()
        x = geo.x
        y = geo.y

    F82.append([float(data),x,y,soil.iloc[i].EGAD_SITE_])
    

F82 = np.array(F82)


#%%

#load outline of state
outline = gpd.read_file(paths.me_outline)

#%%

thres = 10

F82_nozero = F82[F82[:,0]>thres,:]



#%% source 

source = pd.read_pickle(paths.pfas_source)



for seq in set(F82_nozero[:,3]):
    s = str(int(seq))
    try:
        print('{} : {}'.format(s,source[s]))
    except:
        print('{} No source'.format(s))
        


#%%


fig = pl.figure(1)
pl.clf()

for i in range(len(outline)):
    pl.plot(outline.iloc[i].geometry.xy[0],outline.iloc[i].geometry.xy[1],'-k',lw=1)
    
pl.scatter(F82_nozero[:,1],F82_nozero[:,2],c=F82_nozero[:,0],s=5,cmap='cool',label='Positive Detections')

lab_n = 0
for i in range(len(F82_nozero)):
    s = str(int(F82_nozero[i,3]))
    try:
        if 'Kennebec Sanitary TD' in source[s]:
            if lab_n == 0:
                lab_n +=1 
                pl.plot(F82_nozero[i,1] , F82_nozero[i,2], 'ro',markersize=5,markerfacecolor='None',label='Kennebec STD Source')

            else:
                pl.plot(F82_nozero[i,1] , F82_nozero[i,2], 'ro',markersize=5,markerfacecolor='None')
    except:
        continue


cb = pl.colorbar()
cb.set_label('8:2 FTS soil concentration (ppb)')
pl.axis('equal')
pl.title('8:2FTS > {} ppb'.format(thres))
pl.legend()

fig.savefig(base_folder +'/F82_map.pdf')
