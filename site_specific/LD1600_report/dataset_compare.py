# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 09:06:23 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'../../','lookup'))

import paths
import numpy as np
import geopandas as gpd



# load organized data set
all_pfas_path = r"H:\BRWM\Tech Services Division\LD1600\2026 Legislative Report\20260717_GW_.xlsx"
data_org = gpd.read_file(all_pfas_path,layer='Data')

# load GIS layer 
data_gis = gpd.read_file(paths.sample_locations)


# are there any sequence numbers only present in one dataset? 
