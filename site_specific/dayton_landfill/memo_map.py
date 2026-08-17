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

# import paths
import site_map
import numpy as np



fig = site_map.general_map('Dayton Landfill',200,streamp=False,logop=False,titlep=False)

ax = fig.get_axes()[0]
t = ax.texts[0]
t.set_ha('center')
t.set_va('bottom')
t = ax.texts[1]
t.set_va('top')
t = ax.texts[2]
t.set_va('top')



# position of MW1 MW2 and MW5
xo = np. mean(np.array([369.88451687,369.8219494,369.9154562]))
yo = np.mean(np.array([4822.709840370,4822.770408,4822.8177849]))

angle = 51.7
dx = .05 * np.cos(np.deg2rad(angle))
dy = .05 * np.sin(np.deg2rad(angle))


ax.arrow(xo,yo,dx,dy,fc='w',ec='w')

dx = .01 * np.cos(np.deg2rad(angle+90))
dy = .01 * np.sin(np.deg2rad(angle+90))

dx2 = .005 * np.cos(np.deg2rad(angle))
dy2 = .005 * np.sin(np.deg2rad(angle))

ax.text(xo+dx-dx2,yo+dy-dy2,'GW gradient',fontsize=12,rotation=angle,color='w')


filename = 'C:/Users/Lucas.Beem/OneDrive - State of Maine/Documents/Projects/refactor/site_specific/dayton_landfill/memo_map.pdf'
filename2 = 'C:/Users/Lucas.Beem/OneDrive - State of Maine/Documents/Projects/refactor/site_specific/dayton_landfill/memo_map.png'
fig.savefig(filename)
fig.savefig(filename2,dpi=300)
os.startfile(filename)

