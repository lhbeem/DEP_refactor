# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 15:51:07 2026

@author: Lucas.Beem
"""
import numpy as np


#year 2023,2021,2018,2016,2013
# napthalene is only one that changed since 2018
historic_rag_gw = {'C9-C18 Aliphatics' : [350 , 350 , 350,700,700],
     'C5-C8 Aliphatics, Adjusted' : [180,180,180,300,300],
     'C9-C12 Aliphatics, Adjusted' : [350 , 350 , 350,700,700],
     'Benzene' : [4.6,4.6,4.6,4,4],
     'Toluene' : [1100,1100,1100,600,600],
     'Ethylbenzene' : [15,15,15,30,30],
     'p/m-Xylene' : [190,190,190,1000,1000],
     'o-Xylene' : [190,190,190,1000,1000],
     'Methyl tert butyl ether' : [140,140,140,40,40],
     'C9-C10 Aromatics' : [71,71,71,200,200],
     'C19-C36 Aliphatics' : [40000,40000,40000,10000,10000],
     'C11-C22 Aromatics, Adjusted' : [600,600,600,200,200],
     'Naphthalene' : [1.2,1.2,1.7,10,10],
     '2-Methylnaphthalene' : [36,36,36,30,30],
     'Acenaphthylene' : [520,520,520,np.nan,np.nan],
     'Acenaphthene' : [540,540,540,400,400],
     'Fluorene' : [290,290,290,300,300],
     'Phenanthrene' : [180,180,180,np.nan,np.nan],
     'Anthracene' : [1800,1800,1800,2000,2000],
     'Fluoranthene' : [800,800,800,300,300],
     'Pyrene' : [120,120,120,200,200],
     'Benzo(a)anthracene' : [0.3,0.3,0.3,0.5,0.5],
     'Chrysene' : [250,250,250,50,50],
     'Benzo(b)fluoranthene' : [2.5,2.5,2.5,0.5,0.5],
     'Benzo(k)fluoranthene' : [25,25,25,5,5],
     'Benzo(a)pyrene' : [0.25,0.25,0.25,0.05,0.05],
     'Indeno(1,2,3-cd)Pyrene' : [2.5,2.5,2.5,0.5,0.5],
     'Dibenzo(a,h)anthracene' : [0.25,0.25,0.25,0.05,0.05],
     'Benzo(g,h,i)perylene' : [600,600,600,np.nan,np.nan],
     }