# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 16:23:08 2025

@author: Lucas.Beem

works with linux
"""


import argparse
import sys
import os
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'lookup'))
import make_site as utils
import paths


def main(args):
    
    if args.site == 'invoice':
        os.system('start "" "{}"'.format(paths.xRoy))
        exit()
    
    _,df,folders,_ = utils.load_from_pickle(paths.site_pickle)

    
    sitename = utils.shortcut(args.site)
    
    # if utils.in_database(df,sitename) == 0:
    #     print ('\nsite ID ''{}'' not in database\n'.format(args.site))
    #     exit()
    
    
    name = utils.get_id( sitename, 'name') #site name from any ID type
    if name is None:
        print('\n"{}" not found in database. Check spelling\n'.format(sitename))
        exit()

    #get H folder
    folder_present = False
    folder = []
    for fold in folders[name.lower().replace(" ","")]:
        if fold.startswith(args.drive.upper()):
            folder.append( fold )
            folder_present = True
  
    if folder_present:
        if len(folder) > 1:
            print('multiple folders found with {} drive'.format(args.drive))
        for fold in folder:
            os.system('start "" "{}"'.format(fold))
    else:
        print("folder for drive {}: not in lab_track.xls\n".format(args.drive.upper()))



if __name__=="__main__":
    parser= argparse.ArgumentParser()
    # parser.add_argument('cnv_path', help="path to the pace lab cnv file on the H drive, including the file name. Both the cnv and summary pdf need to be in same folder and have the default L### naming convention")
    parser.add_argument('site', help="SiteID (seq, name, or spill#) to open folder")
    parser.add_argument('drive', nargs = '?', default = 'h',choices=['h','c'], help="which drive to open H drive or C drive, case insensitive")
    args = parser.parse_args()



    main(args)
