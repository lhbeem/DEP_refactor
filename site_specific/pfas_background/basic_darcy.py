# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 13:15:55 2026

@author: Lucas.Beem


basic theis equation 
"""

import os
# import sys
base_folder = os.path.dirname(__file__) #folder that contains the script

import numpy as np
import pylab as pl
# import scipy 
import random


def v(mu,dh,k):
    # mu : [ Pa s ] dynamic viscosity
    # dh : [ nd ] hydraulic gradient
    # k  : [ m2 ] hydraulic permeability 
    
    rho = 997
    g = 9.8
    
    v = k * rho * g * dh / mu
    
    return v
    

nn = 1000000
# thres = [0.00001,0.0005,0.001,0.005]
vv = np.zeros( nn)

for n in range(nn):
    dh  = random.uniform( 1e-4 , 1e-2 )
    mu  = random.uniform( 3e-3 , 1e-3 )
    k = random.uniform( 10e-16 , 10e-11 ) # m2

    
    vv[n] =  v(dh,mu,k)


vv *= 30*365*24*3600    # multiply by 30 years in seconds
print(max(vv))
#%%

width = 10
bins = np.arange(0,2000,width)

fig = pl.figure(1)
fig.clf()
ax = fig.add_subplot(111)
v1,b1 = np.histogram(vv,bins=bins)

v1 = v1 / nn



pl.bar(b1[:-1], v1, width=width)

pl.xlabel("Distance (m)")
pl.ylabel('Fraction')
# pl.legend()
# pl.ylim((0,0.1))

fig.savefig(base_folder+'/darcy_monte.png',dpi=300)
