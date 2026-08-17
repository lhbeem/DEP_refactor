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

import argparse
import numpy as np
import pandas as pd
import geopandas as gpd
from matplotlib import pylab as pl



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
    
# name_convert = {'PERFLUOROOCTANE SULFONIC ACID' : 'PFOS',
#                 'PERFLUOROOCTANOIC ACID' : 'PFOA',
#                 'HEXAFLUOROPROPYLENE OXIDE DIMER ACID':'HFPO-DA',
#                 }


def make_table(data):
    table = pd.DataFrame(['','2023\nRAG','Interim\nDWS','EPA\nMCL']+data.FEATURE_NA.to_list()).T
    
    date = []
    for d in data.SAMPLE_DAT.to_list():
        date.append(d.strftime('%m/%d/%y'))
    
    table.loc[len(table)] = ['Date']+['']*3+date
    
    for p in pfas:
        cons = []
        con =  data[pfas[p][3]].to_list()
        for c in con:
            if c.startswith('ND'):
                cons.append('-')
            else:
                cons.append(c.split(' ')[0])
        
        
        row = [p,pfas[p][0],pfas[p][1],pfas[p][2]]+cons
        table.loc[len(table)] = row
    return table


def make_table_soil(data):
    location_names = list(set(data.SAMPLE_POINT_NAME))
    location_names.sort()
    date = []
    for location in location_names:
        date.append(data[data.SAMPLE_POINT_NAME == location].SAMPLE_DATE.iloc[0].strftime('%m/%d/%Y'))
    
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
                    con.append( str(location_data[location_data.PARAMETER_NAME ==lon].CONCENTRATION.iloc[0]))

                except:
                    continue
        for c in con:
            if c == 'nan':
                cons.append('-')
            else:
                cons.append(c)
        
        
        row = [p,soil[p][0],soil[p][1]]+cons

        table.loc[len(table)] = row
        
    return table



def plot_table(table,page=1):
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
        tbl[0,i].set_height(.23)
    for i in range(4,table.shape[1]):
        tbl[0,i].get_text().set_rotation(90)
    for i in range(0,table.shape[0]):
        tbl[i,0].set_width(.125)
        tbl[i,1].set_width(.1111)
        tbl[i,2].set_width(.1111)
        tbl[i,3].set_width(.1111)
    for j in range(4,table.shape[1]):
        for i in range(0,table.shape[0]):
            tbl[i,j].set_width(.125)
    
    
    # set colors
    rag_color = np.array([255,255,191]) / 255
    dws_color = np.array([161,215,106]) / 255
    mcl_color = np.array([252,141,89]) / 255
    
    for i in range(0,table.shape[0]):
        tbl[i,1].set_facecolor(rag_color)
        tbl[i,2].set_facecolor(dws_color)
        tbl[i,3].set_facecolor(mcl_color)
    
    
    
    #set DWS exceedance
    for i,c in enumerate(table.iloc[12,4:].to_list()):
        if c.startswith('-'):
            continue
        if float(c.split(' ')[0]) > float(pfas['SUM OF 6'][1]):
            tbl[12,i+4].set_facecolor(dws_color)
        
    # set RAG and MCL exceedance
    for j,p in enumerate(pfas):
        I = j + 2
        for i,c in enumerate( table.iloc[I , 4:].to_list() ):
            if c.startswith('-'):
                continue
            if pfas[p][0] != '':
                if float(c.split(' ')[0]) > float(pfas[p][0]):
                    tbl[I,i+4].set_facecolor(rag_color)
            if pfas[p][2] != '':
                if float(c.split(' ')[0]) > float(pfas[p][2]):
                    tbl[I,i+4].get_text().set_color(mcl_color)
                    tbl[I,i+4].get_text().set_fontweight('bold')
    
    
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
    outfile = base_folder +'/../figures/{}_soil_{}'.format(args.sample,page)
    for ext in ['.png','.pdf']:
        fig.savefig(outfile + ext)
    
    os.startfile(outfile+'.pdf')


def main(args):
    
    # compounds to include all within sum of 6, all with RAGs
    # sum of six compounds : PFOA, PFOS, PFHxS, PFNA, PFHpA PFDA
    # RAG and EPA MCL in ppb

    if not args.s:
        print('ToDo: compete code for GW sample table')
        exit()
        data = pd.read_excel(paths.sample_locations)
        data = data[data.SAMPLE_TYPE == 'GW']
        point_names = set(data.SAMPLE_POINT_NAME)


        if len(point_names) < 6: # one table
            table = make_table(data)
            plot_table(table)
        elif (len(point_names) > 5) and (len(point_names) <= 10): # split between two tables 
            length = int(round(len(point_names)/2))
    
            table1 = make_table(data.iloc[:length,:])
            table2 = make_table(data.iloc[length:,:])
            plot_table(table1)
            plot_table(table2,page=2)
        elif (len(point_names) > 11):
            n_pages = int( np.ceil( len(data)/5 ) )
            for n in range(n_pages):
                ii = n * 5
                table = make_table(data.iloc[ii:ii+5])
                plot_table(table,page = n+1)

    elif args.s:
        
        data = gpd.read_file(paths.edd +'/' + args.sample+'_m60.xlsx')
        data = data[data.SAMPLE_TYPE == 'SL']
        data = data.sort_values(by='SAMPLE_POINT_NAME')
        point_names = set(data.SAMPLE_POINT_NAME)
        
        
        if len(point_names) < 6:
            table = make_table_soil(data)
            plot_table_soil(table)
        elif (len(point_names) > 5) and (len(point_names) <= 10): # split between two tables 
            length = int(round(len(point_names)/2))
    
            table1 = make_table_soil(data.iloc[:length,:])
            table2 = make_table_soil(data.iloc[length:,:])
            plot_table_soil(table1)
            plot_table_soil(table2,page=2)
        elif (len(point_names) > 11):
            n_pages = int( np.ceil( len(point_names)/5 ) )
            for n in range(n_pages):
                ii = n * 5
                table = make_table_soil(data.iloc[ii:ii+5])
                plot_table_soil(table,page = n+1)


if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('sample' , help='sample number')
    parser.add_argument('-s', action='store_true', help='make table for soil')
    args = parser.parse_args()
    main(args)