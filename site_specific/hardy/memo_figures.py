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


samples = ['L2620040-01','L2620040-02','L2620612-01']
labels = ['PW101','62 Hardy','5 Minnow Brook']

out = base_folder


figs = []
for test in ['pfas','landfill_short']:
    results = []
    for samp in samples:
        short = samp.split('-')[0]
        path = paths.edd + '/'+ short +'_m60.xls'

        df = edd_utils.load_edd(path)
        results.append( edd_utils.edd_compound_parse(df, samp, test) )
    
    figs.append( plots.general_compare_plot(test,results,out,labels,save=False,show=False) )


figs[0].savefig(base_folder + '/pfas.png')
figs[1].savefig(base_folder + '/landfill.png')





#%% 62 time series 
samples = ['L9000002-04','L2620040-02']
labels = ['62 Hardy on 9-1-16','62 Hardy on 4-8-26']
out = base_folder


test = 'landfill_short'
results = []
for samp in samples:
    short = samp.split('-')[0]
    if samp.startswith('L9'):
        ext = 'xlsx'
    else:
        ext = 'xls'
    path = paths.edd + '/'+ short +'_m60.'+ext

    df = edd_utils.load_edd(path)
    results.append( edd_utils.edd_compound_parse(df, samp, test) )

    fig= plots.general_compare_plot(test,results,out,labels,save=False,show=False) 

ax = fig.gca()
ax.set_position([.125,.5,.675,.3])
fig.savefig(base_folder + '/62_landfill.png')

#%% pw101 time series 
samples = [ 'L9000002-10','L2620040-01']
labels = ['PW101 on 12-13-13','PW101 on 4-8-26']
out = base_folder


figs = []
test = 'landfill_short'
results = []
for samp in samples:
    short = samp.split('-')[0]
    if samp.startswith('L9'):
        ext = 'xlsx'
    else:
        ext = 'xls'
    path = paths.edd + '/'+ short +'_m60.'+ext

    df = edd_utils.load_edd(path)
    results.append( edd_utils.edd_compound_parse(df, samp, test) )

    fig = plots.general_compare_plot(test,results,out,labels,save=False,show=False)


ax = fig.gca()
ax.set_position([.125,.5,.675,.3])
fig.savefig(base_folder + '/pw_landfill.png')