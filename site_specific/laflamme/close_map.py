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

# import paths
import site_map




fig = site_map.general_map('laflamme', 100,streamp=False)


ax = fig.get_axes()[0]

ax.plot(409.83, 4870.160,'*',color='tab:red',label='Spill Location')

# moving 14 mill pond text 
ax.texts[0].set_ha('right')
ax.texts[0].set_position((409.9153219, 4870.1476473))

ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),ncols=2)

ax.text(409.78,4870.17,'Royalsborough Road (Rt. 136)',rotation=-78,color='w',fontsize=12)




filename = 'C:/Users/Lucas.Beem/OneDrive - State of Maine/Documents/refactor/site_specific/laflamme/close_map.pdf'
filename2 = 'C:/Users/Lucas.Beem/OneDrive - State of Maine/Documents/refactor/site_specific/laflamme/close_map.png'

fig.savefig(filename)

fig.savefig(filename2,dpi=300)
os.startfile(filename)






