# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 10:16:48 2026

@author: Lucas.Beem
"""


import geopandas as gpd
import pandas as pd
import numpy as np
import argparse

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'..','lookup'))
# sys.path.append(base_folder)

import paths


def make_site_table(path,output):
    #this code generates a site_table.py file.  When site_table.py is run it will 
    # generate a dataframe tha associates sequence numbers with site names so
    # sitename can be converted to sequence numbers and vice versa.
    
    # path : path to sample location geo-package
    # output : filename for .py file (use .py in name)
    
    df = gpd.read_file(path)
    outfile = base_folder + '/../lookup/' + output
    sites = np.unique(df.SITE_NAME.values.tolist())
    
    seqs = []
    for site in sites:
        seqs.append( df[df['SITE_NAME'] == site]['EGAD_SITE_'].iloc[0] )
    
    with open(outfile, "w") as file :
        file.write('# look up table for PFAS compresheive\n')
        file.write('import pandas as pd\n\n')
        file.write('def table():\n')
        file.write('    data = {\n')
        file.write("    'site' : [")
        for site in sites:
            file.write("'{}',".format(site))
        file.write('],\n')
        file.write("    'seq' : [")
        for seq in seqs:
            file.write("{},".format(seq))
        file.write(']\n')
        file.write('    }\n')
        file.write('    df = pd.DataFrame(data)\n')
        file.write('    return df')

def make_field_distance_pd(path,output):
    # determines the distance between every feild 
    # path : path and filename of fields geopackage
    # output : path and filename of outpuot geopackage 
    
    
    # load in fields geopackage
    fields = gpd.read_file(path)
    
    # make distance array
    dist = np.ones((  len(fields), len(fields) )) * -1
    
    
    for i,field in enumerate(fields.itertuples()):
        for j in range(i+1,len(fields)):
            dist[i,j] = field.geometry.geoms[0].distance(fields.loc[j].geometry.geoms[0])
    
    df = pd.DataFrame(data=dist,index= fields[['FEATURE_NA','EGAD_SITE_']], columns = fields[['FEATURE_NA','EGAD_SITE_']])
    df.to_pickle(output)

def make_sample_distance_pd(fld_path,samp_path,output):
    # determine distance from every sample to every field
    # fld_path : path to filed geopackage
    # samp_path : path to sample geopackage
    # output : path and filename for output pickle
    

    # load in fields geopackage
    fields = gpd.read_file(fld_path)
    
    # load in sample locations
    samp = gpd.read_file(samp_path)
    locations = samp.loc[:,'geometry'] # these are shapely points
    
    # make distance array
    dist = np.ones((  len(fields), len(locations) )) * -1
    
    for i,field in enumerate(fields.itertuples()):
        for j,pt in enumerate(locations):
            
            dist[i,j] = field.geometry.geoms[0].distance(pt)
 
    df = pd.DataFrame(data=dist,index = fields['FEATURE_NA'], columns = samp['FEATURE_NA'])
    df.to_pickle(output)  
        
def main(args):
     
    if args.d:
        #generate distance files
        if os.path.isfile(paths.fields):
            print('generating field to field distance table')
            make_field_distance_pd(paths.fields,paths.field_distance)
            
            if os.path.isfile(paths.sample_locations):
                print('generating field to LD1600 sample distances')
                make_sample_distance_pd(paths.fields,paths.sample_locations,paths.sample_distance) # the distance of every sample to every field 
                   
            else:
                print('LD1600 groundwater results geopackage not found: distances not generated')
            
            if os.path.isfile(paths.nonLD_gw):
                print('generating field to Non-LD1600 sample distances')
                make_sample_distance_pd(paths.fields,paths.nonLD_gw,paths.nonLD_distance) # the distance of every sample to every field 
                
            else:
                print('Non-LD1600 groundwater results geopackage not found: distances not generated')
        else:
            print('Field geopackage not found: no distances can be generated')
    
    # make lookup tables
    if os.path.isfile(paths.sample_locations):
        print('generating site table for LD1600 results')
        make_site_table(paths.sample_locations,'LD_site_table.py')
    else:
        print('LD1600 groundwater results geopackage not found: site table not generated')
    
    if os.path.isfile(paths.nonLD_gw):
        print('generating site table for nonLD1600 results')
        make_site_table(paths.nonLD_gw,'nonLD_site_table.py')
    else:
        print('Non-LD1600 groundwater results geopackage not found:site table not generated')

if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('-d', action ='store_true', help='enable distance table calculation')
    # parser.add_argument('-t', action ='store_true', help='enable site table generation')

    args = parser.parse_args()
   

    # if not args.d and not args.t:
    #     print('at least one flag needs to be provided (-d or -t)')
    #     exit()
        
    main(args)