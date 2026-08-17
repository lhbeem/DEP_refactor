# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 16:24:43 2025

@author: Lucas.Beem


compare sample results to RAGs using EDD


"""


import argparse

import os 
os.system("") #makes color work for some reason
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'lookup'))
import rags as rg
import edd_utils as edd
import paths 
import make_site as make

import glob 
import numpy as np



## If passed a sample number it will do just the the one. If it is passed 
# a location it will do all for that location. 


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



def display_rags(test):

    if test == 'history':
        rags = rg.historic_rag_gw
        keys = list(rags.keys())
        keys.sort()
        
        print('\n')
        print('Petroluem GW RAGs (ppb)')
        print('')
        print('{:35}{:8}{:8}{:8}{:8}{:8}'.format('','2023','2021','2018','2016','2013'))
        for key in keys:
            print('{:30}{:8}{:8}{:8}{:8}{:8}'.format(key,*rags[key]))
        print('\n')
        return
    elif test == 'pfas':
        title = 'PFAS RAGs (ppt)'
        medium = 'gw'
    elif test == 'pot':
        title = 'Potability RAGs (ppb)'
        medium = 'gw'
    elif test =='pfas_soil':
        title = 'PFAS leaching to Groundwater and Residential Soil (ppm)'
        test = 'pfas'
        medium = 'soil'
    elif test == 'soil':
        title = 'Petroleum leaching to groundwater (ppm)'
        medium = 'soil'
    elif test == 'vph':
        title = 'VPH RAGs (ppb)'
        medium = 'gw'
    elif test == 'eph':
        title = 'EPH RAGs (ppb)'
        medium = 'gw'
    elif test == 'voc':
        title = 'VOC RAGs (ppb)'
        medium = 'gw'
    elif test =='landfill_short':
        title = 'Landfill Shortlist RAGs (ppb)'
        medium = 'gw'
    elif test == 'landfill_long':
        title = 'Landfill Longlist RAGs (ppb)'
        medium = 'gw'
    
    if medium == 'gw' :
        compounds = rg.test_compounds[test]
        compounds.sort()     
        rags = []
        for compound in compounds:
            rags.append(rg.all_gw[compound])
        print('')
        print(title)
        print('')
        for i in range(len(compounds)):
            print('{:30}{:8}'.format(compounds[i],rags[i]))
        print('')
        print('')
        return
    
    elif medium == 'soil' :
        if test == 'soil':
            compounds = rg.test_compounds['eph']+rg.test_compounds['vph']

            compounds = list(set(compounds))
        else:
            compounds = rg.test_compounds[test]
        compounds.sort()
        rags = []
        rag2 = []
        for compound in compounds:
            rags.append(rg.all_ltg[compound])
            rag2.append(rg.all_soil_resd[compound])
        print('')
        print(title)
        print('')
        print('{:30}{:10}{:10}'.format('','leach','residential'))
        for i in range(len(compounds)):
            print('{:30}{:10}{:10}'.format(compounds[i],rags[i],rag2[i]))
        print('')
        print('')
        
        
        
        
def hazard_index(results):
    con = np.zeros(4) 
    for res in results:
        if 'HFPO-DA' in res:
            if res[1] == 'ND':
                continue
            else:
                con[0] = res[1]
        elif 'PFBS' in res:
            if res[1] == 'ND':
                continue
            else:
                con[1] = res[1]   
        elif 'PFNA' in res:
            if res[1] == 'ND':
                continue
            else:
                con[2] = res[1]
        elif 'PFHXS' in res:
            if res[1] == 'ND':
                continue
            else:
                con[3] = res[1]
    if (con[0] == 0) and (con[2] == 0) and (con[3] == 0): # if all the compounds except PFBS are ND (zero) then hazrd index == zero regardless of PFBS concentration
         index = float(0)
    else:
        index = con[0] / 10 + con[1] / 2000 + con[2] / 10 + con[3] / 10
    return index,con


def print_rags(results):
    # results in array of results
    
    print('')
    print(Color.CYAN+'EXCEEDS 2023 RESIDENTIAL RAG' + Color.RESET )
    print('ND  : Non-Detect')
    
    
    col0 = 0
    for resul in results:
        if len(resul[0]) >= col0:
            col0 = len(resul[0]) + 4
        
    print('{:{col0}}{:8}{:6}\n'.format('','con.','RAGs',col0=col0))
    for resul in results:
        if resul[3] == '*':
            print(Color.CYAN + '{:{col0}}{:8}{:6}'.format(resul[0], resul[1], resul[2],col0=col0) + Color.RESET)
        else:
            print('{:{col0}}{:8}{:6}{}'.format(resul[0], resul[1], resul[2], resul[3],col0=col0))

    print('\n')
    return


def print_haz_index(index,con):
    
    if sum(con == 0) > 2:
        print( 'Hazard Index: n/a\n' )
    else:
    
        if index > 1:
            print(Color.CYAN + 'Hazard Index: {:.2f}\n'.format(index) + Color.RESET)
        else:
            print('Hazard Index: {:.2f}\n'.format(index) )
            
def print_pfas_soil(results):
    leach = rg.pfas_soil_leach
    soil = rg.pfas_soil_resd
    
    print('{:40}{:10}{}'.format('','soil','soil'))
    print('{:30}{:10}{:10}{}\n'.format('','con.','RAG/Resd','RAGs/Leach'))
    for resul in results:
        rag1 = soil[resul[0]]
        rag2 = leach[resul[0]]
        if( resul[1] == 'ND') or (rag1 == '-'):
            print('{:30}{:10}{:10}{}'.format(resul[0], resul[1], rag1, rag2))
        elif float(resul[1]) > float(rag1) :
            print(Color.CYAN + '{:30}{:10}{:10}{}{}'.format(resul[0], resul[1], rag1,Color.RESET,rag2) )
        elif float(resul[1]) > float(rag2):
            print(Color.GREEN + '{:30}{:10}{}{:10}{}{}'.format(resul[0], resul[1], Color.RESET,rag1,Color.GREEN,rag2) + Color.RESET)
        else:
            print('{:30}{:10}{:10}{}'.format(resul[0], resul[1], rag1, rag2))


def main(args):

    # printing rag values
    if args.sample in ['pfas','pfas_soil','soil','vph','eph','history','pot','landfill_short','landfill_long','voc']:
        display_rags(args.sample)
        exit()
    
    # determine if sample number of sample location
    
    lab_info,_,_,_ = make.load_from_pickle(paths.site_pickle)
    
    if len(lab_info[lab_info['Sample ID'] == args.sample]) == 1:
        # args.sample is a sample number 
        sample_number = args.sample.split('-')[0]
        edd_path = glob.glob( paths.edd + '/{}_m60.xls*'.format(sample_number))[0]
        
        
        if os.path.isfile(edd_path):
            df = edd.load_edd(edd_path)
            test = edd.which_tests(df,args.sample)
            
            
            if 'eph' in test:
                results = edd.edd_compound_parse(df,args.sample,'eph')
                print_rags(results)
            if 'vph' in test:
                results = edd.edd_compound_parse(df,args.sample,'vph')
                print_rags(results)
            if 'pfas' in test:
                results = edd.edd_compound_parse(df,args.sample,'pfas')
                print_rags(results)
                index,con = hazard_index(results)
                print_haz_index(index,con)
            if 'pfas_soil' in test:
                results = edd.edd_compound_parse(df,args.sample,'pfas')
                print_pfas_soil(results)
            if 'soil' in test:
                results = edd.edd_compound_parse(df,args.sample,'eph') + edd.edd_compound_parse(df,args.sample,'vph')
                results = list(set(results))
                print_rags(results)
            if 'voc' in test:
                results = edd.edd_compound_parse(df,args.sample,'voc')
                print_rags(results)
            if 'landfill_short' in test:
                results = edd.edd_compound_parse(df,args.sample,'landfill_short')
                print_rags(results)
            if 'landfill_long' in test:
                results = edd.edd_compound_parse(df,args.sample,'landfill_long')
                print_rags(results)   
            if 'pot' in test:
                results = edd.edd_compound_parse(df,args.sample,'pot')
                print_rags(results)
            if 'field' in test:
                results = edd.edd_compound_parse(df,args.sample,'field')
                print_rags(results)
        
    elif len(lab_info[lab_info['Loc.'] == args.sample]) > 0:
        # args.sample is a sample location 
        sample_numbers = lab_info[lab_info['Loc.'] == args.sample ]['Sample ID'].to_list()
        dates = lab_info[lab_info['Loc.'] == args.sample ]['Sample Date'].to_list()
        
        n_rows = len(sample_numbers)
        sample_numbers = np.hstack(( np.array(dates)[:,None], np.array(sample_numbers)[:,None],np.zeros((n_rows,1)), np.zeros((n_rows,1)) ))
            
        # sort by date
        sample_numbers = sample_numbers[sample_numbers[:,0].argsort()]
        
        for i,sample in enumerate(sample_numbers[:,1]):
            if sample.lower() == 'none':
                continue
            edd_path = glob.glob(paths.edd +"/{}_m60.xls*".format(sample.split('-')[0]))
            if len(edd_path) == 0:
                continue
            
            edd_path = edd_path[0]
            if os.path.isfile(edd_path):
                sample_numbers[i,2] = 1
                df = edd.load_edd(edd_path)
                sample_numbers[i,3] = edd.which_tests(df,sample)
            
        #get list of all tests
        tt = []
        for t in sample_numbers[:,3]:
            if isinstance(t,float): # this skips a sample number where results are not present
                continue
            tt += t
        all_test = set(tt) # remove dupliates 
        for test in all_test:
            
            all_results = []
            for i,s in enumerate(sample_numbers):
                sample = s[1]
                edd_path = glob.glob(paths.edd+"/{}_m60.xls*".format(sample.split('-')[0]))
                if sample.lower() == 'none':
                    print('EDD not found for {}'.format(sample))
                    continue
                elif len(edd_path) > 0:
                    print('Using EDD for {}'.format(sample))
                    edd_path = edd_path[0]
                    df = edd.load_edd(edd_path)
                    resul = edd.edd_compound_parse(df,sample,test)
                    if len(resul) > 0:
                        all_results.append( resul )
                else:
                    print('EDD not found for {}'.format(sample))
                    continue    
                    
            # print the results to screen 
            if test == 'pfas_soil':
                print('The preferred way to call pfas_soil results is with the sample number')
                # #get leach rags
                # leach = rags.pfas_soil_leach
                
                # d = ''
                # print('\n')
                # for i in range(len(dates)):
                #     d += '{:10}'.format(dates[i].strftime("%y-%m-%d"))
                    
                # print('{:30}{}{:10}{:10}\n'.format('',d,'RAG/Resd','RAGs/Leach'))
                # for i in range(len(all_results[0])):
                #     compound = all_results[0][i][0]
                #     rag = all_results[0][i][2]
                #     rag2 = leach[all_results[0][i][0]]
                #     con = ''
                #     for j in range(len(dates)):
                #         if j > (len(all_results) - 1):
                #             con+= '{:10}'.format('')
                #         elif all_results[j][i][3] == '*':
                #             con += Color.CYAN+'{:10}'.format(all_results[j][i][1]) + Color.RESET
                #         else:
                #             con+= '{:10}'.format(all_results[j][i][1])
             
                #     print('{:30}{}{:10}{:10}'.format(compound,con,rag,rag2) )
        
                # print('\n\n')
                
            else:
                print('')
                print(Color.CYAN+'EXCEEDS 2023 RESIDENTIAL RAG' + Color.RESET )
                print('ND : Non-Detect')
                
                d = ''
                for i in range(len(dates)):
                    d += '{:10}'.format(sample_numbers[i,0].strftime("%y.%m.%d"))

                print('{:30}{}{:10}\n'.format('',d,'RAGs'))
                for i in range(len(all_results[0])):
                    compound = all_results[0][i][0]
                    rag = all_results[0][i][2]
                    con = ''
                    for j in range(len(dates)):
                        if j > (len(all_results) - 1):
                            con+= '{:10}'.format('')
                        elif all_results[j][i][3] == '*':
                            con += Color.CYAN+'{:10}'.format(all_results[j][i][1]) + Color.RESET
                        else:
                            con+= '{:10}'.format(all_results[j][i][1])
             
                    print('{:30}{}{:10}'.format(compound,con,rag) )
        
                print('\n\n')
                    
            
                
    else:
        print('argument passed: {} not a sample number or sample location, check spelling'.format(args.sample))           
                
            

if __name__=="__main__":
    parser= argparse.ArgumentParser()
    
    helps = ('Can be 1) a sample number with subsample 2) location shortname ' +
            'or 3) to print just RAGS the following keywords can be used [pfas,pfas_soil,soil,vph,eph,history,pot,landfill_short,landfill_long,voc]')

    
    
    parser.add_argument('sample' , nargs= '?' , default = None, help=helps)
    
    args = parser.parse_args()
    main(args)