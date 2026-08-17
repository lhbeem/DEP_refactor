# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 13:49:39 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'lookup'))
sys.path.append(base_folder)
import edd_utils as utils
import paths
import pandas as pd
import numpy as np

def list_append(df,site,ID,loc,date,sitename):
    
    for IDs in  np.unique(df.LAB_SAMPLE_ID):
        locs  = df[df.LAB_SAMPLE_ID == IDs].iloc[0].SAMPLE_POINT_NAME
        dates = df[df.LAB_SAMPLE_ID == IDs].iloc[0].SAMPLE_DATE
        
        loc.append(locs)
        ID.append(IDs)
        site.append(sitename)
        date.append(dates)
    return site,ID,loc

    
# sample list

 
 
cols = ['Site Name','Sample ID','Loc.']
site = []
ID = []
loc = []
date = []


# Dayton Landfill
sitename = 'Dayton'
pth = paths.data + '/brwm_table/daytonLF.xlsx'
utils.brwmtable2edd(pth, 'L9000000',sitename)

# change SAMPLE ID to 47 Rumery Rd
edd = paths.edd +'/L9000000_m60.xlsx'

df  = pd.read_excel(edd)
df.replace('GLOVER', '47rum',inplace=True)
df.to_excel(edd,index=False)


site,ID,loc = list_append(df,site,ID,loc,date,sitename)



#%%
sitename = 'Kittery'
pth = paths.data + '/brwm_table/kitterylf.xlsx'
edd_num = 'L9000001'

utils.brwmtable2edd(pth, edd_num,sitename)

# print the samplenumber address date sets
edd = paths.edd +'/' + edd_num+'_m60.xlsx'
df  = pd.read_excel(edd)


site,ID,loc = list_append(df,site,ID,loc,date,sitename)



#%%
sitename = 'Hardy'
pth = paths.data + '/brwm_table/hardy.xlsx'
edd_num = 'L9000002'
utils.brwmtable2edd(pth, edd_num,sitename)

# print the samplenumber address date sets
edd = paths.edd +'/' + edd_num+'_m60.xlsx'
df  = pd.read_excel(edd)

# replace some sample names
df.replace('65 HARDY RD', '65HARDY',inplace=True)
df.replace('62 HARDY RD', '62HARDY',inplace=True)
df.replace('69 HARDY RD', '69HARDY',inplace=True)
df.replace('60 HARDY RD', '60HARDY',inplace=True)


site,ID,loc = list_append(df,site,ID,loc,date,sitename)


#%% 
sitename = 'Waterboro'
pth = paths.data + '/brwm_table/waterborolf.xlsx'
edd_num = 'L9000003'
utils.brwmtable2edd(pth, edd_num,sitename)

# print the samplenumber address date sets
edd = paths.edd +'/' + edd_num+'_m60.xlsx'
df  = pd.read_excel(edd)

# replace some sample names
df.replace('GASSETT', '87Benn',inplace=True)



site,ID,loc = list_append(df,site,ID,loc,date,sitename)

#%% save list

df2 = pd.DataFrame({'Site Name': site , 'Sample ID': ID , 'Loc.': loc, 'Sample Date':date})

out = base_folder +'/lookup/location_list.xlsx'
df2.to_excel(out,index=False)

