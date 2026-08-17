# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 12:09:48 2026

@author: Lucas.Beem
Site background info

fields used in EGAD Site_info tab
fields used in PFAS site eval

"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'lookup'))
import geo_utils

import argparse
import subprocess

def main(args):
    
    # get site point 
    x,y = geo_utils.find_site_point(args.seq)
    
    if x is None:
        print ('site point not found for {}'.format(args.seq))
        exit()
    
    # print town
    town = geo_utils.pt2town(x, y)
    print('Town: {}'.format(town))
    print('')
    
    # print quadrangle name
    quad, status = geo_utils.get_quad(x,y)
    if status == 0:
        print('Not only 1 quadrangle returned')
        print('')
    else:
        print('Quadrangle: {}'.format(quad))
        print('')
    
    # print surficial geology 
    unit, description, status = geo_utils.get_surficial(x,y)
    if status == 0:
        print('Not only 1 surficial unit returned')
        print('')
    else:
        print('SURFICIAL GEOLOGY')
        print('Unit: {}'.format(unit))
        print('Description:\n{}'.format(description))
        print('')
    
    
    # print bedrock 
    unit, description, status = geo_utils.get_bedrock(x,y)
    if status == 0:
        print('Not only 1 surficial unit returned')
        print('')
    else:
        print('BEDROCK GEOLOGY')
        print('Unit: {}'.format(unit))
        print('Description:\n{}'.format(description))
        print('')
        
    # print tax map and lot
    print("TAX LOT")
    cmd = ['python',base_folder+'/tax.py', str(x), str(y) ]
    subprocess.run(cmd, shell=True)
    

    # print soils
    soils_data = geo_utils.get_soil( x, y )
    
    print( "SOILS" )
    symbols = soils_data.MUSYM
    soils = []
    for symbol in symbols:
        soils.append(symbol[:2])
    soils = set(soils)

    for soil in soils:
        print(soil)
        cmd = ['python',base_folder+'/soil_legend.py',soil]
        subprocess.run(cmd, shell=True)
        
        
    return
    



if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('seq' , type = int , help='sequence number of site to run')

    args = parser.parse_args()
    main(args)