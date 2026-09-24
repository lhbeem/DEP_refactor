# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 12:46:00 2026

@author: Lucas.Beem

PFAS table results for closure document

from pandas.plotting import table 
merge cells: https://stackoverflow.com/questions/53783087/double-header-in-matplotlib-table
"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'..','lookup'))
sys.path.append(os.path.join(base_folder,'..',))

import paths
import edd_utils as edd

import argparse
import numpy as np
import pandas as pd
import geopandas as gpd
from matplotlib import pylab as pl
import datetime



# columns are 2023 RAGs Residential, Interim Drinking water, EPA MCL
pfas = {'PFOS' : ['40', '','4','PFOS'],
        'PFOA' : ['60', '','4','PFOA'],
        'PFBS' : ['6000', '','10','PFBS'],
        'PFBA': ['19000','','','PFBA'],
        'PFHXS': ['390', '','10','PFHXS'],
        'PFHXA': ['9900','', '','PFHXA'],
        'PFNA': ['59', '','10','PFNA'],
        'PFHPA': ['', '','','PFHPA'] , # part of sum of six
        'PFDA': ['','','','PFDA'], # part of sum of six 
        'HFPO-DA': ['60','','10','HFPO_DA'],
        'SUM OF 6': ['','20','','SUM_OF_6_P'],
        }


pfas_norag = {'PFOS' : ['','4','PFOS'],
        'PFOA' : ['','4','PFOA'],
        'PFBS' : ['','10','PFBS'],
        'PFHXS': ['','10','PFHXS'],
        'PFNA': [ '','10','PFNA'],
        'PFHPA': [ '','','PFHPA'] , # part of sum of six
        'PFDA': ['','','PFDA'], # part of sum of six 
        'HFPO-DA': ['','10','HFPO_DA'],
        'Sum of 6': ['20','','SUM_OF_6_P'],
        }

# columns are 2023 RAGs LTG, 2023 RAGs Residential 
soil = {'PFOS'      :['1','170'],
        'PFOA'      :['17','260'],
        'HFPO-DA'   :['0.81','320'],
        'PFBA'      :['36','110000'],
        'PFBS'      :['110','26000'],
        'PFHXA'     :['13','43000'],
        'PFHXS'     :['0.47','1700'],
        'PFNA'      :['4.6','260']}

def short2long(pfas):
    dd = pd.read_excel(paths.compounds_xls)
    dd = dd.fillna('')
    long = []
    for col in ['alias1','alias2','alias3']:
        aa = dd[dd.compound == pfas][col].iloc[0]
        if aa == '':
            continue
        else:
            long.append(aa)
    return long


def make_table_gw_gis(data):
    table = pd.DataFrame(['','Interim\nDWS','EPA\nMCL']+data.FEATURE_NA.to_list()).T
    
    date = []
    for d in data.SAMPLE_DAT.to_list():
        date.append(d.strftime('%m/%d/%y'))
    
    table.loc[len(table)] = ['Date']+['']*2+date
    
    for p in pfas_norag:
        cons = []
        con =  data[pfas_norag[p][2]].to_list()
        for c in con:
            if c.startswith('ND'):
                cons.append('-')
            else:
                cons.append(c.split(' ')[0])
        
        
        row = [p,pfas_norag[p][0],pfas_norag[p][1]]+cons
        table.loc[len(table)] = row
    return table

