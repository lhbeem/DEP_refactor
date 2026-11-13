# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 08:18:46 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'../../lookup'))

import paths
import argparse
# import numpy as np
import pandas as pd
import geopandas as gpd


def main(args):
    data = pd.read_pickle(base_folder + '/all_pfas.pkl')
    
    if args.rag:
        print('todo: implement rag functionality')

    else: # display dates and locations
        sub = data[data.EGAD_SITE_ == int(args.site)]
        if args.s:
            sub = sub.sort_values(by='FEATURE_NA')
        else:
            sub = sub.sort_values(by='SAMPLE_DAT')
        
        # get egad name
        df = gpd.read_file( paths.egad_sites )
        row = df[df.MEDEP_Site == int(args.site)]
        name = row.MEDEP_S_19.iloc[0]
        
        print('')
        print('Site: {} , {}\n'.format(args.site,name))
        for row in sub.iterrows():
            row = row[1]
            # print(row)
            print('{:20}{}'.format(row.SAMPLE_DAT.strftime('%Y-%m-%d'),row.FEATURE_NA))
        print('')

    return
    



if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('site' ,help='Sequence number, default displays date and locations')
    parser.add_argument('-s' , action='store_true', help='sort by location')
    parser.add_argument('-rag' , action='store_true', help='Display sample results compared to rags')

    args = parser.parse_args()
    main(args)