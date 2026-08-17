# -*- coding: utf-8 -*-
"""
Created on Mon May 11 14:34:11 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(base_folder+'/../../lookup')
sys.path.append(base_folder+'/../..')

import site_map




fig = site_map.general_map('Johns store',200,streamp=False,areas=False,samps=False)

ax= fig.get_axes()[0]

ax.plot(506.835,5223.895,'*',color='tab:red',label='Spill Location')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),ncols=2)
y1,y2 = ax.get_ylim()
ax.set_ylim((5223.83,y2))





filename = 'C:/Users/Lucas.Beem/OneDrive - State of Maine/Documents/Projects/refactor/site_specific/johns_store/closure_map.pdf'

fig.savefig(filename)
os.startfile(filename)

