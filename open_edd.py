# -*- coding: utf-8 -*-
"""
Created on Fri May  1 10:22:38 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'lookup'))

import paths
import glob
import argparse


def main(args):
    
    if '-' in args.sample:
        samp = args.sample.split('-')[0]
    else:
        samp = args.sample
    
    if args.p:
        file_path = glob.glob( paths.pdf + '/{}_pdf.pdf*'.format(samp))
    else:
        file_path = glob.glob( paths.edd + '/{}_m60.xls*'.format(samp))
    
    for pth in file_path:
        print(pth)
        os.startfile(pth)
    
    return
    



if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('sample' ,help='sample number of edd or pdf to open')
    parser.add_argument('-p', action='store_true',help='call to open pace pdf')

    args = parser.parse_args()
    main(args)