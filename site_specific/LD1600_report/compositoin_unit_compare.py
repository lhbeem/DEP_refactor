# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 15:20:36 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'../../lookup'))

import paths
import numpy as np
import pyproj
import pandas as pd
import geopandas as gpd
import shapely 
import matplotlib.pylab as pl



'''
compare contamiantion composition between inside and outside of unit
'''



seqs = [27476,28191,29257,29722,30016,30055,
       30303,30409,30613,159164]


data = pd.read_excel(paths.report_database,sheet_name='Sheet 1')

# make pyproj object to project into epsg:29616
P = pyproj.Proj('EPSG:26919')


use_exceed = {'27476' : True,
              '28191' : False,
              '29257' : False,
              '29722' : True,
              '30016' : False,
              '30055' : False,
              '30303' : False,
              '30409' : False,
              '30613' : False,
              '159164': False,
              }

unit = {'27476' : 'Pem',
        '28191' : 'Pt',
        '29257' : 'Pem',
        '29722' : 'Pu',
        '30016' : 'Pg',
        '30055' : 'Pp',
        '30303' : 'Pt',
        '30409' : 'Pg',
        '30613' : 'Pt',
        '159164': 'Pm',
        
        }


