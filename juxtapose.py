# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 09:37:46 2025

@author: Lucas.Beem

compare the results between numerous samples

        345          seep1       351
juxta L2450976-01  L2549961-01 L2543226-01

dayton landfill 
juxta_re L2579519-01 L2579519-02 L2578511-01 -test landfill_long
"""

import argparse
import os 
import sys
# import pandas as pd
import glob
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(base_folder+'/lookup')
sys.path.append(base_folder)
import paths
import make_site
import plot_utils as plots
import edd_utils


# import parse_utils as parse
# import make_plots as plots
# import tracking_utils as track 



def main(args):
    # if args.type == None:
    #     print('')
    #     print('plot type needs to be supplied')
    #     print('')
    #     exit()
    
    out = os.path.join(base_folder,'figures') #where figures are saved
  
    #check for the existance of Edds of the supplied samples and get the paths to the data
    pths = []
    for samp in args.samples:
        sample_number = samp.split('-')[0]
        edd_path = glob.glob(paths.edd + '/{}_m60.xls*'.format(sample_number))
        if len(edd_path) > 0:
            if os.path.isfile(edd_path[0]):
                print('Parsing EDD for {}'.format(samp))
                pths.append( [samp, edd_path[0]] )
            else:
                print('No EDD found for {}'.format(samp))
        else:
            print('No EDD found for {}'.format(samp))
    
    
    # get address from sample number using the location.pickle
    if args.label is not None:
        address = args.label
    else:
        address = []
        df,_,_,_ = make_site.load_from_pickle(paths.site_pickle)
        for pth in pths:
            add = df[df['Sample ID'] == pth[0]]['Loc.']
            if len(add) == 0:
                address.append( pth[0] )
            else:
                address.append( add )
    
    
    results = []
    for pth in pths:
        df = edd_utils.load_edd(pth[1])
        results.append( edd_utils.edd_compound_parse(df, pth[0], args.test) )

    plots.general_compare_plot(args.test,results,out,address)


if __name__=="__main__":
    parser= argparse.ArgumentParser()
        
    parser.add_argument('samples' , nargs= '*' , default = None, help='samples to compare as sample numbers with subsample')
    parser.add_argument('-test' , help='which test result to plot', choices=['pfas','landfill_long','landfill_short','eph','vph','pot','voc'])
    parser.add_argument('-label' , nargs= '*', help='labels to use for each sample',)
    # parser.add_argument('-test' , action='store_true' , help='test which tests are shared between all sample IDs')
    
    args = parser.parse_args()
    
    
    
    main(args)