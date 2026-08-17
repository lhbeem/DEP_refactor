# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 13:24:49 2026

@author: Lucas.Beem
"""

import sys
import os
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'lookup'))
sys.path.append(base_folder)

import geo_utils
import argparse




def main(args):
    geo_utils.find_site_point(args.seq)
    geo_utils.find_site_locations(args.seq)
    geo_utils.find_polygon(args.seq)
    geo_utils.find_soil_polygon(args.seq)
    return
    



if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('seq', type = int,help='site sequence number')

    args = parser.parse_args()
    main(args)