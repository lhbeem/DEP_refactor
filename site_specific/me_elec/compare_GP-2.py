# -*- coding: utf-8 -*-
"""
Created on Thu Jan  1 16:43:10 2026

@author: Lucas.Beem


Maine Electronics.
Convert the common geology file into an "edd" csv that will be read by
the data parser

"""

import pandas as pd
import numpy as np
import pylab as pl

data = pd.read_excel(r"C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\data\common\me_elec_.xlsx",
                      sheet_name = 'Data')



#%% compare GP-2 to GP-3, GP-4, GP-5, MW-2A, MW-2B, MW-3
    # compare arsenic
fig = pl.figure(1)
pl.clf()

for well in ['GP-2','GP-3','GP-4','GP-5','MW-2A','MW-2B','MW-3B']:
    # if well in ['MW-2A']:
    #     continue
    d1 = data[data.SAMPLE_POINT_NAME == well]
    d2 = d1[d1.PARAMETER == 'ARSENIC']
    pl.plot(d2.SAMPLE_DATE, d2.CONCENTRATION,'.',label=well)

pl.legend()

pl.xlabel('Year')
pl.ylabel(r'Arsneic Concentration (ppb)')

fig.savefig(r'C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\refactor\site_specific\me_elec\arsenic_1.png',dpi=300)

pl.ylim((-5,105))
pl.legend(loc=9)
fig.savefig(r'C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\refactor\site_specific\me_elec\arsenic_2.png',dpi=300)

