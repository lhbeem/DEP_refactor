# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 15:20:36 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'../../lookup'))

import paths
import numpy as np
import pyproj
import pandas as pd
import geopandas as gpd
import shapely 
import matplotlib.pylab as pl

#%%
'''
compare contamiantion composition between inside and outside of unit
'''

def plot_locations(df):
    
    pl.figure(1)
    pl.clf()
    
    df.plot()
    for x,y,label in zip( df.geometry.x, df.geometry.y, df.SAMPLE_POINT_SEQ):
        pl.text(x,y,str(label))
    pl.title(df.SITE_SEQ.iloc[0])
   
    

def representive_concentration(df):
    P = pyproj.Proj('EPSG:26919')
    locs = set(df.SAMPLE_POINT_SEQ)
    columns = ['SAMPLE_POINT_NAME','SAMPLE_POINT_SEQ','CONCENTRATION','SITE_SEQ','geometry']
    sorted_data = gpd.GeoDataFrame(columns=columns)
    for loc in locs:

        all_samps = df[df.SAMPLE_POINT_SEQ == loc]
        name = all_samps.SAMPLE_POINT_NAME.iloc[0]
        row = all_samps.loc[all_samps.CONCENTRATION.idxmax()]
        sorted_data.loc[len(sorted_data)] = {'SAMPLE_POINT_NAME' : name,
                    'SAMPLE_POINT_SEQ' : loc, 
                    'CONCENTRATION' : row.CONCENTRATION,
                    'SITE_SEQ' : row.SITE_SEQ,
                    'geometry' : shapely.Point(P(row.SAMPLE_POINT_LONGITUDE,row.SAMPLE_POINT_LATITUDE))}
    return sorted_data
#%%
outfolder = r"C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\site_specific\LD1600_report\20261119_hydro_discussion_figures"

seqs = [27476,28191,29257,29722,30016,30055,
       30303,30409,30613,159164]


data = pd.read_excel(paths.report_database,sheet_name='Sheet 1')

# make pyproj object to project into epsg:29616
P = pyproj.Proj('EPSG:26919')


# use plot_locations to get sample_point_seq for points in unit
use = { '27476' : [159761,159765],
        '28191' : False,
        '29257' : False,
        '29722' : [163259,163140,163142,154880,157779],
        '30016' : [146276,146358,146888,147455,147514,
                   158789,147100,146886,152063,152226,153260],
        '30055' : False,
        '30303' : False,
        '30409' : False,
        '30613' : False,
        '159164': False,
        }


use2 = {'30016' : [146278, 146279,146887],
        }

unit = {'27476' : 'Pem',
        '28191' : 'Pt',
        '29257' : 'Pem',
        '29722' : 'Pu',
        '30016' : 'Pg',
        '30055' : 'Pp',
        '30303' : 'Pt',
        '30409' : 'Pg',
        '30613' : 'Pt',
        '159164': 'Pm',
        }


#%%


seq2 = 30016
comp_data = data[(data.SITE_SEQ == seq2) & (data.PARAMETER == 'SUM OF 6 PFAS')]
comp_data = representive_concentration(comp_data)
plot_locations(comp_data)

#%%
# parameters sorted by chain length
params = ['HFPO-DA',
          'PFBA',
          'PFBS',
          '4:2 FTS',
          'PFPEA',
          'PFPES',
          'PFHXA',
          'PFHXDA',
          'PFHXS',
          'PFHPA',
          'PFHPS',
          'ADONA',
          'PFOS',
          'PFOA',
          'N-MeFOSAA',
          'PFOSA',
          'N-EtFOSAA',
          '6:2 FTS',
          'PFNA',
          'PFNS',
          'PFDA',
          'PFDS',
          '8:2 FTS',
          'PFUNDA',
          'PFDOA',
          'PFTRIA',
          'PFTEA',
          'PFODA',
          'SUM OF 6 PFAS',
          'TOTAL Short-Chain PFCAs',
          'TOTAL Short-Chain PFSAs',
          'TOTAL Long-Chain PFCAs',
          'TOTAL Long-Chain PFSAs',
          'TOTAL PFCA Precursors',
          'TOTAL PFSA Precursors',]


for seq in [27476]:
    
    
    unit_con = {}
    not_unit_con = {}
    for param in params:
        # get PFOS results, 
        comp_data = data[(data.SITE_SEQ == seq) & (data.PARAMETER == param)]
        comp_data = representive_concentration(comp_data)
        # remove samples with a position
        comp_data = comp_data[~comp_data.geometry.x.isna()]
        
        
        
        unit_con[param] = comp_data[comp_data.SAMPLE_POINT_SEQ.isin(use[str(seq)])]
        not_unit_con[param] = comp_data[~comp_data.SAMPLE_POINT_SEQ.isin(use[str(seq)])]


    fig = pl.figure(1)
    fig.clf()
    ax = fig.add_axes([.05,.4,.9,.55])
    
    x_pos = 0
    tick_label = []
    tick_label_pos = []
    for param in  params:
        un = unit_con[param]
        nun = not_unit_con[param]
        if np.all(un.CONCENTRATION == 0) and np.all(nun.CONCENTRATION == 0):
            continue
        
        pl.plot(np.ones(len(unit_con[param]))* x_pos , unit_con[param].CONCENTRATION,'.',color='tab:blue')
        pl.plot(np.ones(len(not_unit_con[param]))*(x_pos +1), not_unit_con[param].CONCENTRATION,'.',color='tab:orange')
        
        tick_label.append(param)
        tick_label_pos.append(x_pos+.5)
        x_pos += 3
        
    pl.ylabel('Concentration (ppt)')
    pl.xticks(tick_label_pos, tick_label ,rotation= 90)
    fig.savefig(outfolder + '/{}_composition.png'.format(seq), dpi=300)
    
    
    
    
    
    
    
    
    
    
    
    #get PFOA results
