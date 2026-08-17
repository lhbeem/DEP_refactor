# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 10:04:10 2026

@author: Lucas.Beem
"""

# using the files generted bu pfas_Data_setup
# make a basic map for a specified site





import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'..','lookup'))
sys.path.append(base_folder)

import paths
import rags
import LD_site_table

import argparse
import numpy as np
from matplotlib import pylab as pl
import geopandas as gpd

import shapely


layer_compounds =  {
              'PFBS' : 'PFBS',
              'PFBA': 'PFBA',
              'PFHXS': 'PFHXS',
              'PFHXA': 'PFHXA',
              'PFNA': 'PFNA',
              'PFOS' : 'PFOS',
              'PFOA' : 'PFOA',
              'Sum of 6': 'SUM_OF_6_P',
              'HFPO-DA':'HFPO-DA',
               '4:2FTS':'F4_2_FTS',
               'PFPEA': 'PFPEA',
               'PFPES': 'PFPES',
               'PFHXDA': 'PFHXDA',
               '6:2FTS':'F6_2_FTS',
               'PFHPS': 'PFHPS',
               'PFHPA': 'PFHPA',
               'ADONA': 'ADONA',
               'NMEFOSAA':'N_MeFOSAA',
               'FOSA':'PFOSA',
               'NETFOSAA' : 'N_EtFOSAA',
               '8:2FTS':'F8_2_FTS',
               'PFNS':'PFNS',
               'PFDA':'PFDA',
               'PFDS':'PFDS',
               'PFUNA': 'PFUNDA',
               'PFDOA': 'PFDOA',
              'PFTRDA': 'PFTRIA',
              'PFTA': 'PFTEA',
              'PFODA': 'PFODA',}

def main(args):
     
    #check compound
    if args.compound == '6':
        args.compound = 'Sum of 6'
    try:
        layer_name = layer_compounds[args.compound]
    except:
        print('')
        print('compound not found: {}'.format(args.compound))
        print('use one of:',layer_compounds.keys())
        exit()
    compound = args.compound
    table = LD_site_table.table()
    sitename = table[table.seq == int(args.seq)].site.to_list()[0]
    
    
    
    # load fields
    field_df = gpd.read_file(paths.fields)
    main_fields = field_df[field_df.EGAD_SITE_ == int(args.seq)]
    
    if len(main_fields) == 0:
        print('')
        print('No Field found for {}'.format(args.seq))
        print('')
        exit()
    
    ROI = main_fields.total_bounds + [-args.dist, -args.dist, args.dist,args.dist]
    x = [ROI[0] , ROI[0] , ROI[2] , ROI[2] , ROI[0]]
    y = [ROI[1] , ROI[3] , ROI[3] , ROI[1] , ROI[1]]
    ROI = np.array(np.vstack((x,y))).T
   
    # road adjust is to make sure that roads near the edge of map are inlcuded 
    # by loading in a larger ROI
    road_adjust = np.array([[-1000,-1000],
    [-1000,1000],
    [1000,1000],
    [1000,-1000],
    [-1000,-1000]])
    
    road_ROI = shapely.Polygon(ROI +road_adjust)
    ROI = shapely.Polygon( ROI )
    
    # Check for other fields within ROI
    sub_fields = gpd.read_file(paths.fields, mask= ROI)
    
    # load roads 
    roads = gpd.read_file(paths.roads, mask= road_ROI)
    
    # load topo contours
    topo = []
    n = 0
    
    for n in range(1,6):
        topo.append( gpd.read_file(paths.dem_contour_path(n), mask= road_ROI))

    
    #load streams
    streams = gpd.read_file(paths.streams, mask= road_ROI)
    #load streams
    rivers = gpd.read_file(paths.rivers, mask= road_ROI)
    
    # load soil polygons
    soils = gpd.read_file(paths.soil_polygons, mask = ROI)
    
    # check for samples witin ROI
    samples = gpd.read_file(paths.sample_locations, mask = ROI)
    # format array on concentrations for compound
    con = np.zeros(len(samples))
    for i,c in enumerate(samples[layer_name].tolist()):
        try:
            con[i] = float(c)
        except:
            if c is None:
                con[i] = 0
            elif c.startswith('ND'):
                con[i] = 0
            elif c.endswith(('J','U','B')):
                con[i] = float(c.split(' ')[0])
    
    sx = np.array(samples['geometry'].x.tolist())
    sy = np.array(samples['geometry'].y.tolist())
    
    
    
    # make map
    fig = pl.figure(figsize = [11,8.5])
    fig.clf()
    
    ax = fig.add_axes((.1,.2,.8,.7))
    
    
    #plot contours
    for j in range(len(topo)):
        for i,top in enumerate(topo[j].iterrows()):
            rd = shapely.get_coordinates(top[1].geometry)
            if i == 0:
                pl.plot(rd[:,0]/1000,rd[:,1]/1000,color=[.7,.7,.7],lw=1)
            else:
                pl.plot(rd[:,0]/1000,rd[:,1]/1000,color=[.7,.7,.7],lw=1)
    
    # plot roads
    for i,road in enumerate(roads.iterrows()):
        rd = shapely.get_coordinates(road[1].geometry)
        if i == 0:
            pl.plot(rd[:,0]/1000,rd[:,1]/1000,color='k',label='Public Roads',lw=.5)
        else:
            pl.plot(rd[:,0]/1000,rd[:,1]/1000,color='k',lw=.5)
    
    # plot rivers
    for i,river in enumerate(rivers.iterrows()):
        rd = shapely.get_coordinates(river[1].geometry)
        if i == 0:
            pl.plot(rd[:,0]/1000,rd[:,1]/1000,color=[0.0549, 0.529, 0.8])
        else:
            pl.plot(rd[:,0]/1000,rd[:,1]/1000,color=[0.0549, 0.529, 0.8])
    
    #plot streams
    for i,stream in enumerate(streams.iterrows()):
        rd = shapely.get_coordinates(stream[1].geometry)
        if i == 0:
            pl.plot(rd[:,0]/1000,rd[:,1]/1000,color=[0.0549, 0.529, 0.8],lw=1,label='Streams')
        else:
            pl.plot(rd[:,0]/1000,rd[:,1]/1000,color=[0.0549, 0.529, 0.8],lw=1)
    
    
    # plot secondary fields
    lab_n = 0
    if len(sub_fields) > len(main_fields):
        for field in sub_fields.iterrows():
            for geom in field[1].geometry.geoms:
                x,y = geom.exterior.xy
                x= np.array(x)/1000
                y = np.array(y) / 1000
                if lab_n == 0:
                    if (len(sub_fields) - len(main_fields)) > 2:
                        lab = 'adjacent sites'
                    else:
                        lab = 'adjacent site'
                    pl.plot(x,y,'b',label=lab)
                    lab_n = 1
                else:
                    pl.plot(x,y,'b')
                if args.pseq:
                    if field[1].EGAD_SITE_ != args.seq:
                        pl.text(x[0],y[0],str(field[1].EGAD_SITE_),clip_on=True)
    
    #plot main feilds
    lab_n = 0
    for field in main_fields.iterrows():
        for geom in field[1].geometry.geoms:
            x,y = geom.exterior.xy
            x= np.array(x)/1000
            y = np.array(y) / 1000
            if lab_n == 0:
                pl.plot(x,y,'k',label='{}'.format(sitename))
                lab_n = 1
            else:
                pl.plot(x,y,'k')
      
    # plot soil polygons
    # soil_c = 'PFOS'
    lab_s = 0
    for soil in soils.iterrows():
        if soil[1].EGAD_SITE_ != args.seq:
            continue
        for geom in soil[1].geometry.geoms:
            x,y = geom.exterior.xy
            x= np.array(x)/1000
            y = np.array(y) / 1000
            if lab_s == 0:
                pl.fill(x,y,'k',label='{}'.format(sitename),alpha=.5)
                lab_s = 1
            else:
                pl.fill(x,y,'k')
    
    # plot samples
    I = con == 0
    ax.plot(sx[I]/1000,sy[I]/1000,'k^',label='ND')
    
    I = con > 0
    im = ax.scatter(sx[I]/1000, sy[I]/1000, c=con[I],cmap='viridis',vmin=0,label='Detection',zorder=1000)
    
    cb = fig.colorbar(im)
    cb.set_label('{} Concentration (ppt)'.format(compound))
    
    
    # plot exceedamce circles ssit
    nn = 0
    if rags.pfas_gw[compound] != '-':
        I = con > float(rags.pfas_gw[compound])
        if nn == 0:
            pl.plot(sx[I]/1000,sy[I]/1000,'or',markersize=10,markerfacecolor='None',label='Exceedance',zorder=1000)
        else:
            pl.plot(sx[I]/1000,sy[I]/1000,'or',markersize=10,markerfacecolor='None',zorder=1000)
    
    # direct label concentrations
    if args.dl:
        for i,conn in enumerate(con):
            if conn == 0:
                continue
            pl.text(sx[i]/1000,sy[i]/1000,' {}'.format(conn))
    
    
    # plot contours
    if args.c:
        vmin = cb.mappable.norm.vmin
        vmax = cb.mappable.norm.vmax
        pl.tricontour(sx/1000,sy/1000,con,np.linspace(vmin,vmax,6)[1:5],vmin=vmin , vmax=vmax)
        # minx, miny, maxx, maxy = ROI.bounds
        ax.set_xlim(ax.get_xlim() + np.array([-25,25]) )
        ax.set_ylim(ax.get_ylim() + np.array([-25,25]) )
    
   
    
    minx, miny, maxx, maxy = ROI.bounds
    ax.set_xlim(minx/1000,maxx/1000)
    ax.set_ylim(miny/1000,maxy/1000)
   
    pl.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),ncols=2)
   
    
    ax.set_aspect('equal')
    ax.set_title('{} - {} - {}'.format(sitename,args.seq,compound))
    ax.set_xlabel('Easting (km)')
    ax.set_ylabel('Northing (km)')
    ax.ticklabel_format(axis='x', useOffset=False)
    ax.ticklabel_format(axis='y', useOffset=False)

    output = r'C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\PFAS_comprehensive\maps\{}_{}_{:.0f}m.pdf'.format(args.seq,compound,args.dist)
    output2 = r'C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\PFAS_comprehensive\maps\{}_{}_{:.0f}m.png'.format(args.seq,compound,args.dist)
    fig.savefig(output)
    fig.savefig(output2, dpi=300)
    print('saved:{}'.format(output))
    
    os.startfile(output)
    
    
    
    
    
    
    
if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('seq', help='sequence number of site')
    parser.add_argument('--compound','-s', nargs='?', type=str.upper, default = '6',help='Compound to display')
    parser.add_argument('--dist','-d' ,nargs = '?', default = 800, type = float, help='distance from field(s) edge to include in map (meters)')
    parser.add_argument('-c' ,action='store_true', help='Turn on concentration contour plotting')
    parser.add_argument('-pseq' ,action='store_true', help='turn on plot sequence number for adjacent fields')
    parser.add_argument('-dl' ,action='store_true', help='Direct label concentrations')
   
    
    args = parser.parse_args()
    main(args)