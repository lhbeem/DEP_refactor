# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 11:12:19 2026

@author: Lucas.Beem
"""

import os
import argparse


def make_pfas_notes(args,folder_path):
    headers = ['Surface waters','Topo','Surficial Geology','Bedrock Geology','Soils','Overburden']
    
    filename = folder_path +'/notes.txt'
    if not os.path.exists(filename):
        with open(filename,'w') as f:
            f.write(args.name.title() + '\n\n\n\n\n')
            for header in headers:
                f.write('{}\n\n\n\n'.format(header))
    else:
        print('\nNote file already exists in {}'.format(folder_path))
    

def main(args):
    
    site_folder = 'C:/Users/Lucas.Beem/OneDrive - State of Maine/Documents/sites'
    
    if args.type == 'brown':
        type_folder = 'brownfields'
    elif args.type == 'landfill':
        type_folder = 'landfills'
    elif args.type == 'pfas':
        type_folder = 'pfas'
    elif args.type == 'spill':
        type_folder = 'spills'
    elif args.type == 'vrap':
        type_folder = 'vrap'
    
    folder_path = '{}/{}/{}'.format(site_folder, type_folder , args.name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    if args.type == 'pfas':
        make_pfas_notes(args,folder_path)
    
    
    print ('\n'+folder_path)
    print('')
    os.startfile(folder_path)

if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('name' ,help='Name of folder')
    parser.add_argument('type' ,choices=['pfas','spill','vrap','brown','landfill'], help='Type of site')

    args = parser.parse_args()
    main(args)