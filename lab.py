# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 14:33:35 2025

@author: Lucas.Beem



parse lab tracking xcel and print info
The following inputs can be used
<site name>
<sample location>
'all'
'chrono'

"""

import argparse
import sys
import os
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'lookup'))

import make_site
import paths 
import edd_utils as edd
import glob

def basic_print(df,test=None):
    colh = df.columns
    
    col0 = df[colh[0]].str.len().max() + 2      # name
    col1 = int(df[colh[1]].str.len().max() + 2) # sample ID
    col2 = df[colh[2]].str.len().max() + 2      # location
    col3 = 11
    
    print('')
    for n in range(len(df)):
        print_str= []
        print_str.append( df.iloc[n,0].ljust(col0))
        print_str.append( df.iloc[n,1].ljust(col1))
        print_str.append( df.iloc[n,2].ljust(col2))
        print_str.append( df.iloc[n,3].strftime('%m/%d/%y').ljust(col3))
        
        if test is not None:
            print_str.append( "  ".join(word.upper() for word in test[n]))
            print('{}{}{}{}{}'.format(*print_str))
        else:
            print('{}{}{}{}'.format(*print_str))
    print('')

def main(args):

    
    df,df_info,_,_ = make_site.load_from_pickle(paths.site_pickle)
    
    df['Site Name'] = df['Site Name'].str.upper()
    df['Loc.'] = df['Loc.'].str.upper()

    if args.site == 'all':
        #sorted by site
        df = df.sort_values(by='Site Name')
        basic_print(df)
    elif args.site == 'chrono':
        # sorted by date
        df =df.sort_values(by='Sample Date')
        basic_print(df)
    elif args.site.upper() in df['Site Name'].to_list():
        # print all samples for site
        df = df[df['Site Name'] == args.site.upper()]
        df =df.sort_values(by='Sample Date')
        test = []
        for row in df.iterrows():
            samp = row[1].iloc[1]
            samp_short = samp.split('-')[0]
            edd_path = glob.glob( paths.edd + '/{}_m60.xls*'.format(samp_short))
            
            try:
                edd_df = edd.load_edd(edd_path[0])
                test.append(edd.which_tests(edd_df,samp))
            except: 
                test.append([])
        df['test'] = test
        basic_print(df,test=test)
    elif args.site.upper() in df['Loc.'].to_list():
        df = df[df['Loc.'] == args.site.upper()]
        df =df.sort_values(by='Sample Date')
        test = []
        for row in df.iterrows():
            samp = row[1].iloc[1]
            samp_short = samp.split('-')[0]
            edd_path = glob.glob( paths.edd + '/{}_m60.xls*'.format(samp_short))
            
            try:
                edd_df = edd.load_edd(edd_path[0])
                test.append(edd.which_tests(edd_df,samp))
            except: 
                test.append([])
        df['test'] = test
        basic_print(df,test=test)
        
    # site id provided
    
    # if (args.site != 'all') and (args.site != 'chrono'):
    #     args.site = utils.shortcut(args.site)
    #     if not utils.in_database(df_info, args.site):
    #         print('site ID {} not in database'.format(args.site))
    #         exit()
    #     if not utils.has_samples(df, df_info, args.site):
    #         print('site ID {} has no samples in database'.format(args.site))
    #         exit()
    #     sitename = utils.get_id(df_info,args.site,'name')
    #     df = df[df['Site Name'] == sitename.title()]
    
    # if args.site == 'all':
        
    # if args.site == 'chrono':
    #     df =df.sort_values(by='Sample Date')
    
    # # get test type(s)
    # test = []
    # for row in df.iterrows():
    #     samp = row[1].iloc[1]
    #     samp_short = samp.split('-')[0]
    #     edd_path = paths.edd + '/{}_m60.xls'.format(samp_short)
    #     try:
    #         edd = pd.read_excel(edd_path)
    #         edd = edd.fillna('ND')
    #         test.append(parse._edd_which_tests(edd,samp))
    #     except: 
    #         test.append([])
    
    # col0 = df[colh[0]].str.len().max() + 2      # name
    # col1 = int(df[colh[1]].str.len().max() + 2) # sample ID
    # col2 = df[colh[2]].str.len().max() + 2      # location
    # col3 = 11                                   # date
    # print('')
   
    # for n in range(len(df)):
    #     print_str= []
    #     print_str.append( df.iloc[n,0].ljust(col0))
    #     print_str.append( df.iloc[n,1].ljust(col1))
    #     print_str.append( df.iloc[n,2].ljust(col2))
    #     print_str.append( df.iloc[n,3].strftime('%m/%d/%y').ljust(col3))
    #     if len(test) == 0:
    #         print_str.append('--')
    #     else:
    #         print_str.append( "  ".join(word.upper() for word in test[n]))
        
    #     print('{}{}{}{}{}'.format(*print_str))


    # print('\n\n')
    
    
if __name__=="__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument('site' , nargs= '?' , default='all', help='if no args: list all, if site id (i.e. seq, name, spill number) list only that site')

    args = parser.parse_args()

    main(args)
