# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 15:50:47 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'../../lookup'))

import paths
import numpy as np
import geopandas as gpd
import pandas as pd
import pyproj
import shapely 
import matplotlib.pylab as pl 
#%% load polygons / data
fields = gpd.read_file(paths.soil_polygons)
ref = pd.read_excel(r"C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\data\LD1600_report\Reference Table.xlsx",
                    sheet_name = 'REF_TABLE')
outline = gpd.read_file(paths.me_outline)
#%% load soil map
P = pyproj.Transformer.from_crs("EPSG:26919", "EPSG:5070", always_xy=True)

# get all soil types and areas for each field 
area = []
soil_type = []
location = []
vol = []
years = []
source = []

for field in fields.iterrows():
    field = field[1]
    
    # skip if there is geomety is missing
    if field.geometry == None:
        area.append(None)
        soil_type.append(None)
        location.append(None)
        vol.append(None)
        years.append(None)
        source.append(None)
        continue
    
    #get source/ volume/ years
    seq = field.EGAD_SITE_                                               
    
    if not ref[ref.SITE_EGAD_SEQ == seq]['NUMBER OF YEARS SPREAD'].to_list():
        years.append(None)
    else:
        years.append( ref[ref.SITE_EGAD_SEQ == seq]['NUMBER OF YEARS SPREAD'].iloc[0] )
    
    if not ref[ref.SITE_EGAD_SEQ == seq].VOLUME_SPREAD.to_list():
        vol.append(None)
    else:
        vol.append( ref[ref.SITE_EGAD_SEQ == seq].VOLUME_SPREAD.iloc[0] )
    
    if not ref[ref.SITE_EGAD_SEQ == seq].LICENSEE.to_list():
        source.append( None )
    else:
        source.append( ref[ref.SITE_EGAD_SEQ == seq].LICENSEE.iloc[0] )
    
    
    # get location 
    location.append(field.geometry.geoms[0].representative_point() )
    

    
    
    # convert fields to projection of soils
    fx,fy = field.geometry.geoms[0].exterior.coords.xy
    x,y = P.transform(fx,fy)
    
    coords = list(zip(x, y))
    ROI = shapely.Polygon(coords)
    soils = gpd.read_file(paths.soil, mask=ROI)
    
    # clip soil with field geometry
    a = [] # temp area variable
    s = [] # temp soil symbol variable
    for soil in soils.iterrows():
        soil = soil[1]
        clip = soil.geometry.intersection(ROI)
        a.append(clip.area)
        s.append(soil.MUSYM)
    
    area.append(a)
    soil_type.append(s)


#%% determine most common soil type for each field and get field concentrations 
common_soil = []

for soil,a in zip(soil_type,area):
    if soil == None:
        common_soil.append(None)
    else:
        common_soil.append(soil[np.argmax(a)][:2])



#%% find fields that have only 1 soil type or one soil type is greater than x amount of area
# x (a_thres) is sufficently large such that the field is effective one soil type
a_thres = 0.8 # area threshold


one_soil = [] # list of index and the main soil type
# find only 1 soil type
for i,(soil,a) in enumerate(zip(soil_type,area)):
    if soil == None:
        continue
    if len(soil) == 1:
        one_soil.append([i,soil[0][:2]])
    else:
        total_area = np.sum(a)
        portions = a / total_area
        ii = np.nonzero(portions>a_thres)[0]
        if len(ii) > 0:
            one_soil.append([i,soil[ii[0]][:2]])
        

one_soil_pfoa = []
one_soil_pfos = []
for soil in one_soil:
    pfoa = fields.iloc[soil[0]].PFOA
    pfos = fields.iloc[soil[0]].PFOS
    if pfoa == None:
        one_soil_pfoa.append(None)
    elif pfoa.startswith('ND'):
        one_soil_pfoa.append(0)
    else:
        one_soil_pfoa.append(float(pfoa.split(' ')[0]))

    if pfos == None:
        one_soil_pfos.append(None)
    elif pfos.startswith('ND'):
        one_soil_pfos.append(0)
    else:
        one_soil_pfos.append(float(pfos.split(' ')[0]))



# for each soil type plot as a column
fig = pl.figure(1)
pl.clf()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

xtic = []
j = 0
for soil in set(np.array(one_soil)[:,1]):
    ss = np.array(one_soil)[:,1]
    ii = np.nonzero(ss == soil)[0]
    if len(ii) < 5:
        continue
    xtic.append('{}({})'.format(soil,len(ii)))
    
    for i in ii:
        if one_soil_pfoa[i] == None:
            continue
        else:
            if one_soil_pfoa[i] == 0:
                ax1.plot(j,one_soil_pfoa[i],'r^',ms=4)
            else:
                ax1.plot(j,one_soil_pfoa[i],'k.')
       
        
        if one_soil_pfos[i] == None:
            continue
        else:
            if one_soil_pfos[i] == 0:
                col = 'r'
            elif one_soil_pfos[i] < 2:
                col = 'g'
            else:
                col = 'k'
            
            ax2.plot(j,one_soil_pfos[i],'.',ms=4, markerfacecolor = col,markeredgecolor=col)
    j += 1
            
