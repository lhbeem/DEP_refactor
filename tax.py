# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 13:33:02 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(base_folder)
sys.path.append(os.path.join(base_folder,'lookup'))

import shapely
import pyproj
import paths
import argparse
import numpy as np
import geopandas as gpd
import geo_utils 


def get_mailing(town,m,l):
    tax = {'acton' : 'https://www.actonmaine.org/wp-content/uploads/2025/09/2025_Town-of-Acton_Tax_Archive_381793.pdf',
           'durham' : 'https://durhammaine.gov/uploads/real-estate-commitment-book-2026.pdf',
           'kittery': None, # kittery has an online form to search, can't find a compiled pdf
           }
    mailing= tax
    return mailing


def get_maplot_from_address(args):
    parcel = gpd.read_file(paths.tax)
    parcel = parcel[parcel['PROP_LOC'] == args.pt[0].upper()]
    town = parcel['TOWN'][0]
    maplot = parcel['MAP_BK_LOT'][0]
    address = parcel['PROP_LOC'][0]
    
    print(town)
    print(maplot)
    print(address)
  
def get_ml(town,maplot):
    if town.lower() in ['windham','lisbon','harpswell']:
        #mmmlll#######
        m = maplot[:3]
        l = maplot[3:6]
        
    elif town.lower() in ['freeport']:
        #m/l/a/#
        mm = maplot.split('/')
        m = mm[0]
        l = mm[1]
        if mm[2] != 0:
            l += mm[2]
    elif town.lower() in ['biddeford','dayton','eliot','gorham','pownal','standish','topsham','west paris','poland']:
        # m-l
        mm = maplot.split('-')
        m = mm[0]
        l = mm[1]
    elif town.lower() in ['falmouth']:
        # m-l-a
        mm = maplot.split('-')
        m = mm[0]
        l = mm[1]+ mm[2]
    elif town.lower() in ['durham','brunswick']:
        # unknown
        m = maplot
        l = maplot
    else:
        m = maplot
        l = maplot
    return m,l


def main(args):

    if args.a:    
        print('Using Address')
        get_maplot_from_address(args)
        exit() 
    
    if len(args.pt) == 1:
        print('Using sequence number')
        point = geo_utils.find_site_point(args.pt[0])
        print(point)
    elif len(args.pt) == 2:
        args.pt = [float(args.pt[0]) , float(args.pt[1])]
        if args.pt[0] < 100:
            print('Using lat lon pair')
            P = pyproj.Proj('EPSG:26919')
            point = P(args.pt[1],args.pt[0])
            
        else:  
            print('Using utm coorindate pair')
            point = [args.pt[0], args.pt[1]]
    else:
        print('number of args is no one or two')
        exit()
        
        
    pt = shapely.Point(point)
    gdf_point = gpd.GeoDataFrame(geometry=[pt], crs="EPSG:26919")
    ROI = gdf_point.total_bounds + [-1,-1,1,1] 
    x = [ROI[0] , ROI[0] , ROI[2] , ROI[2] , ROI[0]]
    y = [ROI[1] , ROI[3] , ROI[3] , ROI[1] , ROI[1]]
    ROI = np.array(np.vstack((x,y))).T
    ROI = shapely.Polygon(ROI)
    parcel = gpd.read_file(paths.tax, mask= ROI)
    
    town = parcel['TOWN'][0]
    maplot = parcel['MAP_BK_LOT'][0]
    address = parcel['PROP_LOC'][0]
    
    print('')
    print('Town:    {}'.format(town))
    print('Address: {}'.format(address))
    
    
    m,l = get_ml(town,maplot)
    
    print('map:     {}'.format(m))
    print('lot:     {}'.format(l))
    print('')    

    
    return


if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('pt', nargs ='*', help='a utm coordiante pair')
    parser.add_argument('-a', action='store_true', help='use flag to indicate that an address is supplied as the required argument. Address serach takes longer')

    args = parser.parse_args()
    main(args)