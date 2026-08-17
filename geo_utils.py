# -*- coding: utf-8 -*-
"""
Created on Thu May 21 15:28:16 2026

@author: Lucas.Beem
"""
import sys
import os
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'lookup'))

import shapely
import geopandas as gpd
import numpy as np
import paths
import pyproj 

def pt2town(x,y):
    pt = shapely.Point([x,y])
    gdf_point = gpd.GeoDataFrame(geometry=[pt], crs="EPSG:26919")
    ROI = gdf_point.total_bounds + [-1,-1,1,1] 
    x = [ROI[0] , ROI[0] , ROI[2] , ROI[2] , ROI[0]]
    y = [ROI[1] , ROI[3] , ROI[3] , ROI[1] , ROI[1]]
    ROI = np.array(np.vstack((x,y))).T
    ROI = shapely.Polygon(ROI)
    town = gpd.read_file(paths.towns, mask= ROI)
    
    return town.TOWN.tolist()[0]

def shp2gpkg(path,out=None):
    # convert individual shapefile to geopackage
    # path to the shapefile
    # output is path and file name, if None saves to same folder as shapefile
    gdf = gpd.read_file(path)
    if out == None:
        outpath = '.'.join(path.split('.')[:-1]) + '.gpkg'
    else:
        outpath = out
        
    gdf.to_file(outpath, driver="GPKG")
    
    
def pt2zip(x,y):
    pt = shapely.Point([x,y])
    gdf_point = gpd.GeoDataFrame(geometry=[pt], crs="EPSG:26919")
    ROI = gdf_point.total_bounds + [-1,-1,1,1] 
    x = [ROI[0] , ROI[0] , ROI[2] , ROI[2] , ROI[0]]
    y = [ROI[1] , ROI[3] , ROI[3] , ROI[1] , ROI[1]]
    ROI = np.array(np.vstack((x,y))).T
    ROI = shapely.Polygon(ROI)
    zips = gpd.read_file(paths.zips, mask= ROI)
    
    return zips.NAME20.tolist()[0]


def find_site_point(seq):
    # check for the existance of a site point
    all_sites = gpd.read_file(paths.egad_sites)
    
    # pt = all_sites[all_sites['GISVIEW_ME'] == seq]
    pt = all_sites[all_sites['MEDEP_Site'] == seq] # change of columns names in gpkg
    if len(pt) == 1:
        print('\n{} {} {}\n'.format( pt['MEDEP_S_19'].to_list()[0] , int(float(pt['MEDEP_Si_6'].to_list()[0])),int(float(pt['MEDEP_Si_7'].to_list()[0]))))
        return [pt['MEDEP_Si_6'].to_list()[0],pt['MEDEP_Si_7'].to_list()[0]]
    
    elif len(pt) > 1:
        print('\nMultiple points found, non unique sequence number\n')
        print(pt)
    else:
        print('\nNo site point found for {}\n'.format(seq))
        
def find_site_locations(seq):
    # list the sample location points for a given sequence number
    locations = gpd.read_file(paths.egad_samples)
    
    locs = locations[locations.EGAD_SITE_ == seq]
    if len(locs) == 0:
        print('\nNo Locations found for {}\n'.format(seq))
    else:
        if len(locs) > 1:
            plural = 's'
        else:
            plural = ''
        print('\nThere are {} location{}'.format(len(locs),plural))
        for loc in locs.iterrows():
            loc = loc[1]
            print('{:40} {:10} {:10}'.format(loc.FEATURE_NA,int(loc.X),int(loc.Y)))
  
def get_quad(x,y):
    # get quandrangle name for a point
    pt = shapely.Point([x,y])
    gdf_point = gpd.GeoDataFrame(geometry=[pt], crs="EPSG:26919")
    ROI = gdf_point.total_bounds + [-1,-1,1,1] 
    x = [ROI[0] , ROI[0] , ROI[2] , ROI[2] , ROI[0]]
    y = [ROI[1] , ROI[3] , ROI[3] , ROI[1] , ROI[1]]
    ROI = np.array(np.vstack((x,y))).T
    ROI = shapely.Polygon(ROI)
    quad = gpd.read_file(paths.quadrangle, mask= ROI)
    
    if len(quad) != 1:
        status = 0
    else:
        status = 1
    
    return quad.NAME.tolist()[0] , status
 

