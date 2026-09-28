# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 14:56:04 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'lookup'))

import paths
import argparse
import numpy as np
import shapely
import geopandas as gpd


def main(args):
    pt = shapely.Point([args.x,args.y])
    gdf_point = gpd.GeoDataFrame(geometry=[pt], crs="EPSG:26919")
    ROI = gdf_point.total_bounds + [-1,-1,1,1] 
    x = [ROI[0] , ROI[0] , ROI[2] , ROI[2] , ROI[0]]
    y = [ROI[1] , ROI[3] , ROI[3] , ROI[1] , ROI[1]]
    ROI = np.array(np.vstack((x,y))).T
    ROI = shapely.Polygon(ROI)
    town = gpd.read_file(paths.towns, mask= ROI)
    
    print('')
    print('{}'.format(town.TOWN.tolist()[0]))
    print('')

    



if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('x',type=float, help='x coordinate EPSG:26919')
    parser.add_argument('y',type=float, help='y coordinate EPSG:26919')

    args = parser.parse_args()
    main(args)