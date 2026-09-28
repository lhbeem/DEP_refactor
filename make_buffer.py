# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 13:50:35 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'lookup'))

import paths
import argparse
# import numpy as np
import geopandas as gpd


def main(args):
    
    fields = gpd.read_file(paths.fields)
    
    field = fields[fields.EGAD_SITE_ == args.seq].iloc[0]
    
    field_geom = field.geometry.geoms[0]
    # print(field.geometry.geoms[0])
    
    
    buffer = field_geom.buffer(args.d, join_style='round', cap_style='round', quad_segs=16)
    # print(buffer)
    gdf = gpd.GeoDataFrame(geometry=[buffer], crs="EPSG:26919")
    
    gdf.to_file(paths.data+"/buffer/buffer.gpkg", layer="{} buffer".format(args.d), driver="GPKG")
    
    return
    



if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('-file' , help='path to center file')
    parser.add_argument('-seq'  , type=int, help='sequnece number to use with paths.feilds')
    parser.add_argument('-d'    , type=float, help='distance; 0.1 mile = 161 m and 0.25mi = 402m')

    args = parser.parse_args()
    main(args)