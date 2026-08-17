# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 10:16:48 2026

@author: Lucas.Beem
"""


import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(base_folder)

import geo_utils
import glob
import paths
import pathlib


def main():
    
    # convert shapefile to geopackage and move to C drive
    # the expectation is that the licensd fields and groundwater results shapefiles are in G:/brwm/Lucas.Beem
    
    
    shps = glob.glob('G:/brwm/Lucas_Beem/*.shp')
    for shp in shps:
        name = pathlib.Path(shp).stem
        out = paths.data + '/geo_files/{}.gpkg'.format(name)
        geo_utils.shp2gpkg(shp,out)
        print('saved: {}'.format(out))
    
   
    
    
    
    
if __name__=="__main__":
    main()