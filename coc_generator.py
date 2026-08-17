# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:05:13 2026

@author: Lucas.Beem

COC generator of both A&L and pace 
address read from PFAS address excel spreadsheet
output pdf saved to same folder as excel spreadsheet

reads contact information from a yaml file
"""

import argparse
import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(base_folder+'/lookup')


import paths
import egad
import geo_utils
from pypdf import PdfWriter, PdfReader
import make_site
import pymupdf

def get_pm_details(pm,k=False):
    
    details = {'lb': ['Lucas Beem', '(207) 272 6438', '312 Canco Rd', 'Portland', '04103','lucas.beem@maine.gov'],
               'es': ['Ed Stamborski','(207) 881 7935','17 State House Station', 'Augusta', '04333', 'edward.stamborski@maine.gov'],
               'ch': ['Colleen Hendricks', '(207) 451 2507','17 State House Station', 'Augusta', '04333','colleen.hendricks@maine.gov'],
               'sm': ['Stephen Morin', '(207) 252 1841','312 Canco Road', 'Portland', '04103','stephen.morin@maine.gov'],
               'lr': ['Louise Roy', '(207) 592 4867','312 Canco Road', 'Portland', '04103','louise.m.roy@maine.gov'],
               'kb': ['Kristen Babcock', '(207) 458 7297','312 Canco Road', 'Portland', '04103','kristen.l.babcock@maine.gov'],
               }
    
    if k:
        return details.keys()
    else:
        return details[pm]



def make_petrol_pace(srgs,pm,town,spill,outfile):
    re = PdfReader(paths.petrol_coc)
    writer = PdfWriter()
    writer.append(re)
    
    writer.update_page_form_field_values( writer.pages[0], {'street': pm[2],
                                                            'city': pm[3],
                                                            'phone': pm[1],
                                                            'zip' : pm[4],
                                                            'email': pm[5],
                                                            'name': args.name.title(),
                                                            'town': town.title(),
                                                            'number': spill,
                                                            'pm': pm[0],
                                                            'copies': pm[5]+',dep.edd@maine.gov',
                                                            'loc1': args.add.title(),
                                                            'date1': args.date,
                                                            })
    
    
    with open(outfile, "wb") as output_stream:
        writer.write(output_stream)
          
    
def make_pfas_pace(args,pm,town,outfile):
    
    re = PdfReader(paths.pfas_coc)
    writer = PdfWriter()
    writer.append(re)
    
    writer.update_page_form_field_values( writer.pages[0], {'street': pm[2],
                                                            'city': pm[3],
                                                            'phone': pm[1],
                                                            'zip' : pm[4],
                                                            'email': pm[5],
                                                            'name': args.name.title(),
                                                            'town': town.title(),
                                                            'number': args.seq,
                                                            'pm': pm[0],
                                                            'copies': pm[5]+',dep.edd@maine.gov',
                                                            'loc1': args.add.title(),
                                                            'date1': args.date,
                                                            })
    
    
    with open(outfile, "wb") as output_stream:
        writer.write(output_stream)
    

    
    
def make_AL(args,pm,town,zipp,outfile):
    re = PdfReader(paths.al_coc)
    writer = PdfWriter()
    writer.append(re)   
    writer.update_page_form_field_values( writer.pages[0], {'phone': pm[1],
                                                            'phone2': pm[1],
                                                            'loc_address': args.add.title(),
                                                            'loc_city' : town.title(),
                                                            'loc_zip' : zipp,
                                                            'email': pm[5],
                                                            'name': pm[0],
                                                            'address': pm[2],
                                                            'city': pm[3],
                                                            'zip': pm[4],
                                                            'date': args.date
                                                            })

    with open(outfile, "wb") as output_stream:
        writer.write(output_stream)




def main(args):
    
    
    x,y = egad.get_site_point(int(args.seq))
    town = geo_utils.pt2town(x,y)
    
    pm = get_pm_details(args.pm)
    
    if args.type == 'petrol':
        
        outfile = base_folder + '/letters/petrol_coc_{}.pdf'.format('_'.join(args.add.split(' ')))
        spill = make_site.get_id(args.seq, 'spill')
        make_petrol_pace (args,pm,town,spill,outfile)
        os.startfile(outfile)
    
    elif args.type =='pfas':
        
        zipp = geo_utils.pt2zip(x,y)
        outfile1 = base_folder + '/letters/pfas_coc_{}.pdf'.format('_'.join(args.add.split(' ')))
        make_pfas_pace(args,pm,town,outfile1)
        
        if args.n:
            outfile2 = base_folder + '/letters/temp.pdf'
            make_AL(args,pm,town,zipp,outfile2)
            
            
            # concatonate pfas cocs
            outfile3 = base_folder + '/letters/pfas_cocs_{}.pdf'.format('_'.join(args.add.split(' ')))
            doc_a = pymupdf.open(outfile1) # open the 1st document
            doc_b = pymupdf.open(outfile2) # open the 2nd document
    
            doc_a.insert_pdf(doc_b) # merge the docs
            doc_a.save(outfile3) # save the merged document with a new filename
            doc_a.close()
            doc_b.close()
            
            #clean up
            os.remove(outfile1)
            os.remove(outfile2)
        
        if args.n:
            os.startfile(outfile3)
        else:
            os.startfile(outfile1)
        


if __name__=="__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument('type', choices =['pfas','petrol'], help='COC type')
    parser.add_argument('seq' , help = 'site sequence number')
    parser.add_argument('name' , help = 'site name')
    parser.add_argument('pm' , choices =  get_pm_details('lb',k=True), default = 'lb', help = 'project manager')
    parser.add_argument('date' , help = 'date of sampling')
    parser.add_argument('add', nargs='?', help = 'address')
    parser.add_argument('-n', action='store_false', help='No potability coc, only applicable with pfas type')
    

    args = parser.parse_args()

    main(args)