pl.xticks(np.arange(0,len(xtic)),xtic,rotation=-90,fontsize=6)      
#%% cycle through each soil type and make figures and maps
pl.ioff()
one_soil = np.array(one_soil)
for soil in set(one_soil[:,1]):
    ss = one_soil[:,1]
    ii = np.nonzero(ss == soil)[0]
    if len(ii) < 5:
        continue
    
    fig2 = pl.figure()
    fig2.clf()
    ax1 = fig2.add_subplot(221)
    ax2 = fig2.add_subplot(222)
    ax3 = fig2.add_subplot(223)
    ax4 = fig2.add_subplot(224)
    
    
    # plot map
    for out in outline.iterrows():
        xy = np.array(out[1].geometry.coords)
        ax1.plot(xy[:,0],xy[:,1],'k')
    for i in ii:
        index = int(one_soil[i,0])
        ax1.plot(location[index].x,location[index].y,'.r')
    ax1.set_title('{}; n = {}'.format(soil, len(ii)))
    
    # plot PFOS v vol and PFOA v vol
    nn = 0
    n_none = 0
    for i in ii:
        index = int(one_soil[i,0])
        if (vol[index] == None) or (np.isnan(vol[index])):
            n_none += 1
            continue
        if one_soil_pfos[i] == None:
            n_none += 1
            continue
        
        if nn == 0:
            ax2.plot(vol[index],one_soil_pfos[i],'.r',label='PFOS')
            ax2.plot(vol[index],one_soil_pfoa[i],'.g',label='PFOA')
            nn = 1
        else:
            ax2.plot(vol[index],one_soil_pfos[i],'.r')
            ax2.plot(vol[index],one_soil_pfoa[i],'.g')
    ax2.legend()
    ax2.set_xlabel('Volume Spread')
    ax2.set_ylabel('PFAS Concentration (ppt)')
    ax2.set_title('no spread data = {}'.format(n_none))
    
    # plot PFOS v YEARS and PFOA v YEARS
    nn = 0
    n_none = 0
    for i in ii:
        index = int(one_soil[i,0])
        if (years[index] == None) or (np.isnan(years[index])):
            n_none += 1
            continue
        if one_soil_pfos[i] == None:
            n_none += 1
            continue
        if nn == 0:
            ax3.plot(years[index],one_soil_pfos[i],'.r',label='PFOS')
            ax3.plot(years[index],one_soil_pfoa[i],'.g',label='PFOA')
            nn = 1
        else:
            ax3.plot(years[index],one_soil_pfos[i],'.r')
            ax3.plot(years[index],one_soil_pfoa[i],'.g')
    ax3.legend()
    ax3.set_xlabel('Years Spread')
    ax3.set_ylabel('PFAS Concentration (ppt)')
    ax3.set_title('no spread data = {}'.format(n_none))
    
    fig2.savefig(base_folder+'/soil_figures/{}.png'.format(soil),dpi=300)
pl.ion()
#%%
# import matplotlib.cm as cm
gradient = pl.get_cmap('viridis') 
colors = gradient(np.linspace(0,1,63))

soil_order = []
for soil in one_soil:
    soil_order.append(soil[1])
soil_order = list(set(soil_order))
source = np.array(source)
one_soil_index = np.array(one_soil)[:,0].astype(int)
for jj,src in enumerate(set(source)): # for each source
    ii = np.nonzero(source == src)[0] # index for all the fields with the given source
    # which one_soil fields are on this list
    indexs =  np.nonzero([item in ii for item in one_soil_index])[0]

    for index in indexs:
        soil = one_soil[index][1]
        x = soil_order.index(soil)
        # all_index = one_soil[index,0]
        if one_soil_pfos[index] == None:
            continue
        pl.plot(x,one_soil_pfos[index],'.',markerfacecolor=colors[jj],markeredgecolor=colors[jj])
    
    # if jj == 10:
    #     break

#%% make tabular with following columns
# feild geom
# most common soil type
# PFOS conctratino
# PFOA concentration 
   
s_tab = gpd.GeoDataFrame()





#%% for each soil get PFOS and PFOA concentrations 
st_pfoa = {}
st_pfos = {}
common_soil_array = np.array(common_soil)
for st in set(common_soil_array):
    I = np.nonzero(common_soil_array == st)
    pfoa = []
    pfos = []
    for ii in I:
        pfoa.append(fields.iloc[ii].PFOA.to_list())
        pfos.append(fields.iloc[ii].PFOS.to_list())
    
    st_pfoa[st] = pfoa[0]
    st_pfos[st] = pfos[0]

#%% convert concetration strings to floats
pfoa = {}
pfos = {}
for key in st_pfoa.keys():
    ps = []
    pa = []
    for con in st_pfoa[key]:
        if con == None:
            pa.append(None)
        elif con.startswith('ND'):
            pa.append(0)
        else:
            pa.append(float(con.split(' ')[0]))
    for con in st_pfos[key]:
        if con == None:
            ps.append(None)
        elif con.startswith('ND'):
            ps.append(0)
        else:
            ps.append(float(con.split(' ')[0]))
    
    pfoa[key] = pa
    pfos[key] = ps
    

#%% plots soil

fig = pl.figure(1)
fig.clf()

xtic = []
for i,key in enumerate(pfos.keys()):
    xtic.append(key)
    for con in pfos[key]:
        if con == None:
            continue
        pl.plot(i,con,'k.')
    
pl.xticks(np.arange(0,len(xtic)),xtic,rotation=-90,fontsize=6)
# soils with greater than 200
# soils with ND
# most common soils 
    # geographic consistency

#%% find most common soils
most_common = []
for key in pfos.keys():
    if len(pfos[key]) > 20:
        most_common.append(key)

#%% plots most common soil

fig = pl.figure(1)
fig.clf()

xtic = []
i = 0
for key in pfos.keys():
    if key in most_common:
        xtic.append('{}({})'.format(key,len(pfos[key])))
        for con in pfos[key]:
            if con == None:
                continue
            pl.plot(i,con,'k.')
        i += 1
        print(i)


pl.xticks(np.arange(0,len(xtic)),xtic,rotation=-90,fontsize=6)


    
    



