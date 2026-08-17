# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 22:53:49 2026

@author: Lucas.Beem


makes the site and lab lists
plus utils for parsing the site and lab lists

"""

import os
import sys
import numpy as np
import geopandas as gpd
import pandas as pd
import xlwings
import pickle

base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(base_folder+'/lookup')
import paths
import argparse


def load_from_pickle(path):
    data = pd.read_pickle(path)
    # lab, site, folder, contacts
    return data[0], data[1],data[2], data[3]


def load_lab_xlw(path,path2):
    # path to xls
    # path2 to brwm_table location list
    with xlwings.App(visible=False):
        book = xlwings.Book(path)
        sheet = book.sheets["Data"]
        df = sheet.range("A1:D500").options(pd.DataFrame, 
                                        header=1,index=False,expand='table').value
        
    
    df = df.loc[:,['Site Name','Sample ID','Loc.','Sample Date']]
    df = df.fillna('None')
    df['Site Name'] = df['Site Name'].str.strip()
    df['Sample ID'] = df['Sample ID'].str.strip()
    
    df['Loc.'] = df['Loc.'].str.strip()
    df['Loc.'] = df['Loc.'].str.replace(" ","")
    df['Loc.'] = df['Loc.'].str.lower()
    
    # append brwm_table convertions
    with xlwings.App(visible=False):
        book = xlwings.Book(path2)
        sheet = book.sheets["Sheet1"]
        df2 = sheet.range("A1:D500").options(pd.DataFrame, 
                                        header=1,index=False,expand='table').value
   
    df2 = df2.fillna('None')
    df2['Loc.'] = df2['Loc.'].str.strip()
    df2['Loc.'] = df2['Loc.'].str.replace(" ","")
    df2['Loc.'] = df2['Loc.'].str.lower()
    
    df2['Sample Date'] = pd.to_datetime(df2['Sample Date'],format="%m/%d/%Y")
    
    df3 = pd.concat([df, df2], ignore_index=True)
    
    
    return df3

def load_site_xlw(path):
    
    with xlwings.App(visible=False):
        book = xlwings.Book(paths.xls)
        sheet = book.sheets["Sites"]
        df = sheet.range("A1:D100").options(pd.DataFrame, 
                                        header=1,index=False,expand='table').value
        
    df = df.fillna('None')
    sites = df.loc[:,['seq','town','name','spill','type','resp_pm','closed','x','y']]
    fold = df.loc[:,['name','folder1','folder2','folder3']]
    folder = {}
    for row in fold.iterrows():
        key = row[1]['name'].lower().replace(" ","")
        folder[key] = [row[1]['folder1'],row[1]['folder2'],row[1]['folder3']]
    
    return sites,folder

def is_mys(siteID):
    # siteID is seq, sitename, or spill_num
    _,df,_,_ = load_from_pickle(paths.site_pickle)
    sitename = get_id(siteID,'name')
    if df[df['name'] == sitename]['type'].iloc[0] == 'mys':
        return True
    else:
        return False 
    
    
def is_lust(siteID):
    # siteID is seq, sitename, or spill_num
    _,df,_,_ = load_from_pickle(paths.site_pickle)
    sitename = get_id(siteID,'name')
    if df[df['name'] == sitename]['type'].iloc[0] == 'lust':
        return True
    else:
        return False

def get_id(prompt,outs):
    # converts identificaion
    # prompt: exising id
    # outs: desired id (spill,name,seq)
    
    _,df,_,_= load_from_pickle(paths.site_pickle)
    df_name = df[df['name'] == prompt.title()]
    df_spill = df[df['spill'] == prompt]
    if prompt.isdecimal():
        df_seq = df[df['seq'] == int(prompt)]
    else:
        df_seq = pd.DataFrame()
    
    df_out = None
    if not df_name.empty:
        df_out = df_name
    elif not df_spill.empty:
        df_out = df_spill
    elif not df_seq.empty:
        df_out = df_seq
    
    if df_out is None:
        return df_out
    else:
        return df_out[outs].iloc[0]  
    




def name_from_sample(sample):
    df,_,_,_= load_from_pickle(paths.site_pickle)

    if '-' in sample:
        name = df[df['Sample ID'] == sample].loc[:,'Site Name'].tolist()[0]
    else:
        #sample number without subsample
        df['Sample ID'] = df['Sample ID'].str.split('-').str[0]
        name = df[df['Sample ID'] == sample].loc[:,'Site Name'].tolist()[0]
    return name



def site_from_location(location):
    
    # return site name from the assocaited sample location
    # df is the Data sheet datafrom from Spill_lab_tracking.xls
    # location is sample location shortname
    df,_,_,_ = load_from_pickle(paths.site_pickle)
    series = df[df['Loc.'] == location]['Site Name']
    if series.empty:
        sitename = None
    else:
        sitename = df[df['Loc.'] == location]['Site Name'].iloc[0].lower()
    
    
    return sitename


def shortcut(ID):
    # check for an existance of a shortcut name
    short = {'nylf' : "North Yarmouth",
             'comb' : 'comb block',
             'alpha': 'alpha one',
             'dental': 'Fryeburg Dental',
             'milliken': 'milliken Road',
             'johnson' : 'Johnson Mountain',
             'king' : 'King-Verrier',
             'lowell' : 'lowell cove',
             'steep' : 'Steep falls',
             'johns' : 'johns store'
             }
    
    if ID.lower() in short.keys():
        out = short[ID.lower()]
    else:
        out = ID
    return out



def load_contact_xlw(path):
    with xlwings.App(visible=False):
        book = xlwings.Book(paths.xls)
        sheet = book.sheets["Contacts"]
        df = sheet.range("A1:D100").options(pd.DataFrame, 
                                        header=1,index=False,expand='table').value
    
        sheet = book.sheets["sites"]
        names = sheet.range("A1:D100").options(pd.DataFrame, 
                                        header=1,index=False,expand='table').value
    
    names = names['name'].tolist()
    
    df = df.fillna('None')
    
    contacts = {}
    for name in names:
        key = name.lower().replace(" ","")
        conts = df[df['name'] == name]
        if len(conts) > 0:
            cons = {}
            for c in conts.iterrows():
                c = c[1]
                k = c['loc shortname'].lower()
                address = c['address'].split(':')
                
                phone = c['phone'].split(',')
                email = c['email'].split(',')
                con_pref = [c['contact pref']]
                report_pref = [c['report pref']]
                notes = [c['notes']]
                    
                
                
                cons[k] = [c['salutation'],c['longname'],address,phone,email,con_pref,report_pref,notes]
            contacts[key] = cons
        else:
            contacts[key] = None
    
    return contacts


def make_pickle(path,path2):
    lab = load_lab_xlw(path,path2)
    site,folder = load_site_xlw(path)
    contacts = load_contact_xlw(path)

    dataframes_list = [lab, site, folder, contacts]
 
    with open(paths.site_pickle, 'wb') as f:
        pickle.dump(dataframes_list, f)
    

def get_sample_numbers(df,location):
    # gets the sample numbers associated with a sample location
    # df is the Data sheet from tracking xls
    # location is the location short name
    
    # slice by location
    samples = df[df['Loc.'] == location.lower()]['Sample ID'].tolist()
    dates = df[df['Loc.'] == location.lower()]['Sample Date'].tolist()
    return samples, dates 



def make_pts():
    ### making geopackage from lab_track rows 
    _,sites,_,_ = load_from_pickle(paths.site_pickle)

    pfas = []
    brown_vrap = []
    petrol = []
    landfill = []
    mys = []

    for site in sites.iterrows():
        site = site[1]
        if site.type in ['last','lust']:
            if site.x != 'None':
                petrol.append([site['name'],site.x,site.y])
        elif site.type in ['pfas']:
            if site.x != 'None':
                pfas.append([site['name'],site.x,site.y])
        elif site.type in ['landfill']:
            if site.x != 'None':
                landfill.append([site['name'],site.x,site.y])
        elif site.type in ['mys']:
            if site.x != 'None':
                mys.append([site['name'],site.x,site.y])
        elif site.type in ['brown','vrap']:
            if site.x != 'None':
                brown_vrap.append([site['name'],site.x,site.y])

    out = paths.site_pts


    layer_names = ['PFAS Sites','VRAP Brownfield Sites', 'Petrol Sites', 'Landfill Sites', 'Mystery Sites']
    for i,lst in enumerate([pfas,brown_vrap,petrol,landfill,mys]):
        lst = np.array(lst)

        geometry = gpd.points_from_xy(lst[:,1], lst[:,2])
        
        gdf = gpd.GeoDataFrame(pd.DataFrame(lst[:,0],columns=['Name']), geometry=geometry, crs="EPSG:26919")
        
        
        if i == 0:
            gdf.to_file(out, layer=layer_names[i], driver="GPKG",mode='w')
        else:
            gdf.to_file(out, layer=layer_names[i], driver="GPKG",mode='w')
            
    
    
    

def main(args):
    # make pickle from lab_tracking and brwm_location_list
    make_pickle(paths.xls,paths.location_list)
    print('Pickle Generated: '+ paths.site_pickle)
    # make geopackage of site_pickle
    make_pts()
    print('saved: ' + paths.site_pts)
    


if __name__=="__main__":
    parser= argparse.ArgumentParser()
        
    parser.add_argument('-make', default = True, )
    
    args = parser.parse_args()
    
    
    
    main(args)