# -*- coding: utf-8 -*-
"""
Created on Mon May 11 13:14:52 2026

@author: Lucas.Beem

make jimbob map

"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(base_folder+'/../../lookup')
sys.path.append(base_folder+'/../..')

# import paths
import site_map




fig = site_map.general_map('lane', 100)


filename = base_folder +'/close_map.pdf'
fig.savefig(filename)
os.startfile(filename)






