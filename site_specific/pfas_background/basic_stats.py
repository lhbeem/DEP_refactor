# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 10:31:14 2026

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



#%% load data
gw = gpd.read_file(paths.sample_locations)
non_gw = gpd.read_file(paths.nonLD_gw)
# combine gw results 
all_gw = gpd.GeoDataFrame(pd.concat([gw, non_gw], ignore_index=True), crs=gw.crs)
all_gw.fillna('')
all_gw.replace(to_replace=[None], value='', inplace=True)


#%% print Basic stats

compounds = [ 'SUM_OF_6_P',
             'F4_2_FTS', 
'F6_2_FTS',
'F8_2_FTS', 
'ADONA', 
'HFPO_DA', 
'N_EtFOSAA', 
'N_MeFOSAA', 
'PFBA',
'PFBS', 
'PFDA', 
'PFDOA', 
'PFDS', 
'PFHPA', 
'PFHPS', 
'PFHXA', 
'PFHXDA',
'PFHXS', 
'PFNA', 
'PFNS', 
'PFOA', 
'PFODA', 
'PFOS', 
'PFOSA', 
'PFPEA',
'PFPES', 
'PFTEA', 
'PFTRIA', 
'PFUNDA']


#%%
n = len(all_gw)
print('Total Samples: {}'.format(n))

n_all= []
for compound in compounds:
    nn = len(all_gw[all_gw[compound].str.startswith('ND')])
    n_all.append(nn)
    print('{:10} ND: {:6} ({:.3}%)'.format(compound, nn, nn/n * 100))

#%% bar graph
n_all = np.array(n_all)
compounds = np.array(compounds)
## sort results
ii = np.argsort(n_all)[::-1]
n_all = n_all[ii]
compounds = compounds[ii]


fig = pl.figure(1,figsize=[6,4])
fig.clf()
ax = fig.add_subplot(111)
pos = ax.get_position()
pos.y0 += .2
ax.set_position(pos)

ax.bar(compounds, n_all / n*100)
pl.xticks(rotation=-90,ha='center')
pl.text(29,97,'Number of samples: {}'.format(n),ha='right')
pl.ylabel('Percentage Non-Detect')

fig.savefig(base_folder+'/ND_precentage_par.png',dpi=300)