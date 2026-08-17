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




fig = site_map.general_map('farr', 100,streamp=False)


ax = fig.get_axes()[0]
ax.plot(388.074, 4817.544,'*',color='tab:red',label='Spill Location')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),ncols=2)

ax.text(388.074,4817.507,'Oceana Ave',rotation=-35,color='w',fontsize=12)
ax.text(388.039,4817.510,'West Grand Ave',rotation=65,color='w',fontsize=12)


# remove the stream guaging
ax.texts[0].remove()
ax.lines[0].remove()


filename = 'C:/Users/Lucas.Beem/OneDrive - State of Maine/Documents/Projects/refactor/site_specific/farr/close_map.pdf'
filename2 = 'C:/Users/Lucas.Beem/OneDrive - State of Maine/Documents/Projects/refactor/site_specific/farr/close_map.png'

fig.savefig(filename)

fig.savefig(filename2,dpi=300)
os.startfile(filename)






