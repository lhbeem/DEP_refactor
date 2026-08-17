# -*- coding: utf-8 -*-
"""
Created on Mon May 11 13:14:52 2026

@author: Lucas.Beem

make farr map

"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(base_folder+'/../../lookup')
sys.path.append(base_folder+'/../..')

import site_map




fig = site_map.general_map('hakala', 100,streamp=True)

 
ax = fig.get_axes()[0]
ax.plot(381.24732, 4907.35478,'*',color='tab:red',label='Spill Location')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),ncols=2)




filename = base_folder +'/close_map.pdf'
filename2 = base_folder+ '/close_map.png'

fig.savefig(filename)

fig.savefig(filename2,dpi=300)
os.startfile(filename)






