# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 13:49:20 2026

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
from matplotlib.lines import Line2D


outfolder = r"C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\site_specific\LD1600_report\20261119_hydro_discussion_figures"

seqs = [27476,28191,29257,29722,30016,30055,
       30303,30409,30613,159164]

color_map = {'Ha': '#aec7e8', # Holocene Alluvium
             'Hw': '#1f77b4', # Holocene Wetland
             'Pp': '#c7c7c7', # Presumpscot Formation
             'Pt': '#e377c2', # Till
             'Pem': '#f7b6d2',# End Moraine 
             'Pm': '#ff7f0e', # Shoreline
             'Pg': '#ffbb78', # Glacier Meltwater
             'Pu': '#ff9896', # Undifferentiated
             'other': '#98df8a',}

extended_legend = ['Ha - Holocene Alluvium',
                   'Hw - Holocene Wetland',
                   'Pp - Pliestocene Presumpscot Formation',
                   'Pt - Pliestocene Till',
                   'Pem - Pliestocene End Moraine',
                   'Pm - Pliestocene Shoreline',
                   'Pg - Pliestocene Glacier Meltwater Contact',
                   'Pu - Pliestocene Undifferentiated Glacier Sediment',
                   'Other']


#%% load pfas data 
# seqs =[27772,28537,28617,29228,29233,29478,29584,29848,
#           29946,30059,30369,30437,157189,
#           159164,161489] # JR identied sequences. 

dist = 600

data = pd.read_excel(paths.report_database,sheet_name='Sheet 1')
# extract sum of 6 exceedance 
data = data[data.PARAMETER == 'SUM OF 6 PFAS']


# load_licened field
fields = gpd.read_file(paths.fields)

# make pyproj object to project into epsg:29616
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

#%% plotting 
for seq in seqs:
    main_fields = fields[fields.EGAD_SITE_ == int(seq)]
    
    
    
    ROI = main_fields.total_bounds + [-dist, -dist, dist, dist]
    x = [ROI[0] , ROI[0] , ROI[2] , ROI[2] , ROI[0]]
    y = [ROI[1] , ROI[3] , ROI[3] , ROI[1] , ROI[1]]
    ROI = np.array(np.vstack((x,y))).T
    ROI = shapely.Polygon( ROI )
    # extract surfical units within box
    geol = gpd.read_file(paths.surficial, mask= ROI, layer='Maine_Surficial_Geology_Units')
    geol = geol.clip(ROI)
    # make simplied unit name column
    s_unit = []
    units = color_map.keys()
    for geo in geol.iterrows():
        geo = geo[1]
        other = True
        for unit in units:
            if geo.UNIT.startswith(unit):
                s_unit.append(unit)
                other = False
                break
        if other:
            s_unit.append('other')
    geol['s_unit'] = s_unit
    
    # exrtract sample locations 
    locs = sum6.clip(ROI)
    # extract fields
    field = fields.clip(ROI)
    
    fig = pl.figure()
    fig.clf()
    ax = fig.add_subplot(111)
    
    geol["plot_color"] = geol["s_unit"].map(color_map)
    aa = geol.plot(edgecolor='black',color=geol["plot_color"],ax=ax,legend=True)
    
    pt_colors = np.where(locs.CONCENTRATION > 20, 'red', 'blue')
    locs.plot(color=pt_colors, ax=ax, markersize=50)
    
    field.plot(edgecolor='white', facecolor = 'none', ax=ax)
    
    ax.axis('equal')
    
    # aa.legend(bbox_to_anchor=(1.45, 1))
    
    custom_points = [Line2D([0], [0], marker="o", linestyle="none", markersize=10, color=color) for color in color_map.values()]
    leg_points = ax.legend(custom_points, color_map.keys(),loc=5,bbox_to_anchor =[1.4,.5])
    ax.add_artist(leg_points )          
    
    
    ax.set_title(seq)
    ax.set_xlabel('Easting (km)')
    ax.set_ylabel('Northing (km)')

    fig.savefig(outfolder+'/surficial_{}_exceed.png'.format(seq))
    pl.close(fig)


#%% print legend
fig3 = pl.figure()
fig3.clf()

ax = fig3.add_subplot(111)

custom_points = [Line2D([0], [0], marker="o", linestyle="none", markersize=10, color=color) for color in color_map.values()]
leg_points = ax.legend(custom_points, extended_legend,loc=5,bbox_to_anchor =[1,.5])
ax.add_artist(leg_points ) 
  
fig3.savefig(outfolder+'/surficial_legend_extend.png')

fig3 = pl.figure()
fig3.clf()

