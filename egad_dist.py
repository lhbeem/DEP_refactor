# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 08:05:26 2026

@author: Lucas.Beem

return sites within a given distance of a point

"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'lookup'))
# import parse_utils
import paths
# import all_egad_table

import argparse
import numpy as np
import geopandas as gpd
import shapely





def get_pt_from_seq(seq):
    sites = gpd.read_file(paths.egad_sites)
    site = sites[sites.GISVIEW_ME == seq]
    if len(site) == 0:
        print('Sequence number not found: {}'.format(args.site))
        exit()
    x = site.geometry.x.tolist()[0]
    y = site.geometry.y.tolist()[0]

    name = site.MEDEP_S_19.to_list()[0]
    return  x,y,name

def main(args):
    
    # parse arg.site and get UTM x,y coordinates
    if ',' in args.site:
        #assume coordiantes
        if len(args.site.split(',')) != 2:
            print('coordinates do not match expectation')
            print('single pair comma delimited, passed to argparse as a string in quotes')
            print('{}'.format(args.site))
            exit()
        
        x = float(args.site.split(',')[0])
        y = float(args.site.split(',')[1])
        print('using point\nx: {}\n y:{}'.format(x,y))
        name = 'Supplied Point'
    
    elif args.site.isdecimal():
        #assume sequence number
        x,y,name = get_pt_from_seq(int(args.site))
    else:
        # assume string to search egad names
        # table = all_egad_table.table()
        table = []
        out = []
        for tab in table.iterrows():
            if args.site.upper() in tab[1].site:
                out.append ( [tab[1].site,tab[1].seq,tab[1].type] )
        if out == 0:
            print('site not found, check site spelling')
            exit()
        elif len(out)> 1:
            print('multiple sites found by search, refine and try again')
            for o in out:
                print('{:40}{}'.format(o[0],o[1]))
            exit()
        else:
            x,y,name = get_pt_from_seq(out[0][1])
            if (x==0) and (y==0):
                print('no site point associated with site')
                print('lat=0,lon=0')
                exit()
        
    # open geopackage with ROI
    ROI_x = [x -args.dist , x + args.dist]
    ROI_y = [y -args.dist , y + args.dist]
    
    x = [ROI_x[0] , ROI_x[0] , ROI_x[1] , ROI_x[1] , ROI_x[0]]
    y = [ROI_y[0] , ROI_y[1] , ROI_y[1] , ROI_y[0] , ROI_y[0]]
    ROI = np.array(np.vstack((x,y))).T
    ROI = shapely.Polygon( ROI )
    sites = gpd.read_file(paths.egad_sites, mask = ROI)
    
    if len(sites) == 0:
        print('\nThere are no sites witin {} meters of {}\n'.format(int(args.dist),name))
    else:
        print('\nThere are {} sites are within {} meters of {}:\n'.format(len(sites),int(args.dist),name))
        for s in sites.iterrows():
            print('{:35} {}'.format(s[1].MEDEP_S_19,int(s[1].MEDEP_Site)))
        print('')


if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('site',  help='siteID (seq, or string to search for), or list of one UTM x and y pair (comma delimited and in quotes')
    parser.add_argument('dist', nargs='?', type= float, default = 400, help='distance in meters')

    args = parser.parse_args()
    main(args)