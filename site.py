# -*- coding: utf-8 -*-
"""
Created on Mon May  5 09:11:23 2025

@author: Lucas.Beem


todo:
export feature to csv for easy sharing of all data?

"""





#%% intro and load modules
# use the data list to make a dataframe.
# dateframe is called to output search quieries 


import numpy as np
import argparse
import sys
import os
os.system("") #makes color work for some reason
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'lookup'))
import make_site as utils
import paths

#%% code
class Color:
        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        WHITE = '\033[37m'
        RESET = '\033[0m'  # Resets all formatting (color, bold, etc.)

# list all towns in dataframe
def list_towns(df):
    print('\n\nTowns with sites:\n')
    towns = np.unique(df.town)
    for town in towns:
        print(town)
    print('\n\n')



#list all spills in given town 
def in_town(t,df):
    print('\n\nSites in {}:\n'.format(t.title()))
    subset = df[df.town == t.title()]
    for n in subset.name:
        print(n)
    if subset.name.empty:
        print('None')
    print('\n\n')
    

# list all site info for a given spill (either by seq# or site name)
def get_site(prompt,df,f,con,folders,contacts):
    if f == 'name':
        site = df[df.name == prompt]
    if f == 'seq':
        site = df[df.seq == prompt]
    if f == 'spill':
        site = df[df.spill == prompt]
        
    print('\n\n')
    print('{:14}{}'.format('name:',site.name.iloc[0]))
    
    
    if isinstance(site.seq.iloc[0],float) :
        seq_str = str(int(site.seq.iloc[0]))
    else:
        seq_str = 'None'
    
    print('{:14}{}'.format('seq#:',seq_str))
    print('{:14}{}'.format('town:',site.town.iloc[0]))
    print('{:14}{}'.format('Site type:',site.type.iloc[0]))
    
    if site.spill.iloc[0] is None:
        print('Spill Number: None')
    else:
        print('{:14}{}'.format('Spill Number:', site.spill.iloc[0]))
    
    if site.type.iloc[0] in ['last','lust','mys']:
        print('{:14}{}'.format('Responder:',site.resp_pm.iloc[0]))
    else:
        print('{:14}{}'.format('Project Mgt:',site.resp_pm.iloc[0]))
    
    
    sitename= site.name.iloc[0].lower().replace(" ","")
    folds = folders[sitename]
    if folds is None:
        print('\nFolders: None')
    else:
        print('\nFolders:')
        for fold in folds:
            if fold == 'None':
                continue
            else:
                print(fold)
    if con:
        cons = contacts[sitename]

        
        if cons is None:
            print('\nContacts: None \n')
        else:
            print('\nContacts:\n')
            for key in cons.keys():
                only_contact(cons[key])
    print('\n\n')

# print contant info
def only_contact(con):

    if con is None:
        print('None')
    else:
        print('location: {}'.format(con[1]) )
        print('')
        for address in con[2]:
            print(address)
        print('')
        for phone in con[3]:
            print('Phone: {}'.format(phone))
        for email in con[4]:
            print('Email: {}'.format(email))
        print('Contact Preference: {}'.format(con[5][0]))
        print('Report Format Preference: {}'.format(con[6][0]))

        note = con[-1][0]
        if note != 'None':
            print('\n')
            for i in range(0,len(note),60):
                print(note[i:i+60])
        print('\n')





# list basic info off each spill in dataframe
def list_(df):
    
    col0 = df.name.str.len().max() + 2
    
    print('\n\n')
    print('{:{col0}}{:18}{:10}{:18}{:10}{}'.format('NAME','TOWN','SEQ#','SPILL#','TYPE','PM/RESPOND',col0=col0))
    print('') # prints empty line
    
    
    df = df.sort_values(by='closed',ascending=False)
    
    for name,town,seq,spill,types,pm,close in zip(df.name,df.town, df.seq, df.spill, df.type, df.resp_pm,df.closed):
        if seq != 'None':
            seq = str(int(seq))
        if close == 'y':
            print(Color.GREEN + '{:{col0}}{:18}{:<10}{:18}{:10}{}'.format(name, town, seq, str(spill),types,pm,col0=col0) + Color.RESET)
        else:
            print('{:{col0}}{:18}{:<10}{:18}{:10}{}'.format(name, town, seq, str(spill),types,pm,col0=col0))
   
    print('\n\n')



def main(args):    
    
    _,df,folders,contacts = utils.load_from_pickle(paths.site_pickle)
        
     
    # list all info for a given site
    if args.site == 'all':
        list_(df)
    elif args.site.lower() in ['last','lust','landfill','brown','pfas','vrap','mys','rcra']:
        sub = df[df.type == args.site.lower()]
        list_(sub)
    else:
        
        sitename = utils.shortcut(args.site)
        
        try: 
            get_site(sitename.title(),df,'name',args.c,folders,contacts)
        except:
            try:
                get_site(int(sitename),df,'seq',args.c,folders,contacts)
            except:
                try:
                    get_site(sitename.title(),df,'spill',args.c,folders,contacts)
                except:
                    print ('\nsite ID ''{}'' not in database\n'.format(args.site))
        
if __name__=="__main__":
    parser= argparse.ArgumentParser()
    
    help_text = ['list all site info for a given site (seq# , site name, or spill#) ' +
                'If no argument supplied then lists all. Or a specific site type ' +
                'Can be supplied (last,lust,mys, landfill, pfas,brown,vrap, rcra)']
    
    
    parser.add_argument('site',nargs = '?', default = 'all',help=help_text )
    parser.add_argument('-c', action='store_true', help='print contacts info')
    args = parser.parse_args()
    
    main(args)