ax = fig3.add_subplot(111)

custom_points = [Line2D([0], [0], marker="o", linestyle="none", markersize=10, color=color) for color in color_map.values()]
leg_points = ax.legend(custom_points, color_map.keys(),loc=5,bbox_to_anchor =[1,.5])
ax.add_artist(leg_points ) 
  
fig3.savefig(outfolder+'/surficial_legend.png')



   
#%% make map with concentrations dots 
for seq in seqs:
    main_fields = fields[fields.EGAD_SITE_ == int(seq)]
    
    
    
    ROI = main_fields.total_bounds + [-dist, -dist, dist, dist]
    x = [ROI[0] , ROI[0] , ROI[2] , ROI[2] , ROI[0]]
    y = [ROI[1] , ROI[3] , ROI[3] , ROI[1] , ROI[1]]
    ROI = np.array(np.vstack((x,y))).T
    ROI = shapely.Polygon( ROI )
    # extract surfical units within box
    geol = gpd.read_file(paths.surficial, mask= ROI, layer='Maine_Surficial_Geology_Units')
    geol = geol.clip(ROI)
    # make simplied unit name column
    s_unit = []
    units = color_map.keys()
    for geo in geol.iterrows():
        geo = geo[1]
        other = True
        for unit in units:
            if geo.UNIT.startswith(unit):
                s_unit.append(unit)
                other = False
                break
        if other:
            s_unit.append('other')
    geol['s_unit'] = s_unit
    
    # exrtract sample locations 
    locs = sum6.clip(ROI)
    # extract fields
    field = fields.clip(ROI)
    
    fig = pl.figure()
    fig.clf()
    ax = fig.add_subplot(111)
    
    geol["plot_color"] = geol["s_unit"].map(color_map)
    aa = geol.plot(edgecolor='black',color=geol["plot_color"],ax=ax,legend=True)
    
    field.plot(edgecolor='white', facecolor = 'none', ax=ax)
    
    locs_not0 = locs[locs.CONCENTRATION > 0 ]
    
    pt_colors = np.where(locs_not0.CONCENTRATION > 20, 'red', 'none')
    locs_not0.plot( ax=ax, markersize=50,column='CONCENTRATION',legend=True)
    locs_not0.plot(ax=ax, edgecolor=pt_colors, markersize=50, marker='o',color='none')
    
    locs0 =  locs[locs.CONCENTRATION == 0 ]
    locs0.plot(ax=ax, markersize=50, marker='^',color='tab:blue')
    
    
    
    ax.axis('equal')

    # custom_points = [Line2D([0], [0], marker="o", linestyle="none", markersize=10, color=color) for color in color_map.values()]
    # leg_points = ax.legend(custom_points, color_map.keys(),loc=5,bbox_to_anchor =[1.4,.5])
    # ax.add_artist(leg_points )          
    
    
    ax.set_title(seq)
    ax.set_xlabel('Easting (km)')
    ax.set_ylabel('Northing (km)')

    fig.savefig(outfolder+'/surficial_{}_concent.png'.format(seq))
    pl.close(fig)
    
#%% make map of locations 
mask = fields.EGAD_SITE_.isin(seqs)
# data2 = data.data

rep_pt = []
for seq in seqs:
    f = fields[fields.EGAD_SITE_ == seq]
    rep_pt.append( f.iloc[0].geometry.representative_point() )

outline = gpd.read_file(paths.me_outline)
geol = gpd.read_file(paths.surficial,layer='Maine_Surficial_Geology_Units')
limit = gpd.read_file(paths.marine_limit)
# geol_all = geol.geometry.union_all()
# geol_outline = geol_all.boundary

   
#% maps showing locations 



fig2 = pl.figure(4)
fig2.clf()
ax = fig2.add_subplot(111)


geol.boundary.plot(ax=ax,label='24k maps')
limit.plot(ax=ax,color='red',lw=.5,label='Marine Limit')
outline.plot(ax=ax,lw=.5,color='black')
ii = True
for pt in rep_pt:
    if ii:
        pl.plot(pt.x,pt.y,'r.',label='Surficial Geology Site')
        ii=False
    else:
        pl.plot(pt.x,pt.y,'r.')
# pl.axis('equal')      
pl.xlabel('Easting (m)')
pl.ylabel('Northing (m)')
pl.legend(loc="center left", bbox_to_anchor=(1.02, .5))

pos = ax.get_position()
ax.set_position([pos.x0-.25,pos.y0,pos.width,pos.height])

fig2.savefig(outfolder+'/State_map.png',dpi=300)











