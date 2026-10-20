# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 11:31:13 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'lookup'))

# import paths
# import argparse
import numpy as np


import pandas as pd
# import geopandas as gpd


pfas = pd.read_pickle(r"C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\site_specific\LD1600_report\all_pfas.pkl")
#%%


data = pfas[(pfas.LOCATION != 'AF') & (pfas.LOCATION != 'BT')]

no_samples = len(data)


#%%
l20 = data[data.SUM_OF_6_P < 20]
g20l100 = data[(data.SUM_OF_6_P > 20) & (data.SUM_OF_6_P <= 100)]
g100l1k = data[(data.SUM_OF_6_P > 100) & (data.SUM_OF_6_P < 1000)]
g1k =  data[(data.SUM_OF_6_P >= 1000)]
print('Less than 20 sum of 6: {} / {} ; {}'.format(len(l20),no_samples, len(l20)/no_samples))
print('greater than 20  less than= 100 sum of 6: {} / {} ; {}'.format(len(g20l100),no_samples, len(g20l100)/no_samples))
print('greater than 100  less than= 1000 sum of 6: {} / {} ; {}'.format(len(g100l1k),no_samples, len(g100l1k)/no_samples))
print('greater than 1000 sum of 6: {} / {} ; {}'.format(len(g1k),no_samples, len(g1k)/no_samples))


#%%

pfosg4 = data[(data.SUM_OF_6_P < 20) & (data.PFOS > 4)]
pfoag4 = data[(data.SUM_OF_6_P < 20) & (data.PFOA > 4)]
hxsg10 = data[(data.SUM_OF_6_P < 20) & (data.PFHXS > 10)]
pfnag10 = data[(data.SUM_OF_6_P < 20) & (data.PFBA > 10)]
dag10 = data[(data.SUM_OF_6_P < 20) & (data.HFPO_DA > 10)]


print('MCL')
print('PFOS > 4 less than 20 sum of 6: {}'.format(len(set(pfosg4.FEATURE_NA))))
print('PFOA > 4 less than 20 sum of 6: {}'.format(len(set(pfoag4.FEATURE_NA))))
print('PFHxS > 10 less than 20 sum of 6: {}'.format(len(set(hxsg10.FEATURE_NA))))
print('PFNA > 10 less than 20 sum of 6: {}'.format(len(set(pfnag10.FEATURE_NA))))
print('HFPO-DA > 10 less than 20 sum of 6: {}'.format(len(set(dag10.FEATURE_NA))))






#%% hazard 
# HFPO-DA  10
# PFBS 2000
# PFNA 10
# PFHXS 10


index = []
s6 = []
for row in data.iterrows():
    row = row[1]
    index.append (row.HFPO_DA / 10 + row.PFBS / 2000 + row.PFNA / 10 + row.PFHXS / 10)
    s6.append ( row.SUM_OF_6_P)

index = np.array(index)
s6 = np.array(s6)
ii = sum(index>1)
ii2= sum ( (index>1) & (s6 < 20))
print('number of sample HI > 1: {}'.format(ii))
print('numbner of samples HI > 1 and sum6 < 20: {}'.format(ii2))

hi = np.nonzero((index>1) & (s6 < 20))
print('Seq number')
print(index[ind])
print(data.EGAD_SITE_.iloc[ind])







