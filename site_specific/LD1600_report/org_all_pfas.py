# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 11:17:36 2026

@author: Lucas.Beem
"""
import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script

import pandas as pd
import geopandas as gpd
import shapely 
import pyproj

# load "all" EGAD data set
all_pfas_path = r"H:\BRWM\Tech Services Division\LD1600\2026 Legislative Report\20260717_GW_.xlsx"
# data_org = pd.read_excel(all_pfas_path,sheet_name='Data')
data_org = gpd.read_file(all_pfas_path,layer='Data')

P = pyproj.Proj('epsg:26919')

#%%

pfas_columns = {'SUM_OF_6_P': 'SUM OF 6 PFAS (PFHPA + PFHXS + PFOA + PFNA + PFOS + PFDA)',
                'F4_2_FTS': '4:2-FLUOROTELOMER SULFONIC ACID',
                'F6_2_FTS': '6:2 FLUOROTELOMER SULFONIC ACID',
                'F8_2_FTS': '8:2 FLUOROTELOMER SULFONIC ACID',
                'ADONA': '4,8-DIOXA-3H-PERFLUORONONANOIC ACID',
                'HFPO_DA': 'HEXAFLUOROPROPYLENE OXIDE DIMER ACID',
                'N_EtFOSAA': 'N-ETHYL PERFLUOROOCTANE SULFONAMIDOACETIC ACID',
                'N_MeFOSAA': 'N-METHYL PERFLUOROOCTANE SULFONAMIDOACETIC ACID',
                'PFBA': 'PERFLUOROBUTANOIC ACID',
                'PFBS': 'PERFLUOROBUTANE SULFONIC ACID',
                'PFDA':'PERFLUORODECANOIC ACID',
                'PFDOA':'PERFLUORODODECANOIC ACID',
                'PFDS':'PERFLUORODECANESULFONIC ACID',
                'PFHPA': 'PERFLUOROHEPTANOIC ACID',
                'PFHPS':'PERFLUOROHEPTANE SULFONIC ACID',
                'PFHXA':'PERFLUOROHEXANOIC ACID',
                'PFHXDA':'PERFLUOROHEXADECANOIC ACID',
                'PFHXS':'PERFLUOROHEXANE SULFONIC ACID',
                'PFNA':'PERFLUORONONANOIC ACID',
                'PFNS':'PERFLUORONONANE SULFONIC ACID',
                'PFOA':'PERFLUOROOCTANOIC ACID', 
                'PFODA':'PERFLUOROOCTADECANOIC ACID',
                'PFOS':'PERFLUOROOCTANE SULFONIC ACID',
                'PFOSA':'PERFLUOROOCTANE SULFONAMIDE',
                'PFPEA':'PERFLUOROPENTANOIC ACID',
                'PFPES':'PERFLUOROPENTANE SULFONIC ACID',
                'PFTEA':'PERFLUOROTETRADECANOIC ACID',
                'PFTRIA':'PERFLUOROTRIDECANOIC ACID',
                'PFUNDA':'PERFLUOROUNDECANOIC ACID'}


#%%

# organize into the following columns
# 1. SAMPLE_DAT
# 2. FEATURE_NA
# 3. EGAD_SITE_
# 4. each of the PFAS compounds 
# 5. geometry (easting,northing)

# set list of all site sequence numbers 
all_seq = set(data_org.SITE_SEQ)



data = pd.DataFrame() # empty dataframe to reorganize into

print('number of sequences:',len(all_seq))
for seq in all_seq:
    # get all the rows for the specific sequence
    sub = data_org[data_org.SITE_SEQ == seq]
    
    # make list of all the sample point names
    all_names = set(sub.SAMPLE_POINT_NAME)
    
    for name in all_names:
        sub_sub = sub[sub.SAMPLE_POINT_NAME == name]
        
        # make list of all sample dates
        dates = set(sub_sub.SAMPLE_DATE)
        for date in dates:
            dd = {}
            dd['SAMPLE_DAT'] = date
            dd['FEATURE_NA'] = name
            dd['EGAD_SITE_'] = seq
            
            # get each PFAS
            for pfas in pfas_columns.keys():
                
                compound_data = sub_sub[(sub_sub.SAMPLE_DATE == date) & (sub_sub.PARAMETER == pfas_columns[pfas])]
                if len(compound_data) == 0:
                    dd[pfas] = None
                else:
                    dd[pfas] = compound_data.iloc[0].CONCENTRATION
            
            
            lat = sub_sub.SAMPLE_POINT_LATITUDE.iloc[0]
            lon = sub_sub.SAMPLE_POINT_LONGITUDE.iloc[0]
            if (lat == None) or (lon == None):
                dd['geometry'] = None
            else:
                x,y = P(lon,lat)
                dd['geometry'] = shapely.Point(x,y)

            data = pd.concat([data, pd.DataFrame([dd])])

data.to_pickle(base_folder + '/all_pfas.pkl')
            
            
    