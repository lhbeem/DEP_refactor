# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 20:45:25 2026

@author: Lucas.Beem


Print an emperical estimation of the 
equlivalnt carbon number from the compound's
boiling point in degrees celcius 

equation from ITRC figure:
    https://tphrisk-1.itrcweb.org/4-tph-fundamentals/

"""
import os 
import sys

base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'lookup'))
import paths

import argparse
import numpy as np
import pandas as pd
pd.set_option('future.no_silent_downcasting', True) # called to prevent a future warning

def fuel_carbon_length():
    fcl = {'gasoline': [4,12],
           'diesel' : [7,24],
           'kerosine' : [8,17],
           'Fuel oil': [10,24], # and higher potentialy 
           }
    return fcl

def carbon_number(args):
    comps = pd.read_excel(paths.compounds_xls)
    carbon = comps[comps[args.bp] == 1][['compound','carbon_number','equivalent_carbon']]
    carbon = carbon.replace('-',0)
    carbon = carbon.sort_values(by='carbon_number')
    return carbon



def main(args):
    
    if args.bp.lower() in ['vph','eph']:
        cn = carbon_number(args)
        print('')
        for row in cn.iterrows():
            row = row[1]
            if row.carbon_number == 0:
                print('{:30}{:10}{}'.format(row.compound,'-',row.equivalent_carbon))
            else:
                print('{:30}{:<10}{}'.format(row.compound,int(row.carbon_number),row.equivalent_carbon))

        print('')
    
    else:
        bp = float(args.bp)
        EC = 4.12 + 0.02 * bp + 6.5e-5 * bp ** 2
        print('Equilant Carbon number: ',np.round(EC,1))
    
    



if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('bp' ,type=str, help='Boiling point in celcius')
    


    args = parser.parse_args()
    main(args)