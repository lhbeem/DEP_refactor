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
from pfas_map import layer_compounds as compounds
import numpy as np
import geopandas as gpd
import pandas as pd
import pylab as pl
from pypdf import PdfWriter
import glob
# import pyproj
# import rasterio


soil = gpd.read_file(paths.soil_polygons)

del compounds['Sum of 6']
compounds['HFPO-DA'] = 'HFPO_DA'

source = pd.read_pickle(paths.pfas_source)
gen_list = []
for key in source.keys():
    if isinstance(source[key],str):
        gen_list.append(source[key])
    else:
        for gen in source[key]:
            gen_list.append(gen)

gen_list = list(set(gen_list))
gen_list.append('None')

#%%


thres = {'PFBS': 0,
 'PFBA': 0,
 'PFHXS': 0,
 'PFHXA': 0,
 'PFNA': 0,
 'PFOS': 0,
 'PFOA': 0,
 'HFPO-DA': 0,
 '4:2FTS': 0,
 'PFPEA': 0,
 'PFPES': 0,
 'PFHXDA': 0,
 '6:2FTS': 0,
 'PFHPS': 0,
 'PFHPA': 0,
 'ADONA': 0,
 'NMEFOSAA': 0,
 'FOSA': 0,
 'NETFOSAA': 0,
 '8:2FTS': 10,
 'PFNS': 0,
 'PFDA': 0,
 'PFDS': 0,
 'PFUNA': 0,
 'PFDOA': 0,
 'PFTRDA': 0,
 'PFTA': 0,
 'PFODA': 0}


outline = gpd.read_file(paths.me_outline)


for compound in compounds.keys():
    compound_results = []
    for i in range(len(soil)):
        data = FTS82 = soil.iloc[i][compounds[compound]]
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
    
        compound_results.append([float(data),x,y,soil.iloc[i].EGAD_SITE_])
        
    
    compound_results = np.array(compound_results)
    compound_results_nozero = compound_results[compound_results[:,0]>thres[compound],:]

    src = []
    for seq in set(compound_results_nozero[:,3]):
        s = str(int(seq))
        try:
            src.append(source[s])
        except:
            src.append(['None'])

    source_count = np.zeros(len(gen_list))
    for sr in src:
        if isinstance(sr,str):
            sr = [sr]
        for name in sr:
            
            ii = gen_list.index(name)
            source_count[ii] += 1


    fig = pl.figure(1)
    pl.clf()
    
    for i in range(len(outline)):
        pl.plot(outline.iloc[i].geometry.xy[0],outline.iloc[i].geometry.xy[1],'-k',lw=1)
        
    pl.scatter(compound_results_nozero[:,1],compound_results_nozero[:,2],c=compound_results_nozero[:,0],s=5,cmap='cool',label='Positive Detections')
    
    cb = pl.colorbar()
    cb.set_label('soil concentration (ppb)')
    pl.axis('equal')
    pl.title('{} > {} ppb'.format(compound, thres[compound]))
    pl.legend(loc=4)
    pl.tight_layout()
    fig.savefig(base_folder +'/all_compounds/{}_map.pdf'.format(compound))
    
    
    #%%
    gen_array = np.array(gen_list)
    jj = source_count > 0
    sort_i = np.argsort(source_count[jj])[::-1]
    
 #%%   
    fig2 = pl.figure(2)
    pl.clf()
    ax = fig2.add_subplot(111)
    ax.bar(gen_array[jj][sort_i],source_count[jj][sort_i])
    pl.xticks(rotation = 45,ha='right')
    pl.title(compound)
    pl.tight_layout()
    fig2.savefig(base_folder +'/all_compounds/{}_source.pdf'.format(compound))
    # ax.tick_params("x", rotation=45, rotation_mode="xtick")
    

#%% concatenate files



for keyword in ['*_source.pdf','*_map.pdf']:
    merger = PdfWriter()
    pdfs = glob.glob(base_folder+'/all_compounds/'+keyword)
    all_filename = keyword.replace('*','all')
    mergered_file = base_folder+'/'+all_filename
    for pdf in pdfs:
        merger.append(pdf)

    merger.write(mergered_file)
    merger.close()
    
            
    