# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 08:17:08 2026

@author: Lucas.Beem
"""

import argparse
import paths
import pathlib
import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(base_folder)

import geo_utils



def main(args):
    
    name = pathlib.Path(args.shp).stem
    
    out = paths.data + '/geo_files/{}.gpkg'.format(name)
    geo_utils.shp2gpkg(args.shp,out)
    print('saved: {}'.format(out))



if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('shp' ,help='path to shapefile to be converted to geopackage')

    args = parser.parse_args()
    main(args)