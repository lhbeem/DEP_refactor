# -*- coding: utf-8 -*-
"""
Created on Wed Oct  1 12:30:11 2025

@author: Lucas.Beem
"""

import argparse
import pandas as pd
import numpy as np

import os 
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'..','lookup'))
sys.path.append(os.path.join(base_folder,'..',))
import paths
import edd_utils as edd 


 
def hazard_index(results):
    con = np.zeros(4) 
    for res in results:
        if 'HFPO-DA' in res:
            if res[1] == 'ND':
                continue
            else:
                con[0] = res[1]
        elif 'PFBS' in res:
            if res[1] == 'ND':
                continue
            else:
                con[1] = res[1]   
        elif 'PFNA' in res:
            if res[1] == 'ND':
                continue
            else:
                con[2] = res[1]
        elif 'PFHXS' in res:
            if res[1] == 'ND':
                continue
            else:
                con[3] = res[1]
    if (con[0] == 0) and (con[2] == 0) and (con[3] == 0): # if all the compounds except PFBS are ND (zero) then hazrd index == zero regardless of PFBS concentration
         index = float(0)
    else:
        index = con[0] / 10 + con[1] / 2000 + con[2] / 10 + con[3] / 10
    return index,con

def main(args):

    if len(args.con) == 4:
        con = np.array([float(s) for s in args.con])
        if sum(con == 0) > 2:
            print('Hazard Index only relevant if two or more of the compounds have non-zero concentrations, \ncondition was not meet by supplied concentrations')
            exit()
        index = con[0] / 10 + con[1] / 2000 + con[2] / 10 + con[3] / 10
        
    elif len(args.con) == 1:
        sample_number = args.con[0]
        if (not len(sample_number) == 11) and (not sample_number.contain('-')):
            print('input not formated as sample number with subsample (e.g. L1234567-01)')
            exit()
        
        samp = sample_number.split('-')[0]
        edd_path = paths.edd + '/{}_m60.xls'.format(samp)
        
        
        if os.path.isfile(edd_path):
            df = edd.load_edd(edd_path)
            test = edd.which_tests(df,sample_number)
            
            if not 'pfas' in test:
                print('sample does not contain pfas results: {}'.format(sample_number))
                exit()
            
            
            results = edd. edd_compound_parse(df,sample_number,'pfas')
            index, con = hazard_index(results)
            if sum(con == 0) > 2:
                print('')
                print('Hazard Index only relevant if two or more of the compounds have non-zero concentrations, \ncondition was not meet by supplied concentrations')
                print('{:>14} {:>12} {:>12} {:>12}'.format('genx(HFPO-DA)',' PFBS', 'PFNA', 'PFHXS'))
                print('{:>14} {:>12} {:>12} {:>12}'.format(*con))
                print('')
                exit()
        
        else: 
            print('\nedd for sample number ({}) not found'.format(samp))
            exit()
        
    else:
        print('\nArguments passed are not 4 numbers or one sample number with subsample\n')
        exit()
        
    
    print('\nHazard Index: {:.2f}\n'.format(index))



if __name__=="__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument('con' , nargs = '*',help='sample number with subsample or for numeric values representing the concentration of genx(HFPO-DA), pfbs, pfna, pfhxS' )
   

    
    
    args = parser.parse_args()
    
    main(args)