def make_table_gw_edd(data):
    location_names = list(set(data.SAMPLE_POINT_NAME))
    location_names.sort()
    date = []
    for location in location_names:
        if args.source == 'common':
            date_ob = data[data.SAMPLE_POINT_NAME == location].SAMPLE_DATE.iloc[0]
        else:
            date_ob = datetime.datetime.strptime(data[data.SAMPLE_POINT_NAME == location].SAMPLE_DATE.iloc[0],'%m/%d/%Y')
        date.append(date_ob.strftime('%m/%d/%Y'))

    table = pd.DataFrame(['','Interim\nDWS','EPA\nMCL']+location_names).T
    table.loc[1] = ['Date']+['']*2+date
    
    for p in pfas_norag:
        cons = []
        con = []
        long = short2long(p)
        
        
        for location in location_names:
            location_data = data[data.SAMPLE_POINT_NAME == location]
            for lon in long:
                try:
                    if args.source == 'common':
                        con.append( str(location_data[location_data.PARAMETER ==lon].CONCENTRATION.iloc[0]))
                    else:
                        con.append( str(location_data[location_data.PARAMETER_NAME ==lon].CONCENTRATION.iloc[0]))
                except:
                    continue
        for c in con:
            
            if c == 'nan':
                cons.append('-')
            elif c.startswith('ND'):
                cons.append('-')
            elif c == '0.0':    #common geology uses zero when Non-detect
                cons.append('-')
            else:
                cons.append(c)
            
       
        row = [p,pfas_norag[p][0],pfas_norag[p][1]]+cons
        table.loc[len(table)] = row
        
    return table


def make_table_soil_gis(data):
    table = pd.DataFrame(['','2023 RAG\nLTG','2023 RAG\nResidential']+data.FEATURE_NA.to_list()).T
    
    date = []
    for d in data.SAMPLE_DAT.to_list():
        date.append(d.strftime('%m/%d/%y'))
    
    table.loc[len(table)] = ['Date']+['']*2+date
    
    for p in soil:
        cons = []
        con =  data[pfas[p][3]].to_list()
        for c in con:
            if c.startswith('ND'):
                cons.append('-')
            else:
                cons.append(c.split(' ')[0])
        
        
        row = [p,soil[p][0],soil[p][1]]+cons
        table.loc[len(table)] = row
        
    return table

def make_table_soil_edd(data):
    location_names = list(set(data.SAMPLE_POINT_NAME))
    location_names.sort()
    date = []
    for location in location_names:
        if args.source == 'common':
            date_ob = data[data.SAMPLE_POINT_NAME == location].SAMPLE_DATE.iloc[0]
        else:
            date_ob = datetime.datetime.strptime(data[data.SAMPLE_POINT_NAME == location].SAMPLE_DATE.iloc[0],'%m/%d/%Y')
        date.append(date_ob.strftime('%m/%d/%Y'))
    
    table = pd.DataFrame(['','2023 RAG\nLTG','2023 RAG\nResidential']+location_names).T
    
    table.loc[len(table)] = ['Date']+['']*2+date
    
    for p in soil:
        cons = []
        con = []
        long = short2long(p)
        
        for location in location_names:
            location_data = data[data.SAMPLE_POINT_NAME == location]
            for lon in long:
                try:
                    if args.source == 'common':
                        con.append( str(location_data[location_data.PARAMETER ==lon].CONCENTRATION.iloc[0]))
                    else:
                        con.append( str(location_data[location_data.PARAMETER_NAME ==lon].CONCENTRATION.iloc[0]))
                except:
                    continue
        for c in con:
            
            if c == 'nan':
                cons.append('-')
            elif c.startswith('ND'):
                cons.append('-')
            elif c == '0.0':    #common geology uses zero when Non-detect
                cons.append('-')
            else:
                cons.append(c)
            
       
        row = [p,soil[p][0],soil[p][1]]+cons
        
        table.loc[len(table)] = row
        
    return table