def get_surficial(x,y):
    # get surficial name and description  for a point
    pt = shapely.Point([x,y])
    gdf_point = gpd.GeoDataFrame(geometry=[pt], crs="EPSG:26919")
    ROI = gdf_point.total_bounds + [-1,-1,1,1] 
    x = [ROI[0] , ROI[0] , ROI[2] , ROI[2] , ROI[0]]
    y = [ROI[1] , ROI[3] , ROI[3] , ROI[1] , ROI[1]]
    ROI = np.array(np.vstack((x,y))).T
    ROI = shapely.Polygon(ROI)
    unit = gpd.read_file(paths.surficial, layer = 'Maine_Surficial_Geology_Units', mask= ROI)
    
    if len(unit) == 1:
        status = 1
    else:
        status = 0
    
    return unit.UNIT.tolist()[0] , unit.Explanatio.tolist()[0] , status

def get_bedrock(x,y):
    # get bedrock name and description  for a point
    pt = shapely.Point([x,y])
    gdf_point = gpd.GeoDataFrame(geometry=[pt], crs="EPSG:26919")
    ROI = gdf_point.total_bounds + [-1,-1,1,1] 
    x = [ROI[0] , ROI[0] , ROI[2] , ROI[2] , ROI[0]]
    y = [ROI[1] , ROI[3] , ROI[3] , ROI[1] , ROI[1]]
    ROI = np.array(np.vstack((x,y))).T
    ROI = shapely.Polygon(ROI)
    unit = gpd.read_file(paths.bedrock, layer = 'Maine_Bedrock_Geology_500K_Units', mask= ROI)
    
    if len(unit) == 1:
        status = 1
    else:
        status = 0
    
    return unit.UNIT.tolist()[0] , unit.SIMPLIFIED.tolist()[0] , status

           
def find_polygon(seq):
    # if site is PFAS site, a polygon should exist.
    fields = gpd.read_file(paths.fields)
    field = fields[fields.EGAD_SITE_ == seq]
    if len(field) == 0:
        print('\nNo feild polygon found for {}\n'.format(seq))
    else:
        if len(field) > 1:
            plural = 's'
        else:
            plural = ''
        print('\nThere are {} feilds polygon{}'.format(len(field),plural))
        for field in field.iterrows():
            field = field[1]
            print('{:40}'.format(field.FEATURE_NA,))

def find_soil_polygon(seq):
    # if pfas soils exist there should be a polygon
    fields = gpd.read_file(paths.soil_polygons)
    field = fields[fields.EGAD_SITE_ == seq]
    if len(field) == 0:
        print('\nNo soil polygons found for {}\n'.format(seq))
    else:
        if len(field) > 1:
            plural = 's'
        else:
            plural = ''
        print('\nThere are {} soil sample polygon{}'.format(len(field),plural))
        for field in field.iterrows():
            field = field[1]
            print('{:40}'.format(field.FEATURE_NA,))           
            
            
            
def get_soil( x, y, d=100 ):
    # get soils from a point (x,y)
    # d is a distance (m) from the point to include 
    
    # soil is in EPSG:5070
    P = pyproj.Transformer.from_crs("EPSG:26919", "EPSG:5070", always_xy=True)
    x,y = P.transform(x,y)
    
    roi_x = [x+d, x+d, x-d, x-d, x+d]
    roi_y = [y+d, y-d, y-d, y+d, y+d]
    ROI = np.array(np.vstack((roi_x,roi_y))).T
    ROI = shapely.Polygon( ROI )
    soil = gpd.read_file(paths.soil, mask=ROI)
    
    return soil
    
    