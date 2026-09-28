# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 14:56:04 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(base_folder)

import geo_utils as utils 
import argparse



def main(args):
    
    
    town = utils.pt2town(args.x,args.y)
    print('')
    print('{}'.format(town))
    print('')
    

if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('x',type=float, help='x coordinate EPSG:26919')
    parser.add_argument('y',type=float, help='y coordinate EPSG:26919')

    args = parser.parse_args()
    main(args)