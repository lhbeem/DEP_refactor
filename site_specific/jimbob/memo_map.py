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




fig = site_map.general_map('jimbob', 100)

ax = fig.get_axes()
t = ax[0].texts[2]
t.set_ha('right')
t = ax[0].texts[5]
t.set_ha('right')
t.set_va('top')



filename = 'C:/Users/Lucas.Beem/OneDrive - State of Maine/Documents/Projects/refactor/site_specific/jimbob/close_map.pdf'
fig.savefig(filename)
os.startfile(filename)






