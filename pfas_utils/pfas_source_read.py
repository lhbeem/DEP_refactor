# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 14:54:44 2026

@author: Lucas.Beem
"""



import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(base_folder+'/lookup')
# sys.path.append(base_folder)
import paths 

import pandas as pd
import pickle



df = pd.read_excel(paths.pfas_source_xls,header=2)

# make list unique of egads
seqs = set(df['EGAD #'].dropna().tolist())
gener = {}
for seq in seqs:
    
    if isinstance(seq, str):
        if seq in '146316?':
            gener['33422'] = 'Scott Paper / SD Warren'
        elif seq == '30600; 30637':
            gener['30600'] = 'IP-Verso (Bioash)'
            gener['30637'] = 'IP-Verso (Bioash)'
        elif seq == '30058; 30059':
            gener['30058'] = 'South Portland'
            gener['30059'] = 'South Portland'
        elif seq == '28186; 29656':
            gener['28186'] ='Portland Water District'
            gener['29656'] ='Portland Water District'
        elif seq == '31225, 31258, 31259':
            gener['31225'] = 'Scott Paper / SD Warren'
            gener['31258'] = 'Scott Paper / SD Warren'
            gener['31259'] = 'Scott Paper / SD Warren'
        elif seq == '30795, 30761':
            gener['30795'] = 'LAWPCA'
            gener['30761'] = 'LAWPCA'
        elif seq == '31204; 31205':
            gener['31204'] = 'Sabattus SD'
            gener['31205'] = 'Sabattus SD'
        elif seq == '29362, 29363':
            gener['29362'] = 'SD Warren'
            gener['29363'] = 'SD Warren'
        else:
            print(seq)
            
    else:
        gens = df[df['EGAD #'] == seq]
        gen = list(set(gens['Licensee'].dropna().tolist()))
    
        gener[str(seq)] = gen
      

outfile = base_folder+'/lookup/pfas_source.pkl'
with open(outfile, 'wb') as f:
    pickle.dump(gener, f)

print('saved: {}'.format(outfile))
    
    
    
        
    