def plot_table_gw(table,page=1, landscape=False):
    if landscape:
        fig = pl.figure(figsize=[11,8.5])
    else:
        fig = pl.figure(figsize=[8.5,11])
    fig.clf()
    ax = fig.add_axes([.05,.05,.9,.9])
    
    ax.axis('off')
    
    # tbl = pl_table(ax, table,loc='center', cellLoc='center')
    tbl = ax.table(cellText=table.values, colLabels=None, loc='center',cellLoc='center')
    
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    tbl.scale(1,1.25)
    
    if landscape:
        for i in range(0,table.shape[1]):
            tbl[0,i].set_height(.26)
        for i in range(3,table.shape[1]):
            tbl[0,i].get_text().set_rotation(90)
        for i in range(0,table.shape[0]):
            tbl[i,0].set_width(.10)
            tbl[i,1].set_width(.07)
            tbl[i,2].set_width(.07)
        for j in range(3,table.shape[1]):
            for i in range(0,table.shape[0]):
                tbl[i,j].set_width(.085)
    else:
        for i in range(0,table.shape[1]):
            tbl[0,i].set_height(.23)
        for i in range(3,table.shape[1]):
            tbl[0,i].get_text().set_rotation(90)
        for i in range(0,table.shape[0]):
            tbl[i,0].set_width(.125)
            tbl[i,1].set_width(.1111)
            tbl[i,2].set_width(.1111)
        for j in range(3,table.shape[1]):
            for i in range(0,table.shape[0]):
                tbl[i,j].set_width(.13)
    
    
    # set colors
    # rag_color = np.array([255,255,191]) / 255
    dws_color = np.array([161,215,106]) / 255
    mcl_color = np.array([252,141,89]) / 255
    
    for i in range(0,table.shape[0]):
        # tbl[i,1].set_facecolor(rag_color)
        tbl[i,1].set_facecolor(dws_color)
        tbl[i,2].set_facecolor(mcl_color)
    
    
    
    #set DWS exceedance
    for i,c in enumerate(table.iloc[10,3:].to_list()):
        if c.startswith('-'):
            continue
        if float(c.split(' ')[0]) > float(pfas_norag['Sum of 6'][0]):
            tbl[10,i+3].set_facecolor(dws_color)
        
    # set RAG and MCL exceedance
    for j,p in enumerate(pfas_norag):
        I = j + 2
        for i,c in enumerate( table.iloc[I , 3:].to_list() ):
            if c.startswith('-'):
                continue
            # if pfas[p][0] != '':
            #     if float(c.split(' ')[0]) > float(pfas[p][0]):
            #         tbl[I,i+4].set_facecolor(rag_color)
            if pfas_norag[p][1] != '':
                if float(c.split(' ')[0]) > float(pfas_norag[p][1]):
                    tbl[I,i+3].get_text().set_color(mcl_color)
                    tbl[I,i+3].get_text().set_fontweight('bold')
    
    
    outfile = base_folder +'/../figures/{}_{}'.format(args.site,page)
    for ext in ['.png','.pdf']:
        fig.savefig(outfile + ext)
    
    os.startfile(outfile+'.pdf')



def plot_table_soil(table,page=1):
    fig = pl.figure(figsize=[8.5,11])
    fig.clf()
    ax = fig.add_axes([.05,.05,.9,.9])
    
    ax.axis('off')
    
    # tbl = pl_table(ax, table,loc='center', cellLoc='center')
    tbl = ax.table(cellText=table.values, colLabels=None, loc='center',cellLoc='center')
    
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    tbl.scale(1,1.25)
    
    
    for i in range(0,table.shape[1]):
        tbl[0,i].set_height(.15)
    for i in range(3,table.shape[1]):
         tbl[0,i].get_text().set_rotation(90)
    
    
    # set colors
    ltg_color = np.array([255,255,191]) / 255
    res_color = np.array([161,215,106]) / 255
    
    for i in range(0,table.shape[0]):
        tbl[i,1].set_facecolor(ltg_color) #leach to groundwater
        tbl[i,2].set_facecolor(res_color) #residential 
    
    
    
    #set ltg and resd exceedance        
    for j,p in enumerate(soil):
        I = j + 2
        for i,c in enumerate( table.iloc[I , 3:].to_list() ):
            if c.startswith('-'):
                continue
            
            if float(c.split(' ')[0]) > float(soil[p][0]):
                tbl[I,i+4].set_facecolor(ltg_color)
            
            if float(c.split(' ')[0]) > float(soil[p][1]):
                tbl[I,i+4].get_text().set_color(res_color)
                tbl[I,i+4].get_text().set_fontweight('bold')
    
    pl.tight_layout()
    outfile = base_folder +'/../figures/{}_soil_{}'.format(args.site,page)
    for ext in ['.png','.pdf']:
        fig.savefig(outfile + ext)
        print('saving: {}'.format(outfile+ext))
    
    os.startfile(outfile+'.pdf')


