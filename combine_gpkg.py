# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 12:17:14 2026

@author: Lucas.Beem
combine all gpkg in a folder
or
combine the supplied gpkg paths
"""

import os
import argparse
import glob
import geopandas as gpd
import pandas as pd

def main(args):
    if len(args.input) == 1:
        print("running as supplied folder")
        gpkgs = []
        for file in glob.glob(os.path.join(args.input[0] ,'*.gpkg' )):
            gdf = gpd.read_file(file) 
            gpkgs.append(gdf)

            combined_gdf = pd.concat(gpkgs, ignore_index=True)

            # Write the unified data to a new GeoPackage
            if args.output == None:
                output_file = os.path.join(args.input[0] , 'combined_gpkg.gpkg')
            else:
                output_file = args.output
        combined_gdf.to_file(output_file, layer="merged_layer", driver="GPKG")
        print('Saved: {}'.format(output_file))
    else:
        print('running as supplied gpkgs files')
        if args.output == None:
            print('output must be supplied when running as supplied gpkg files')
        gpkgs = []
        for file in args.input:
            gdf = gpd.read_file(file) 
            gpkgs.append(gdf)

            output_file = args.output
            combined_gdf.to_file(args.output, layer="merged_layer", driver="GPKG")
            print('Saved: {}'.format(args.output))
        
        
       
    return
    



if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('input', nargs = '+',
                        help='If one argument passed, assumed to be folder all gpkg combined. If multiple arguments assumed each are a gpkg file and will combine')
    parser.add_argument('output', nargs = '?', default = None, help='If not passed, assumes folder of input folder. Must be supplied if listing specific gpkg files')
    args = parser.parse_args()
    main(args)