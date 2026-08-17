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
import matplotlib.patches as mpatches


fig = site_map.general_map('Hardy',200,streamp=False,logop=False,titlep=False)


ax = fig.get_axes()[0]
ax.texts[7].remove()
ax.texts[5].set_ha('right')
ax.texts[5].set_va('top')
ax.texts[2].set_va('top')
ax.lines[12].remove()

ax.texts[0].set_text(' PW102')
ax.texts[3].set_text(' 62 Hardy Road')
ax.texts[5].set_text('60 Hardy Road ')
ax.texts[6].set_text(' PW101')

handles,labels = ax.get_legend_handles_labels()
hand = mpatches.Patch(edgecolor='b', label='Landfill Area',facecolor='none')



handles.append(hand)
labels.append("Landfill Area")
ax.legend(handles=handles,labels=labels,loc='upper center', bbox_to_anchor=(0.5, -0.1),ncols=2)




filename = base_folder+'/memo_map.pdf'
filename2 =  base_folder+'/memo_map.png'
fig.savefig(filename)
fig.savefig(filename2,dpi=300)
os.startfile(filename)