def main(args):
    
    # compounds to include all within sum of 6, all with RAGs
    # sum of six compounds : PFOA, PFOS, PFHxS, PFNA, PFHpA PFDA
    # RAG and EPA MCL in ppb
    
    if args.source == 'gis':

        if args.s:
            data = gpd.read_file(paths.soil_polygons)
            data = data[data['EGAD_SITE_'] == args.site]
            data = data.sort_values(by='FEATURE_NA')
        else:
            data = gpd.read_file(paths.sample_locations)
            data = data[data['EGAD_SITE_'] == args.site]
            data = data.sort_values(by='FEATURE_NA')   
        no_samps = len(data)
    
    elif args.source =='edd':

        try:
            print('trying .xls')
            data = edd.load_edd(paths.edd +'/' + args.site+'_m60.xls')
            data = data[data.LAB_SAMPLE_ID.str.startswith('L')]
        except:
            print('.xls not found, trying .xlsx')
            data = gpd.read_file(paths.edd +'/' + args.site+'_m60.xlsx')      
    
        if args.s:
            data = data[data.SAMPLE_TYPE == 'SL']
        else:
            data = data[data.SAMPLE_TYPE == 'GW']
        data = data.sort_values(by='SAMPLE_POINT_NAME')
        no_samps = len(set(data.SAMPLE_POINT_NAME))
        
    
    elif args.source == 'common':

        data = gpd.read_file(paths.common +'/' + args.site+'.xlsx',layer='Data')
        if args.s:
            data = data[data.SAMPLE_TYPE == 'SL']
        else:
            data = data[data.SAMPLE_TYPE == 'GW']
        data = data.sort_values(by='SAMPLE_POINT_NAME')
        no_samps = len(set(data.SAMPLE_POINT_NAME))
        
 
    print('Number of sample locations:', no_samps)
    if no_samps == 0:
        print('')
        print('No sample locations: Table not printed.')
        print('')
    
    elif no_samps < 7: # one table portrait
        if args.s:
            if args.source == 'gis':
                table = make_table_soil_gis(data)
            else:
                table = make_table_soil_edd(data)
            plot_table_soil(table)
        else:
            if args.source == 'gis':
                table = make_table_gw_gis(data)
            else:
                table = make_table_gw_edd(data)
            plot_table_gw(table)
    
    elif no_samps < 11: # plot landscape single row
        if args.s:
            if args.source == 'gis':
                table = make_table_soil_gis(data)
            else:
                table = make_table_soil_edd(data)
            plot_table_soil(table,landscape=True)
        else:
            if args.source == 'gis':
                table = make_table_gw_gis(data)
            else:
                table = make_table_gw_edd(data)
            plot_table_gw(table,landscape=True)
    else: #greater than 10 sample locations n number of landscape pages
        n_pages = int( np.ceil( len(data)/10 ) )
        if args.source == 'gis':
            for n in range(n_pages):
                ii = n * 10
                table = make_table_gw_gis(data.iloc[ii:ii+10])
                plot_table_gw(table,page = n+1,landscape=True)
        

    
   


if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('site' , help='site ID; sequence number or filename')
    parser.add_argument('source', default='gis', choices = ['gis','common','edd'])
    parser.add_argument('-s', action='store_true', help='make table for soil')
    args = parser.parse_args()
    main(args)