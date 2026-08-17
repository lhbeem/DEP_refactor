# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 09:33:42 2026

@author: Lucas.Beem
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'lookup'))
sys.path.append(base_folder)
import paths
import make_site

import numpy as np
import geopandas as gpd 
import shapely 
from matplotlib import pylab as pl
import matplotlib.image as mpimg
from osgeo import gdal, osr
import pyproj


def load_basemap(site):
    
    filename = paths.aerial_images+'/'+site+'.tif'
    if not os.path.isfile(filename):
        print('\nBasemap for {} not found'.format(site))
        print('check data/aerial_images\n')
        exit()
    
    dataset = gdal.Open(filename)
    rgb_array = dataset.ReadAsArray()
    red_band = rgb_array[0, :, :]
    green_band = rgb_array[1, :, :]
    blue_band = rgb_array[2, :, :]
    base_map = np.dstack((red_band, green_band, blue_band))
    
    geotransform = dataset.GetGeoTransform()
    x_origin, pixel_width, _, y_origin, _, pixel_height = geotransform
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize
    
    ulx = x_origin 
    uly = y_origin
    lrx = x_origin + (cols * pixel_width)
    lry = y_origin + (rows * pixel_height)
    
    

    projection = osr.SpatialReference(wkt=dataset.GetProjection()).GetAttrValue('AUTHORITY',1)
    P = pyproj.Transformer.from_crs("EPSG:{}".format(projection), "EPSG:32619", always_xy=True)
    ulx,uly = P.transform(ulx,uly)
    lrx,lry = P.transform(lrx,lry)
    
    ll = np.array([ulx,lrx,lry,uly])/1000
    
    
    return base_map,ll,projection


