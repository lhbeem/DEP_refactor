# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 14:25:39 2025

@author: Lucas.Beem


example call from powershell: g2N19 g "44°16'47.4`"N 69°49'52.0`"W"
or delete double quotes
g2N19 g "44°16'47.4N 69°49'52.0W"

"""





import argparse
import pyproj



def main(args):
    P = pyproj.Proj('EPSG:26919')
    
    
    
    lat = float(args.arg1)
    lon = float(args.arg2)
    if lon > 0:
        lon *= -1
    
    if args.i:
        lon, lat =  P(args.arg1,args.arg2, inverse=True)
        print('')
        print(lat,lon)
        print('')
    else:
        x , y = P(lon,lat)
        
        print(lat,lon)
        print(round(x),round(y))
        print(round(x,2),round(y,2))
        return [x,y]
    
if __name__=="__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument('arg1' , help='decimal Latitude or utm_x if using -i flag')
    parser.add_argument('arg2' , help='decimal longitude or utm_y if using -i flag')
    parser.add_argument('-i' , action='store_true', help='Inverse to ')
    args = parser.parse_args()
    main(args)




