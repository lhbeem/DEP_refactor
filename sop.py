# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 14:21:49 2025

@author: Lucas.Beem
"""

import argparse
import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(base_folder+'/lookup')
import paths
import glob
 

toc =   ('PP-006 : Conceptual Site Model\n'+
'PP-007 : Sampling and Analysis Plan\n'+
'PP-008 : Field Instrument Calibration\n'+
'PP-009 : Vapor Source Investigation Remediation\n'+
'PP-010 : Groundwater Resource and Drinking Water Protection\n'+
'PP-012 : Managing Contaminated Groundwater and Surplus Soils\n'+
'PP-014 : Water Sampling at Petroleum Release Sites\n'+
'PP-015 : Water Supply Filtration and Air Treatment\n'+
'PP-016 : Water Supply Replacement\n'+
'PP-018 : Agreements\n'+
'PP-020 : Well Boring Abandonment Procedure\n'+
'PP-022 : Radon Sampler Certification\n'+
'PP-071 : Site Safety Plan\n'+
'DR-001 : Water Sample Collection From Water Supply Wells\n'+
'DR-002 : Groundwater Sample Collection for Site Investigation and Monitoring\n'+
'DR-003 : Low Flow Groundwater Sampling\n'+
'DR-004 : surface water sediment\n'+
'DR-005 : Soil Gas Collection with Hand Tools\n'+
'DR-006 : soil sampling\n'+
'DR-007 : Dust Wipe Sampling\n'+
'DR-008 : Indoor Air Sampling\n'+
'DR-009 : Microwell installation\n'+
'DR-010 : Container Sampling\n'+
'DR-011 : soil field screening\n'+
'DR-012 : chain of custody\n'+
'DR-013 : Field documentation and trip report\n'+
'DR-014 : FORM Sampling and Analysis\n'+
'DR-015 : Incremental sample methodology\n'+
'DR-016 : Development of Site Specific QAP\n'+
'DR-017 : Equipment Decontamination Protocol\n'+
'DR-019 : Portable Air Monitors\n'+
'DR-023 : Pore Water Sampling\n'+
'DR-025 : XRF Procedure\n'+
'DR-026 : Protocol For Collecting Soil Gas Samples\n'+
'DR-027 : Sub Slab Gas Sampling\n'+
'DR-028 : Well Maintenance Development\n'+
'DR-029 : RSL Calulator\n'+
'TS-004 : field testing soil samples\n')


def main(args):

    if (args.num is None):
        print(toc)
        exit()
    
    # num = args.num.title()
    sop = glob.glob(paths.sop_dir+'/*{}*{}*.pdf'.format(args.num[:2],args.num[2:]))
    if len(sop) == 0:
        print('No SOP found with number: {}'.format(args.num))
        exit()
    sop = sop[0]
    
    
    os.startfile(sop)





if __name__=="__main__":
    parser= argparse.ArgumentParser()
    
    
    parser.add_argument('num' , nargs= '?' , default = None, help='SOP number to open, five characters (pp###,ts###,dr###)')
   
    args = parser.parse_args()
    main(args)