# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 12:45:19 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'../../lookup'))

import paths

import shutil
import pandas as pd
import geopandas as gpd
import shapely 
import pyproj
import matplotlib.pylab as pl
import numpy as np

'''
Make map for each site comparing exceedances to surficial geology
'''


#%% load data
data = pd.read_excel(paths.report_database,sheet_name='Sheet 1')

# extract sum of 6 exceedance 
data = data[data.PARAMETER == 'SUM OF 6 PFAS']
# data = data[data.CONCENTRATION > 20]

# load_licened field
fields = gpd.read_file(paths.fields)


# make pyproj object to project into egsg:29616
P = pyproj.Proj('EPSG:26919')




#%% list of unique sample locations
locs = set(data.SAMPLE_POINT_NAME)

# make geo dataframe for each sample location,
# if multiple samples exist the highest concentration is taken

columns = ['SAMPLE_POINT_NAME','CONCENTRATION','SITE_SEQ','geometry']
sum6 = gpd.GeoDataFrame(columns=columns)
for loc in locs:
    all_samps = data[data.SAMPLE_POINT_NAME == loc]
    row = all_samps.loc[all_samps.CONCENTRATION.idxmax()]
    sum6.loc[len(sum6)] = {'SAMPLE_POINT_NAME' : loc,
                'CONCENTRATION' : row.CONCENTRATION,
                'SITE_SEQ' : row.SITE_SEQ,
                'geometry' : shapely.Point(P(row.SAMPLE_POINT_LONGITUDE,row.SAMPLE_POINT_LATITUDE))}
    
#%%
def plot_geom(gdf,ax,color=None,fill=False,point=False,outline=False):
    if fill:
        gdf.plot()
        # pts = shapely.get_coordinates(gdf[1].geometry)
        # ax.fill(pts[:,0]/1000,pts[:,1]/1000,label=gdf[1].UNIT)
    if point:
        pts = shapely.get_coordinates(gdf[1].geometry)
        if color is not None:
            ax.plot(pts[:,0],pts[:,1],'.', color= color)
        else:
            ax.plot(pts[:,0],pts[:,1],'r.')
    if outline:
        pts = shapely.get_coordinates(gdf[1].geometry)
        ax.plot(pts[:,0],pts[:,1],'w')

    return 


no_geol = []
no_field = []
no_locs = []
complete = []
dist = 500 #  [meters] to make initial bounding box


sites = set(sum6.SITE_SEQ)
for site in sites:
    # make bounding box based off of spreading fields and buffer distance
    main_fields = fields[fields.EGAD_SITE_ == int(site)]
    if len(main_fields) == 0:
        print('site has no field polygon: {}'.format(site))
        no_field.append(site)
        continue
    
    
    ROI = main_fields.total_bounds + [-dist, -dist, dist, dist]
    x = [ROI[0] , ROI[0] , ROI[2] , ROI[2] , ROI[0]]
    y = [ROI[1] , ROI[3] , ROI[3] , ROI[1] , ROI[1]]
    ROI = np.array(np.vstack((x,y))).T
    ROI = shapely.Polygon( ROI )
    # extract surfical units within box
    geol = gpd.read_file(paths.surficial, mask= ROI, layer='Maine_Surficial_Geology_Units')
    if len(geol) == 0:
        print('Site outside 24k surficial maps: {}'.format(site))
        no_geol.append(site)
        continue
    
    # extract sample points
    locs = sum6.clip(ROI)
    
    if len(locs) == 0:
        print('Site has no samples in ROI: {}'.format(site))
        no_locs.append(site)
        continue
    
    # extract fields
    field = fields.clip(ROI)
    
    # geology
    geol = geol.clip(ROI)
    
   
    fig = pl.figure(1)
    fig.clf()
    ax = fig.add_subplot(111)
    
    geol.plot(edgecolor='black',cmap="tab20",ax=ax,legend=True,column = 'UNIT')
    
    pt_colors = np.where(locs.CONCENTRATION > 20, 'red', 'blue')
    # locs['point_color'] = np.where(locs.CONCENTRATION > 20, 'red', 'blue')
    locs.plot(color=pt_colors, ax=ax, markersize=50)
    
    field.plot(edgecolor='white', facecolor = 'none', ax=ax)

    ax.set_title(site)
    ax.set_xlabel('Easting (km)')
    ax.set_ylabel('Northing (km)')
    
    fig.savefig(base_folder+'/surficial_maps/{}.pdf'.format(site))
    complete.append(site)

#%% copy promising to all_figures

seqs_possibly = [29722,30016,27476,30369,30055]
seqs_maybe    = [28191,33204,29603,160720,30295,
                 30409,30613,30059,160723,
                 29228,29402,30303,142099]

nn = 1
for seq in seqs_possibly:
    shutil.copyfile(base_folder+'/surficial_maps/{}.png'.format(seq),
                    base_folder+'/all_figures/surf{:02}_{}.png'.format(nn,seq))
    nn +=1

for seq in seqs_maybe:
    shutil.copyfile(base_folder+'/surficial_maps/{}.png'.format(seq),
                    base_folder+'/all_figures/surf{:02}_{}.png'.format(nn,seq))
    nn +=1




table = pd.DataFrame(columns = ['Detail', 'Magnitude'])
table.loc[len(table)] = ['Number of sites', len(sites) ]
table.loc[len(table)] = ['Number of maps created', len(complete) ]
table.loc[len(table)] = ['Number of sites without field', len(no_field) ]
table.loc[len(table)] = ['Number of sites with field, but outside 24k surficial', len(no_geol) ]
table.loc[len(table)] = ['Number of sites with field and surficial, but no sample locations', len(no_locs) ]
table.loc[len(table)] = ['','']
table.loc[len(table)] = ['Number of sites possible correlaion', len(seqs_possibly) ]
table.loc[len(table)] = ['Number of sites maybe correlaion', len(seqs_maybe) ]
    
fig = pl.figure(1)
fig.clf()
ax = fig.add_subplot(111)
ax.axis('off')
tbl = ax.table(cellText=table.values, colLabels=None, loc='center',cellLoc='center')

fig.savefig(base_folder+'/all_figures/surf00_basic_stats.pdf',bbox_inches='tight')   