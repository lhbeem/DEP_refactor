# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 15:11:28 2026

@author: Lucas.Beem


EDD manipulation utilities


"""

import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(base_folder+'/lookup')

import paths
import pandas as pd 
import datetime

import rags
import edd_compounds as edd_comp



def brwmtable2edd(pth,edd_num,site):
    #convert BRWM table (generated from egad export)
    # into an 'edd' that can be used with edd parser tools
    # pth : path to brwm table .xls
    
    data = pd.read_excel(pth)
    data = data.fillna('NA')
    
    # cols are consistent with load_edd 
    cols = edd_cols()
    compounds = data.iloc[0, 4:]
    sls = data.iloc[3:,1] # sample locations 
 
    # truncate to date
    for i in range(len(data)):
        if isinstance( data.iloc[i,2] ,datetime.date ):
            dd = data.iloc[i,2]
            data.iloc[i,2] = datetime.date(dd.year,dd.month,dd.day)
    dates = data.iloc[3:,2]
    
    
    data_rows = []
    n= 0
    df = pd.DataFrame({'site': sls.to_list(), 'date': dates.to_list()})
    df_unique = df[['site', 'date']].drop_duplicates()
    
    for aa in df_unique.iterrows():
        if aa[1].site == 'NA':
            continue
        df = data[data.iloc[:,1] == aa[1].site]
        df = df[df.iloc[:,2] == aa[1].date]
    
        results = df.iloc[:, 4:]
        samp_id = '{}-{:02}'.format(edd_num,n+1)
        location = aa[1].site
        date = aa[1].date
        
        for row in results.iterrows():
            row = row[1]
            for j , comp in enumerate(compounds):
                con = row.iloc[j]
                if isinstance(con,str):
                    if con == 'NA':
                        continue
                    elif '<' in con:
                        con = ''
                    elif 'J' in con:
                        con = float(con.split('J')[0])
                data_rows.append([site,location,samp_id,date.strftime('%m/%d/%Y'),'GW',comp,con])
        
        n += 1
    
    df = pd.DataFrame(data_rows,columns = cols)
    
    out = paths.edd+'/'+edd_num+'_m60.xlsx'
    df.to_excel(out, index=False)


def edd_cols():
    # relvent columns from edd
    # determines how edd are loaded and the construction of brwmtable and 
    # common geology conversion 
    return ['PROJECT','SAMPLE_POINT_NAME','LAB_SAMPLE_ID','SAMPLE_DATE','SAMPLE_TYPE','PARAMETER_NAME',
            'CONCENTRATION']

def is_sample_present(df,sample):
    
    if sample in df['LAB_SAMPLE_ID'].tolist():
        return True
    else:
        return False
    
    
def load_edd(path):
    # path is path to the excel file
    # code loads and makes a dataframe that will be consistent across 
    # the variations present in EDDs and exports only 'important' columns
    
    df = pd.read_excel(path)
    df = df.fillna('ND')
    df.columns = df.columns.str.upper()
    
    if 'PROJECT/SITE' in df.columns:
        df.rename(columns = {'PROJECT/SITE' : 'PROJECT'}, inplace=True)
    if 'RESULT_TYPE_CODE' in df.columns:
        df = df[df['RESULT_TYPE_CODE'] == 'TRG']
    if 'SAMPLE_POINT_NAME' in df.columns:
        df = df[df['SAMPLE_POINT_NAME'] != 'QC']

    columns_to_keep = edd_cols()
    
    df = df.loc[:,columns_to_keep] 
    df = df.stack().apply(lambda x: x.strip() if isinstance(x, str) else x).unstack() # remove trailing spaces (strip on numeric data results in a nan)
    return df


def which_tests(df,sample):
    # returns a list of the test types present
    # df:       data frame from the edd
    # sample:   sample number with subsample indicator
    if not is_sample_present(df, sample):
        return [False,0]
    
    test = []
    
    df = df[df['LAB_SAMPLE_ID'] == sample]#space after sample number in edd
    
    compounds = df['PARAMETER_NAME'].to_list()

    if ('PERFLUOROOCTANESULFONIC ACID (PFOS)' in compounds) or ('PERFLUOROOCTANESULFONIC ACID' in compounds) and ('PFAS, TOTAL (6)' in compounds) or ('SUM OF 6 PFAS (PFHPA + PFHXS + PFOA + PFNA + PFOS + PFDA)' in compounds):
        try:
            samp_type = df[df['PARAMETER_NAME'] == 'PERFLUOROOCTANESULFONIC ACID (PFOS)'].SAMPLE_TYPE.to_list()
        except:
            samp_type = df[df['PARAMETER_NAME'] == 'PERFLUOROOCTANESULFONIC ACID'].SAMPLE_TYPE.to_list()
        if 'GW' in samp_type:
            test.append('pfas')
        if 'SL' in samp_type:
            test.append('pfas_soil')
    
    if ('TOTAL ORGANIC CARBON' in compounds) and ('SULFATE' in compounds):
        if ('CHEMICAL OXYGEN DEMAND' in compounds) and ('CHROMIUM, TOTAL' in compounds):
            test.append('landfill_long')
        else: 
            test.append('landfill_short')
    if 'C9-C12 ALIPHATICS, ADJUSTED' in compounds:
        test.append('vph')
    if 'C9-C18 ALIPHATICS' in compounds:
        test.append('eph')
    if 'BROMOFORM' in compounds:
        test.append('voc')
    if ('TOTAL HARDNESS ' in compounds) or ('Hardness as calcium carbonate' in compounds):
        test.append('pot')
    if 'PH' in compounds:
        test.append('field')
    return test 
    

def edd_compound_parse(df,sample,test):
    # sort the dataframe to just the results for the supplied sample number
    res = df[ (df['LAB_SAMPLE_ID'] == sample)]
    # res = res [ res['RESULT_TYPE_CODE'] == 'TRG' ]
    # res = res [res['QC_TYPE'] == 'NA' ]
    compounds = rags.test_compounds[test]
    
    shortnames = []
    for row in res.iterrows():
        shortnames.append(edd_comp.edd_compound[row[1]['PARAMETER_NAME'].upper()])
    
    results = []
    for comp in compounds:
        rag = rags.all_gw[comp]
        if comp in shortnames: # is test compound in the sample results
            I = shortnames.index(comp)
            row = res.iloc[I]
            
            con = row.CONCENTRATION
            
            # occationally there is a precision issue with the concentration. 
            if len(str(con))> 6:       
                if float(con)> 1:
                    con = str(round(float(con),2))
                if float(con)< 1:
                    con = str(round(float(con),4))
            
            if rag == '-':
                label = ''
            elif con == 'ND':
                label = ''
            elif float(rag) < float(con):
                label = '*'
            else:
                label = ''
                
            results.append([comp,str(con),rag,label])
        else:
            results.append([comp,'',rag,''])
       
    return results
