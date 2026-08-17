# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 13:15:55 2026

@author: Lucas.Beem


basic theis equation 
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script

import numpy as np
import pylab as pl
import scipy 
import random



def gal2m3(gal):
    return gal * 0.00378541


def r0(Sy,K,Q,threshold):
    # Sy : [ nd ] specific yeild 0.01 to 0.3 (cherry page 61)
    # K  : [ m / s ] hydraulic conductivity
    # Q  : [ m^3 / s ] well discharge , pumping rate, flux 
    
    r = np.arange(0,20000,10) # [m] radial distance 
    t = 3.14e8 # [s] time ( 3.14e8 ~10 years)
    b = 1000 # [m] aquifer thickness

    T = K / b #transmissivity
    u = r**2 * Sy / (4 * T * t)
    dh = Q / (4 * np.pi * T) * scipy.special.expn(1,u)
    
    out = np.zeros( len(threshold) )
    for i,thres in enumerate(threshold):
        i0 = np.nonzero( dh < thres )[0]
        if len(i0) == 0:
            out[i] = -1
        else:
            out[i] = r[i0[0]]
    
    return out
    
    
    # if len(i0) == 1:
    #     return r[i0]
    # else:
    #     return -1

    


nn = 100000
thres = [0.00001,0.0005,0.001,0.005]
rr = np.zeros(( nn,len(thres) ))

for n in range(nn):
    Sy = random.uniform( 0.01 , 0.3 )
    K  = random.uniform( 10e-9 , 10-4 )
    Q  = random.uniform( 4.38126e-06 , 2.19063e-05 ) #100 to 500 gal / day as m3/s
    
    rr[n,:] =  r0(Sy,K,Q,thres)



#%%

width = 50
bins = np.arange(0,10000,width)

fig = pl.figure(1)
fig.clf()
ax = fig.add_subplot(111)
c1,b1 = np.histogram(rr[:,3],bins=bins)
c2,b2 = np.histogram(rr[:,2],bins=bins)
c3,b3 = np.histogram(rr[:,1],bins=bins)
c4,b4 = np.histogram(rr[:,0],bins=bins)

c1 = c1 / nn
c2 = c2 / nn
c3 = c3 / nn
c4 = c4 / nn

pl.bar(b1[:-1], c1, width=width,label='Thres = {} m'.format(thres[3]),alpha=.5)
pl.bar(b2[:-1], c2, width=width,label='Thres = {} m'.format(thres[2]),alpha=.5)
pl.bar(b3[:-1], c3, width=width,label='Thres = {} m'.format(thres[1]),alpha=.5)
pl.bar(b4[:-1], c4, width=width,label='Thres = {} m'.format(thres[0]),alpha=.5)

# pl.hist(rr1, bins=np.arange(0,10000,50))
# pl.hist(rr2, bins=np.arange(0,10000,50))
# pl.hist(rr3, bins=np.arange(0,10000,50))
# pl.arrow(2000,.9,1900,0)
ax.annotate("",xytext=(1000,.09), xy=(10,.09),arrowprops=dict(arrowstyle="->"))
ax.text(1000,.09,'greater than 0.69',va='center')

print(np.sum(rr== -1,0))
# pl.title('{},{},{}'.format(sum(rr[:,0]==-1) ,sum(rr[:,1]==-1) , sum(rr[:,2]==-1) )) # check for failure

pl.xlabel("Distance (m)")
pl.ylabel('fraction')
pl.legend()
pl.ylim((0,0.1))

fig.savefig(base_folder+'/theis_monte.png',dpi=300)
