# -*- coding: utf-8 -*-
"""
Created on Wed May  6 14:38:54 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'lookup'))
import paths
import edd_utils as edd
import argparse
import glob
import pandas as pd
import numpy as np



def empty_col(df,header):
    return np.any(df[header] == ' ')

def main(args):
    samp = args.sample.split('-')[0]
    edd_path = glob.glob( paths.edd + '/{}_m60.xls*'.format(samp))[0]
    
    if os.path.isfile((edd_path)):
        df = pd.read_excel(edd_path)
        df.columns = df.columns.str.upper()
        
        df = df[df['LAB_SAMPLE_ID'] == args.sample+' ']
        df = df[df['RESULT_TYPE_CODE'] == 'TRG']
        
        if args.id == '-':
            ID = args.name
        else:
            ID = args.id
        
        headers = {'PROJECT/SITE': args.site.upper(),
                   'SAMPLE_POINT_NAME': args.name.upper(),
                   'SAMPLE_ID': ID.upper(),
                   'SAMPLE_TYPE':args.type.upper(),
                   'SAMPLE_LOCATION': args.location.upper(),
                   'SAMPLE_COLLECTION_METHOD': args.method.upper(),
                   'TREATMENT_STATUS' : args.treat.upper(),
                   'SAMPLED_BY' : args.by.upper()
                   }
        
        if args.o == False:
            print('')
            
            for header in headers.keys():
                if empty_col(df,header):
                    print('{} contains empty cells'.format(header))
                else:
                    if np.all(df[header] == headers[header]):
                        print('{} matches: {}'.format(header,headers[header]))
            print('')           
                        
        else: #write document 
            
            df = pd.read_excel(edd_path)
            df.columns = df.columns.str.upper()
            I = (df['LAB_SAMPLE_ID'] == args.sample+' ') & (df['RESULT_TYPE_CODE'] == 'TRG')
            
            for header in headers:
                df.loc[I, header] = headers[header]
 
            if args.d:             
                df.loc[I,'QC_TYPE'] = 'D'

            file = 'C:/Users/Lucas.Beem/Downloads/{}_m60.xlsx'.format(args.sample.split('-')[0])
            df.to_excel(file, index=False)
            print('updated edd saved to: {}'.format(file))
      
    return
    



if __name__=="__main__":
    parser= argparse.ArgumentParser()
    
    parser.add_argument('sample', help='Lab sample number with sub sample')
    parser.add_argument('site', help='Site Name')
    parser.add_argument('name', help='Sample location name')
    parser.add_argument('location', help='Sample location e.g. PT, OT, etc')
    parser.add_argument('-id', default='-')
    parser.add_argument('-type', default = 'GW', help='Typically either GW or SL')
    parser.add_argument('-method', default = 'PST')
    parser.add_argument('-treat', default = 'N')
    parser.add_argument('-by', default = 'DEP')
    parser.add_argument('-o',action='store_true', help='write new xls')
    parser.add_argument('-d', action='store_true',help='sample is duplicate')
    

    args = parser.parse_args()
    
    main(args)