# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 14:33:47 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'..','utils'))
import all_egad_table

import argparse
import glob 

def main(args):
    # find a site that matches the keyword and get town and site type
    
    table = all_egad_table.table()

    if args.siteID.isdecimal():
        # assume is a sequence number
        row = table[table.seq == int(args.siteID)]
        if len(row) == 0:
            print('\nsequence number not found in table: {}\n'.format(args.siteID))
            exit()
        else:
            keys = row.site.to_list()[0].split(' ')
            town = row.town.tolist()[0]
            site_type = row.type.tolist()[0]
    else:
        sites = []
        for tab in table.iterrows():
            if args.siteID.upper() in tab[1].site:
                sites.append([tab[1].site,tab[1].seq,tab[1].town,tab[1].type])
        if len(sites) == 1:
            keys = sites[0,0].split(' ')
            town = sites[0][2]
            site_type = sites[0][3]
        elif len(sites) == 0:
            print('No sites found with search term: {}'.format(args.siteID))
            exit()
        else:
            print('multiple sites found, try to refine')
            for s in sites:
                print(s)
    # search for the keyword in folder names 
    
    
    if 'sludge' in site_type.lower():
        base = 'H:/BRWM/PFAS - LD 1600/Sites'
        folder_path = '{}/{}/'.format(base,town.title())
        folders = glob.glob(folder_path+'*')
        for key in keys:
            folds = []
            for folder in folders:
                if key.lower() in folder.lower():
                    folds.append(folder)
            if len(folds) == 1:
                break
        
        folds = list(set(folds))
        if len(folds) == 1:
            os.system('start "" "{}"'.format(folds[0]))
        elif len(folds) == 0:
            print('no folders matched key words: {}'.format(keys))
            print(folder_path)
        else:
            print('More than one folder found')
            
            
    elif 'leaking' in site_type:
        folder_path = r'H:\BRWM\BRWM Databases\FILE ROOM\TechServSpillClosure\SMRO'
        
        # next folder starts with town name is the desired folder
        
    elif 'landfill' in site_type:
        base = r'H:\BRWM\Remediation Division\Sites'

        folder_path = '{}/{}/'.format(base,town)
        
    return
    



if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('siteID' ,help='help')

    args = parser.parse_args()
    main(args)