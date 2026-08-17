# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 14:32:56 2026

@author: Lucas.Beem

display results of PFAS tests for a given sequence number

"""

import os
os.system("") #makes color work for some reason
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'..','lookup'))

import paths
import argparse
import numpy as np
import geopandas as gpd
import pandas as pd
from pfas_map import layer_compounds as comps


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
        BG_YELLOW = "\033[43m"
        BG_WHITE = "\033[47m"
        BG_CYAN = '\033[46m'

def main(args):
    
    # load rags 
    all_rag = pd.read_excel( paths.compounds_xls )
    rags = all_rag[all_rag.pfas == 1].iloc[:,[0,1,2,3,6]]
    
    comps['HFPO-DA'] = 'HFPO_DA'
    
    if not args.s:
        # display GW results
        data = gpd.read_file(paths.sample_locations)
        data = data[data['EGAD_SITE_'] == args.seq]
        data = data.sort_values(by='FEATURE_NA')
        
        
        
        locations = data.FEATURE_NA.tolist()
        locs = ''
        for loc in locations:
            locs += '{:20}'.format(loc)
        
        print('')
        print( Color.BG_WHITE + Color.BLACK+'EXCEEDS EPA MCL' + Color.RESET )
        print(Color.BG_CYAN + Color.BLACK + 'EXCEEDS RAG / Interim Standard'+ Color.RESET )
        print('-   : Non-Detect')
        print('-r- : Not in Data')
        print('{:30}{}'.format('',locs))
        
        for p in rags.compound: # compound list 
            cons = ''
            rag = rags[rags.compound == p].rag_gw.tolist()[0]
            if rag == '-':
                rag = np.nan
            MCL = rags[rags.compound == p].EPA_MCL.tolist()[0]
            if MCL == '-':
                MCL = np.nan

            con =  data[comps[p]].to_list()
            
            for c in con:
                
                if c is None:
                    cons += '{:20}'.format('-r-')
                elif c.startswith('ND'):
                    cons +='{:20}'.format('-')
                else:
                    result = c.split(' ')[0]
                    
                    if (float(result) > rag) and (float(result) > MCL) : #exceeds both which basically will never happen due to the high magnitude of rag
                        cons += Color.CYAN +'{:34}'.format(Color.BG_WHITE + Color.BLACK + result + Color.RESET ) 
                    elif (float(result) > rag) and not (float(result) > MCL):   # exceed only rag / intermim
                        cons +=  '{:34}'.format(Color.BG_CYAN + Color.BLACK + result + Color.RESET )
                    elif (float(result) < rag) and (float(result) > MCL):   #exceed only MCL
                        cons +=  '{:34}'.format(Color.BG_WHITE + Color.BLACK + result + Color.RESET ) # extra width (34) because of the charactesre in color code
                    else:
                        cons += '{:20}'.format(result)
            
            print('{:30}{}'.format(p,cons))
        print( '')
        

    
    
    if args.s:
        # display soil results
        data = gpd.read_file(paths.soil_polygons)
        data = data[data['EGAD_SITE_'] == args.seq]
        data = data.sort_values(by='FEATURE_NA')
        
        if len(data) == 0:
            print ('\nNo soil data for {}\n'.format(args.seq))
            exit()
           
        locations = data.FEATURE_NA.tolist()
        locs = ''
        for loc in locations:
            locs += '{:20}'.format(loc)
            
        print('')
        print( Color.BG_WHITE + Color.BLACK+'EXCEEDS both LTG and Residential' + Color.RESET )
        print( Color.BG_CYAN + Color.BLACK + 'EXCEEDS only LTG'+ Color.RESET )
        print('-   : Non-Detect')
        print('-r- : Not in Data')
        print('{:30}{}'.format('',locs))

        for p in rags.compound: # compound list 
            if p == 'Sum of 6':
                continue
            cons = ''
            ltg = rags[rags.compound == p].soil_leach.tolist()[0]
            if ltg == '-':
                ltg = np.nan
            resd = rags[rags.compound == p].soil_resd.tolist()[0]
            if resd == '-':
                resd = np.nan

            con =  data[comps[p]].to_list()
            
            for c in con:
                if c is None:
                    cons += '{:20}'.format('-r-')
                elif c.startswith('ND'):
                    cons +='{:20}'.format('-')
                else:
                    result = c.split(' ')[0]
                    
                    if (float(result) > ltg) and (float(result) > resd) : #exceeds both 
                        cons += '{:34}'.format( Color.BG_WHITE + Color.BLACK + result + Color.RESET ) # extra width (34) because of the charactesre in color code
                    elif (float(result) > ltg) and not (float(result) > resd):   # exceed only ltg
                        cons +=  '{:34}'.format( Color.BG_CYAN + Color.BLACK + result + Color.RESET )
                    else:
                        cons += '{:20}'.format(result)
            print('{:30}{}'.format(p,cons))
        print( '')


if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('seq' ,type=int, help='Sequence number of site')
    parser.add_argument('-s' , action = 'store_true', help='flag to display soil results')

    args = parser.parse_args()
    main(args)