def general_map(siteID,dist,contourp=False,roadp=False,streamp=True,areas=True,logop=True,titlep=True,samps=True):
    
    _,df,_,_ = make_site.load_from_pickle(paths.site_pickle)
    sitename = make_site.shortcut(siteID).title()
    
    spill_type = df[df.name == sitename].type.tolist()[0].upper()
    spill_num = make_site.get_id( sitename, 'spill')
    
    town = df[df['name'] == sitename]['town'].iloc[0] 
    
    print('Running site: {}'.format(sitename))
    # print('Offset: {} m'.format(args.d))
    
    # get site point
    # wpt = {}
    layers = gpd.list_layers(paths.site_pts)
    for layer_name in layers.iterrows():
        df = gpd.read_file(paths.site_pts, layer=layer_name[1]['name'])
        pt = df[df['Name'] == sitename]['geometry']
        if len(pt) == 1:
            break
    
    # define ROI
    x = [pt.x - dist , pt.x - dist , pt.x + dist , pt.x + dist , pt.x - dist]
    y = [pt.y - dist , pt.y + dist , pt.y + dist , pt.y - dist , pt.y - dist]
    ROI = np.array(np.hstack((x,y)))
    
    offset = 2 * dist
    road_adjust = np.array([[-offset,-offset],
    [-offset,offset],
    [offset,offset],
    [offset,-offset],
    [-offset,-offset]])
    
    road_ROI = shapely.Polygon(ROI + road_adjust)
    
    
    ROI = shapely.Polygon( ROI )

    # load basemap
    basemap,ll,_ = load_basemap(siteID)

    # # load layers for plotting
    
    streams = gpd.read_file(paths.streams, mask= ROI)
    rivers = gpd.read_file(paths.rivers, mask= road_ROI)
   
    samples = gpd.read_file(paths.egad_samples, mask= ROI)
   
    lines = gpd.read_file(paths.ts_line, mask= ROI)
 
    
    # plot map
    fig = pl.figure(figsize = [8.5,11])
    fig.clf()
    
    ax = fig.add_axes((.1,.2,.8,.7))
    
    
    pl.imshow(basemap,extent=ll)
    
    # contours
    if contourp:
        topo = []
        n = 0
        while len(topo) == 0: #read topo tile until there is data within ROI
            n += 1
            topo = gpd.read_file(paths.dem_contour_path(n), mask= road_ROI)
        for i,top in enumerate(topo.iterrows()):
            rd = shapely.get_coordinates(top[1].geometry)
            if i == 0:
                pl.plot(rd[:,0]/1000,rd[:,1]/1000,color=[.7,.7,.7],lw=1)
            else:
                pl.plot(rd[:,0]/1000,rd[:,1]/1000,color=[.7,.7,.7],lw=1)
    
    
    # plot roads
    if roadp:
        roads = gpd.read_file(paths.roads, mask= road_ROI)
        for i,road in enumerate(roads.iterrows()):
            rd = shapely.get_coordinates(road[1].geometry)
            
            if i == 0:
                pl.plot(rd[:,0]/1000,rd[:,1]/1000,color=[.3,.3,.3],label='Public Roads',lw=3)
            else:
                pl.plot(rd[:,0]/1000,rd[:,1]/1000,color=[.3,.3,.3],lw=.2)
            I = int(len(rd)/2)
            pl.text(rd[I,0]/1000,rd[I,1]/1000,' '+road[1]['strtname'].title())
        
    
    if streamp:
        streams = gpd.read_file(paths.streams, mask= ROI)
        rivers = gpd.read_file(paths.rivers, mask= road_ROI)
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
    
    # plot areas 
    if areas:
        area = gpd.read_file(paths.ts_area, mask= ROI)
        for i,area in enumerate(area.iterrows()):
            rd = shapely.get_coordinates(area[1].geometry)
            if i == 0 and (area[1]['FEATURE_NA'] is not None):
                
                pl.plot(rd[:,0]/1000,rd[:,1]/1000,'b',label=area[1]['FEATURE_NA'].title())
            else:
                pl.plot(rd[:,0]/1000,rd[:,1]/1000,'b')
            # pl.text(rd[2,0]/1000,rd[2,1]/1000,' '+area[1]['FEATURE_NA'].title())
        
    #plot sample locations
    if samps:
        if len(samples)> 1:
            label = 'Sample Locations'
        else:
            label = 'Sample Location'
        for i,sample in enumerate(samples.iterrows()):
            rd = shapely.get_coordinates(sample[1].geometry)
            if i == 0:
                pl.plot(rd[:,0]/1000,rd[:,1]/1000,'.w',label=label,markeredgecolor='black')
            else:
                pl.plot(rd[:,0]/1000,rd[:,1]/1000,'.w',markeredgecolor='black')
           
            pl.text(rd[:,0]/1000,rd[:,1]/1000,' '+sample[1]['FEATURE_NA'].title(),color='w')
        
        #plot lines
        for i,line in enumerate(lines.iterrows()):
            rd = shapely.get_coordinates(line[1].geometry)
            if i == 0:
                pl.plot(rd[:,0]/1000,rd[:,1]/1000,'k',label=line[1]['FEATURE_NA'].title())
            else:
                pl.plot(rd[:,0]/1000,rd[:,1]/1000,'k')
           
            # pl.text(rd[:,0]/1000,rd[:,1]/1000,' '+sample[1]['FEATURE_NA'].title(),color='w')

    
    #plot points 
    pts = gpd.read_file(paths.ts_pt, mask= ROI)
    for i,pt in enumerate(pts.iterrows()):
        rd = shapely.get_coordinates(pt[1].geometry)
        if i == 0:
            pl.plot(rd[:,0]/1000,rd[:,1]/1000,'^w',markersize = 4, label='Reference Points',markeredgecolor='black')
        else:
            pl.plot(rd[:,0]/1000,rd[:,1]/1000,'^w',markersize = 4,markeredgecolor='black')
       
        pl.text(rd[:,0]/1000,rd[:,1]/1000,' '+pt[1]['FEATURE_NA'].title(),color='w')
    
    # legend
    pl.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),ncols=2)
    minx, miny, maxx, maxy = ROI.bounds
    ax.set_xlim(minx/1000,maxx/1000)
    ax.set_ylim(miny/1000,maxy/1000)

    
    ax.set_aspect('equal')
    ax.set_xlabel('Easting (km)')
    ax.set_ylabel('Northing (km)')
    ax.ticklabel_format(axis='x', useOffset=False)
    ax.ticklabel_format(axis='y', useOffset=False)
    

    
    # logo
    if logop:
        logo = mpimg.imread(paths.dep_color)
        ax1 = fig.add_axes((.8,.02,.15,.15))
        ax1.imshow(logo)
        ax1.set_axis_off()


    # adjust figure toward the right side of page
    bb = list(ax.get_position().extents)
    w = bb[2] - bb[0]
    h = bb[3] - bb[1]
    bb_diff = .95 - bb[2]
    bb[0] += bb_diff
    ax.set_position([bb[0],bb[1],w,h])
    
    if titlep:
        ax2 = fig.add_axes((0,0,1,1))
        ax2.axis('off')
        ax2.text(.5,.05,'{} {}\n{}\n{}, ME'.format(siteID.title(),spill_type,spill_num,town),ha='center',fontsize=12)
    
    return fig
