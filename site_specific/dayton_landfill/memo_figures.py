# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 15:05:25 2026

@author: Lucas.Beem
"""

# import argparse
import os 
import sys
# import pandas as pd
# import glob
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(base_folder+'/../../lookup')
sys.path.append(base_folder+'/../..')
import paths
# import make_site
import plot_utils as plots
import edd_utils


samples = ['L2579519-01','L2579519-02','L2578511-01']
labels = ['Mw-02','Mw-05','47 Rumery Rd']

out = base_folder


figs = []
for test in ['pfas','voc','landfill_long']:
    results = []
    for samp in samples:
        short = samp.split('-')[0]
        path = paths.edd + '/'+ short +'_m60.xls'

        df = edd_utils.load_edd(path)
        results.append( edd_utils.edd_compound_parse(df, samp, test) )
    
    figs.append( plots.general_compare_plot(test,results,out,labels,save=False,show=False) )


# ax = figs[0].get_axes()[0]
# for t in ax.texts:
#     t.set_fontsize(9)
figs[0].savefig(base_folder + '/pfas.png')
figs[1].savefig(base_folder + '/voc.png')



figs[2].set_size_inches(6.5 , 6)
# print(figs[2].axes[0].get_position().bounds)
figs[2].axes[0].set_position([0.125,.4,0.775,.4])
figs[2].savefig(base_folder + '/landfill_long.png')
