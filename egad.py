# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 20:50:17 2026

@author: Lucas.Beem
"""

import sys
import os
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'lookup'))

os.system("") #makes color work for some reason
import paths
import argparse
import numpy as np
import geopandas as gpd

class Color:
        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        WHITE = '\033[37m'
        RESET = '\033[0m'  # Resets all formatting (color, bold, etc.)
        


def get_type(seq,df=None):
    if df is None:
        df = gpd.read_file( paths.egad_type )
    
    typ = df[df.EGAD_SEQ == seq].SITE_TYPE
    
    if len(typ) > 0:
        return typ.iloc[0]
    else:
        return 'None'
    
def get_desc(seq,df=None):
    if df is None:
        df = gpd.read_file( paths.egad_type )
    
    
    desc = df[df.EGAD_SEQ == seq].SITE_DESCR.iloc[0]
    narr = df[df.EGAD_SEQ == seq].NARATIVE_S.iloc[0]
    
    if len(desc) == 0:
        desc = 'None'
    if len(narr) == 0:
        narr = 'None'

    return desc, narr
    

def get_site_point(seq):
    # check for the existance of a site point
    all_sites = gpd.read_file(paths.egad_sites)

    pt = all_sites[all_sites['MEDEP_Site'] == seq]
    
    if len(pt) == 1:
        print('\n{} {} {}\n'.format( pt['MEDEP_S_19'].to_list()[0] , int(float(pt['MEDEP_Si_6'].to_list()[0])),int(float(pt['MEDEP_Si_7'].to_list()[0]))))
        return [pt['MEDEP_Si_6'].to_list()[0],pt['MEDEP_Si_7'].to_list()[0]]
    
    else:
        return None



def main(args):
    df = gpd.read_file( paths.egad_sites ) 
    
    if args.siteID.isdecimal():
        # assume to be sequence number
        seq = int(args.siteID)
        row = df[df.MEDEP_Site == seq]
        if len(row) == 0:
            print ('\nsequence number not found in geopackage: {}\n'.format(args.siteID) )
        else:
            name = row.MEDEP_S_19.iloc[0]
            seq  = row.MEDEP_Site.iloc[0]
            address = row.MEDEP_S_20.iloc[0]
            town = row.MEDEP_S_21.iloc[0]
            state = row.MEDEP_S_23.iloc[0]
            typ = get_type(seq)
            print('')
            print('{:50} {}{:8}{} {:30} {}, {}, {}'.format(name,Color.GREEN,seq, Color.RESET,typ, address, town, state ))
            print('')
        if args.d:
            desc,narr = get_desc(seq)
            print(desc)
            print('')
            print(narr)
            
    else:
        # presume a string
        typ_df = gpd.read_file( paths.egad_type )
        search = args.siteID.upper()
        if args.s is None:
            search2 = None
        else:
            search2 = args.s.upper()
        print('')
        for names in df.MEDEP_S_19:
            if names is None:
                continue
            if search in names:
                row = df[df.MEDEP_S_19 == names]
                name = row.MEDEP_S_19.iloc[0]
                seq  = row.MEDEP_Site.iloc[0]
                address = row.MEDEP_S_20.iloc[0]
                town = row.MEDEP_S_21.iloc[0]
                state = row.MEDEP_S_23.iloc[0]
                typ = get_type(seq,typ_df)
                
                if search2 is not None:
                    if np.any( [True for item in [name,address,town,state,typ] if search2 in item] ):
                        print('{:40} {}{:8}{} {:45} {}, {}, {}'.format(name,Color.GREEN,seq, Color.RESET,typ, address, town, state ))
                else:
                    print('{:40} {}{:8}{} {:45} {}, {}, {}'.format(name,Color.GREEN,seq, Color.RESET,typ, address, town, state ))
        
        print('')
        
            

if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('siteID' ,  help='SiteID or search string')
    parser.add_argument('-d' , action='store_true',  help='print site description if present, only is sequence number provided')
    parser.add_argument('-s', help='secondary search term')
    args = parser.parse_args()
    main(args)