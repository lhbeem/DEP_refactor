# -*- coding: utf-8 -*-
"""
Created on Fri May  2 14:27:08 2025

@author: Lucas.Beem

"""


import datetime
import argparse 
import fpdf
from fpdf.enums import XPos, YPos
from pypdf import PdfWriter, PdfReader
from datetime import datetime as dt
import dateutil
import subprocess
import shutil
import pymupdf
import glob
import fitz
import numpy as np

import sys
import os
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(os.path.join(base_folder,'lookup'))

import make_site as utils
import paths
import edd_utils as edd 

#the Pace summary pdf from pace has an issue where lots of "Multiple definitions in dictionary..." 
# are output. The logging code below suppresses the output
import logging 
logger = logging.getLogger("pypdf")
logger.setLevel(logging.ERROR)


def header(pdf,paths,basefolder):
    pdf.image(paths.letter_image+'/maine_seal.png', x=20, y=14, w=20)
    pdf.image(paths.letter_image+'/dep_seal.png',x=170,y=18,w=14)
    # pdf.add_font('garamond', '', "{}/eb-garamond/EBGaramond-0.016/ttf/EBGaramond08-Regular.ttf".format(basefolder))
    pdf.set_font('Helvetica', '', 8)
    
    pdf.ln(12)
    # Title
    pdf.set_text_color(43,140,190)
    
    pdf.cell(0, 0, 'STATE OF MAINE',new_x=XPos.LMARGIN, new_y=YPos.TOP,align='C')
    pdf.ln(4)
    pdf.cell(80)
    pdf.set_font('Helvetica', '', 10.5)
    pdf.cell(35, 0, 'DEPARTMENT OF ENVIRONMENTAL PROTECTION', new_x=XPos.LMARGIN, new_y=YPos.TOP,align='C')
    # Line break
    pdf.ln(10)
    
    pdf.set_font('Helvetica','', 7)
    pdf.cell(44,0,'JANET T. MILLS',new_x=XPos.LMARGIN, new_y=YPos.TOP,align='C')
    pdf.cell(333,0,'MELANIE LOYZIM',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='C')
    pdf.ln(4)
    pdf.cell(44,0,'GOVERNOR',new_x=XPos.LMARGIN, new_y=YPos.TOP,align='C')
    pdf.cell(333,0,'COMMISSIONER',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='C')
    pdf.set_text_color(0,0,0)
    return pdf
    

def find_result_page(pdf,sample):
    # pdf is pypdf instance of a lab summary pdf 
    # sample includes subsample
    #line 84 (vph) or line 128 (eph) of results page as the sample number with subsample
    # find result page of subsample
    for page in range(len(pdf.pages)):
        lines = pdf.pages[page].extract_text().split('\n')
        if len(lines)>84:
            for l in lines[84:]:
                if l.startswith(sample):
                    p = page
    return p

def find_glossary_page(pdf):
    # 'pdf' a pypdf instance opf the lab result summary
    for page in range(len(pdf.pages)):
        line = pdf.pages[page].extract_text().split('\n')
        if line[1] == 'GLOSSARY':
            return page


def highlight_pages(pdf_path,sample,output,final_doc_name,test):
    # pdf path : path to pdf summmary of results
    # sample : sample number
    # output : file name of pdf of letter
    # final_doc_name: file name for final concatonated results
    # test: test type
    
    
    # get lab report page numbers
    re = PdfReader(pdf_path)
    p  = find_result_page(re,sample)
    p1 = find_glossary_page(re)
    
    
    doc = fitz.open(pdf_path) # open pdf summary of results
    result_page = doc[p]
    shape= result_page.new_shape()
    if test == 'eph':
        # rect for the results page highlight
        rect_y1 = 400
        rect_y2 = 690
        # rect2 for the ND glossary highlight
        rect2_y1 = 110
        rect2_y2 = 125
    elif test == 'vph':
        rect_y1 = 390
        rect_y2 = 540
        
        rect2_y1 = 110
        rect2_y2 = 125
        
    result_page.draw_rect(fitz.Rect(250, rect_y1, 270, rect_y2), fill =  (0.99609375, 0.96484375, 0) , width = 1, color = (1, 1, 0.734375), fill_opacity=0.5)

    shape.commit()

    glossary2 = doc[p1+2]
    shape= glossary2.new_shape()
    glossary2.draw_rect(fitz.Rect(30, rect2_y1, 505, rect2_y2), fill =  (0.99609375, 0.96484375, 0) , width = 1, color = (1, 1, 0.734375), fill_opacity=0.5)
    shape.commit()
    
    output2 = base_folder + '/letters/temp.pdf'
    
    doc.save(output2)
    doc.close()
    
    doc = pymupdf.open(output2)
    doc.select([0,p,p1,p1+1,p1+2])
    output3 = base_folder + '/letters/temp2.pdf'
    doc.save(output3)
    doc.close()



    ## Concatentate files
    doc_a = pymupdf.open(output) # open the 1st document
    doc_b = pymupdf.open(output3) # open the 2nd document

    doc_a.insert_pdf(doc_b) # merge the docs
    doc_a.save(final_doc_name) # save the merged document with a new filename
    doc_a.close()
    doc_b.close()
    
    #clean up
    os.remove(output)
    os.remove(output2)
    os.remove(output3)



def invoice(args):
    # get cnv path
    lab_id = args.samplelocation.split('-')[0]
    
    cnv_pth = paths.data + '/pace_pdf/{}_cnv.pdf'.format(lab_id) # using sample location as sample when using -invoice

    if not os.path.isfile(cnv_pth):
        print('\nInvoice PDF not found: {}\n'.format(cnv_pth))
        exit()
    
    
    #today's date
    today = dt.now().strftime('%Y%m%d')
    
    # parse invoice number, date, amount from cnv
    re = PdfReader(cnv_pth,strict=False)
    page = re.pages[0]

    

    for line in page.extract_text().split('\n'):
        if line.startswith('Invoice Number:'):
            inv_num = line.split(' ')[2]
        if line.startswith('Invoice Date:'):
            inv_date = dt.strptime(line.split(' ')[4],'%d-%b-%y').strftime('%m/%d/%Y')
        if line.startswith('Total Amount Due:'):
            due = line.split(' ')[-1]
        if line.startswith('Project'):
            spill = line.split()[2]
      
        
    # determine if LAST or LUST
    df_lab,df,_,_ = utils.load_from_pickle(paths.site_pickle)
    # df,_ = utils.load_site_xlw(paths.xls)
    # df_lab = utils.load_lab_xlw(paths.xls)
    
    
    name = utils.name_from_sample( args.samplelocation)
    print('site name: {}'.format(name))
    if spill == 'Pace':
        spill = name
        print('No spill# in invoice, using name as spill #')
    if utils.is_lust(name):
        unit = '1517' # underground tank
    elif utils.is_mys(name):
        unit = '1534' # mystery not tank related
    else:
        unit = '1519' #above ground tank
        
    # create filenames
    stamp_filename = '{}/letters/{}_PaceAnalytical_{}_Stamp.pdf'.format(base_folder,today, inv_num)
    inv_filename = '{}/letters/{}_PaceAnalytical_{}.pdf'.format(base_folder, today, inv_num)
    
    
    ## fill in form fields
    reader = PdfReader(base_folder +'/lookup/FY2024_Stamp.pdf', strict=False) # open blank stamp pdf
    writer = PdfWriter()
    
    page = reader.pages[0]
    # fields = reader.get_fields()
    
    writer.append(reader)
    
    writer.update_page_form_field_values( writer.pages[0], {'InvoiceNumber': inv_num,
                                                            'InvoiceDate': inv_date,
                                                            'VendorCode': 'VC1000070011',
                                                            'VendorName': 'Pace Analytical DBA Alpha Analytical Lab',
                                                            'Fund': '014',
                                                            'Unit': unit, #1519 above ground , 1517 underground
                                                            'SubUnit': '44',
                                                            'Objt': '4006',
                                                            'Activity': 'TECH',
                                                            'SubActivity': 'SMRO',
                                                            'Spill_Num': spill,
                                                            'Amount': '${}'.format(due),
                                                            'CTMV': '/Yes' ,
                                                            'Contract_No': 'CTMV#20240605*0026',
                                                            'BRWM_Action': 'SAMP - Sampling Water/Soil/Air',
                                                            })
    
    
    with open(stamp_filename, "wb") as output_stream:
        writer.write(output_stream)
    
    # copy invoice pdf into output folder
    shutil.copyfile(cnv_pth,inv_filename)
    
    # open invoice folders
    os.startfile(paths.xRoy)
    os.startfile(base_folder +'/letters')
   
    # open invoice in adobe
    adobe_path =r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe"
    subprocess.Popen([adobe_path,stamp_filename])
    



def results(args):
        
    # build path to summary file 
    sample = args.results
    sample_number_short = sample.split('-')[0]
    pdf_path = paths.data +'/pace_pdf/{}_pdf.pdf'.format(sample_number_short)
    
    # check for existance of summary file
    if os.path.isfile(pdf_path) is False:
        print('Summary PDF Not Found, check spelling or for file in folder:')
        print(pdf_path)
        exit()
    
    
    # build contact and site database 
    labs,df,_,contacts = utils.load_from_pickle(paths.site_pickle)

    # read EDD 
    edd_path = glob.glob(paths.edd+'/{}_m60*'.format(sample_number_short))[0]
    if os.path.isfile(edd_path) is False:
        print('EDD Not Found, check spelling or for file in folder:')
        print(pdf_path)
        exit()
    edd_df = edd.load_edd(edd_path)
    
    
    # determine ND v LD v contaminated results

 
    
    #determine sitename from location
    sitename = utils.site_from_location(args.samplelocation)
    if sitename is None:
        print('Sample location ({}) not in Spill_lab_tracking.xlsx'.format(args.samplelocation))
        print('check spelling or Spill_lab_tracking.xlsx')
        exit()
    
    #get spill number 
    spill_num = utils.get_id(sitename, 'spill')
    


    # check for contact information for sample location
    # parse contacts
    contacts = contacts[sitename.lower()][args.samplelocation]
    
    if (contacts[0][0] == None) or (contacts[2][0] == None):
        print('No contact info for: {}'.format(args.samplelocation))
        exit()
    
   
    dear = contacts[0]
    mailing_address = contacts[2]

    
    tests = edd.which_tests(edd_df,sample)
    if len(tests)>1:
        print('multiple tests in one sample number')
        for t in tests:
            print(t)
    results = edd.edd_compound_parse(edd_df,sample,tests[0])
    if tests[0] == 'eph':
        test_text = ['Extractable', 'EPH']
    elif tests[0] == 'vph':
        test_text = ['Volatile', 'VPH']
    
    
    
    if any([aa[3] == '*' for aa in results]):
        if args.d:
            print('Results exceed RAGs, using Detection Letter')
            letter_type = 'D'
        else:
            print('Results exceed RAGs, use -d to override and use Detect Letter')
            exit()
        
    elif all([aa[1] == 'ND' for aa in results]):
        print('Non-Detect letter')
        letter_type = 'ND'
    else:
        print('Limited Detect Letter')
        letter_type = 'LD'
        
    
    # get todays date
    today = datetime.date.today().strftime('%B %#d, %Y')
    today_short = datetime.date.today().strftime('%Y%m%d')

    
    sample_date = edd_df[edd_df['LAB_SAMPLE_ID'] == sample]['SAMPLE_DATE'].iloc[0]

    sample_date = datetime.datetime.strptime(sample_date,'%m/%d/%Y')
    sample_date_str = sample_date.strftime('%B %#d, %Y')
    
    
    
    
    
    

    if letter_type in ['LD','D']:
        # identify which compounds are not ND
        pos = []
        for resul in results:
            if resul[1] != 'ND':
                pos.append(resul)
       
    if letter_type == 'ND':
        # next sample date 
        if args.next is None:
            next_samp = (sample_date + dateutil.relativedelta.relativedelta(months=3)).strftime('%B %Y')
        else:
            next_samp = args.next
    
    #first section of letter same for either ND or LD
    
    pdf = fpdf.FPDF()
    pdf.add_page()
    
    pdf = header(pdf, paths,base_folder)
    
    
    
    pdf.set_text_color(0,0,0)
    pdf.set_xy(0, 0)
    pdf.ln(50)
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(150,0,today,new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='R')
    pdf.ln(5)
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)
    for line in mailing_address:
        pdf.cell(0,0,line,new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
        pdf.ln(5)
    pdf.ln(8)
    pdf.cell(0,0,'RE: Drinking Water Results - {}'.format(contacts[1]))
    pdf.ln(5)
    pdf.cell(0,0,'Spill Number: {}'.format(spill_num))
    pdf.ln(10)
    pdf.cell(0,0,'Dear {},'.format(dear))
    pdf.ln(5)
    
    
    
    if letter_type == 'LD':
        
        pdf.multi_cell(0,5,'On {}, I collected a water sample '.format(sample_date_str)+
                      '(Lab Number {}) at your property. '.format(sample_number_short)+
                      'The test used to analyze the sample for petroleum hydrocarbons was the '+
                      '{} Petroleum Hydrocarbons ({}) protocol. The following petroleum hydrocarbons '.format(test_text[0],test_text[1])+
                      'were detected in the sample: ',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
        pdf.ln()
        pdf.cell(50,0,'Compound',align='L')
        pdf.cell(50,0,'Concentration (ug/L)',align='L')
        pdf.cell(40,0,'RAG (ug/L)',align='L')
        
        pdf.ln(5)
        for com in pos:
            pdf.cell(50,0,com[0],align='L')
            pdf.cell(50,0,com[1],align='L')
            pdf.cell(40,0,com[2],align='L')
            pdf.ln(5)
        
        pdf.ln(5)
        pdf.multi_cell(0,5,
                        "These concentrations are below the Department's groundwater Remediation " +
                        'Action Guidelines (RAG) for residential drinking water. This means that these compounds, ' +
                        'while detected at low levels, are currently not present at a concentration high enough '+
                        'to pose a risk for human consumption. You should consider water from this source safe to '+
                        'drink at this time.',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
        pdf.ln(5)
        pdf.multi_cell(0,5,
                        'Please note that this petroleum protocol does not detect bacteria, iron, manganese, sulfur, '+
                        'or other naturally occurring water quality impurities. I can not speak to the possible '+
                        'presence of those compounds in your water.',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    
        pdf.ln(5)
        pdf.multi_cell(0,5,'If you have further questions, I can be reached at (207) 272-6438 (call or text).',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')

    
    if letter_type == 'ND':

        pdf.multi_cell(0,5,'On {}, I collected a water sample '.format(sample_date_str)+
                      '(Lab Number {}) at your property. '.format(sample_number_short)+
                      'The test used to analyze the sample for petroleum hydrocarbons was the '+
                      '{} Petroleum Hydrocarbons ({}) test. Petroleum hydrocarbons '.format(test_text[0],test_text[1])+
                      'were not detected.  On the enclosed laboratory report, this is indicated '+
                      'by "ND" in the result column.',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
        pdf.ln(5)
        if args.next == 'skip':
            pdf.multi_cell(0,5,'If you have further questions, I can be reached at (207) 272-6438 (call or text).',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
        else: 
            pdf.multi_cell(0,5, 'I will contact you about {} to schedule the next sampling date. '.format(next_samp)+
                      'If you have further questions, I can be reached at (207) 272-6438 (call or text).',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')


    if letter_type == 'D':
        
         pdf.multi_cell(0,5,'On {}, I collected a water sample '.format(sample_date_str)+
                       '(Lab Number {}) at your property. '.format(sample_number_short)+
                       'The test used to analyze the sample for petroleum hydrocarbons was the '+
                       '{} Petroleum Hydrocarbons ({}) protocol. The following petroleum hydrocarbons '.format(test_text[0],test_text[1])+
                       'were detected in the sample: ',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
         pdf.ln()
         pdf.cell(50,0,'Compound',align='L')
         pdf.cell(50,0,'Concentration (ug/L)',align='L')
         pdf.cell(40,0,'RAG (ug/L)',align='L')
         
         pdf.ln(5)
         for com in pos:
             pdf.cell(50,0,com[0],align='L')
             pdf.cell(50,0,com[1],align='L')
             pdf.cell(40,0,com[2],align='L')
             pdf.ln(5)
         
         if sum([aa[3] == '*' for aa in results]) > 1:
            s= 's'
         else:
            s= ''
         
            
         pdf.ln(5)
         pdf.multi_cell(0,5,
                         "There are concentrations above the Department's groundwater Remediation " +
                         'Action Guidelines (RAG) for residential drinking water. This means that the compound{} in excess of the RAG, '.format(s) +
                         'if ingested regularly, would pose a risk to human health. We recommend you do not consume this ' +
                         'water. We will be in contact to discuss the next steps including additional sampling '+
                         'and/or mitigaion strategies.',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
         pdf.ln(5)
         pdf.multi_cell(0,5,
                         'Please note that this petroleum protocol does not detect bacteria, iron, manganese, sulfur, '+
                         'or other naturally occurring water quality impurities. I can not speak to the possible '+
                         'presence of those compounds in your water.',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
        
         pdf.ln(5)
         pdf.multi_cell(0,5,'If you have further questions, I can be reached at (207) 272-6438 (call or text).',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')

    # signature the same for ND, LD, D letters

    pdf.set_left_margin(100)
    pdf.ln(5)
    pdf.cell(0,10,'Sincerely,',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    pdf.image(base_folder+'/lookup/images/signature.png',None,None,30) #100,200
    pdf.ln(4)
    pdf.cell(0,0,'Lucas Beem GE#692',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    pdf.ln(5)
    pdf.cell(0,0,'Maine Department of Environmental Protection',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    pdf.ln(5)
    pdf.cell(0,0,'Bureau of Remediation and Waste Management',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    
    pdf.ln(15)
    pdf.set_x(20)
    pdf.cell(0,0,'Attached: Laboratory Results',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    
    
    output = base_folder + '/letters/letter_{}_{}.pdf'.format(args.samplelocation,today_short)
    
    pdf.output(output)


    ## create highlighted lab report
    final_doc_name = base_folder + '/letters/{}_{}.pdf'.format(today_short,'_'.join(contacts[1].split(' ')))

    highlight_pages(pdf_path,sample,output,final_doc_name,tests[0])
    os.startfile(final_doc_name)


def last(args):
    
    # build path to summary file 
    sample = args.last
    sample_number_short = sample.split('-')[0]
    pdf_path = paths.data +'/pace_pdf/{}_pdf.pdf'.format(sample_number_short)
    
    # check for existance of summary file
    if os.path.isfile(pdf_path) is False:
        print('Summary PDF Not Found, check spelling or for file in folder:')
        print(pdf_path)
        exit()
    
    
    # build contact and site database 
    labs,df,_,contacts = utils.load_from_pickle(paths.site_pickle)

    # read EDD 
    edd_path = glob.glob(paths.edd+'/{}_m60*'.format(sample_number_short))[0]
    if os.path.isfile(edd_path) is False:
        print('EDD Not Found, check spelling or for file in folder:')
        print(pdf_path)
        exit()
    edd_df = edd.load_edd(edd_path)
    
    
    # open lab report pdf
    re = PdfReader(pdf_path)
    # get lab report page numbers 
    p  = find_result_page(re,sample)
    p1 = find_glossary_page(re)
    
    #determine sitename from location
    sitename = utils.site_from_location(args.samplelocation)
    if sitename is None:
        print('Sample location ({}) not in Spill_lab_tracking.xlsx'.format(args.samplelocation))
        print('check spelling or Spill_lab_tracking.xlsx')
        exit()
    
    #get spill number 
    spill_num = utils.get_id(sitename, 'spill')
    


    # check for contact information for sample location
    # parse contacts
    contacts = contacts[sitename.lower()][args.samplelocation]
    
    if (contacts[0][0] == None) or (contacts[2][0] == None):
        print('No contact info for: {}'.format(args.samplelocation))
        exit()
    
   
    dear = contacts[0]
    mailing_address = contacts[2]

    
    tests = edd.which_tests(edd_df,sample)
    
    if len(tests)>1:
        print('multiple tests in one sample number')
        for t in tests:
            print(t)
    
    if tests[0] == 'eph':
        test_text = ['Extractable', 'EPH']
    elif tests[0] == 'vph':
        test_text = ['Volatile', 'VPH']
        
    
    # get todays date
    today = datetime.date.today().strftime('%B %#d, %Y')
    today_short = datetime.date.today().strftime('%Y%m%d')

    
    sample_date = edd_df[edd_df['LAB_SAMPLE_ID'] == sample]['SAMPLE_DATE'].iloc[0]

    sample_date = datetime.datetime.strptime(sample_date,'%m/%d/%Y')
    sample_date_str = sample_date.strftime('%B %#d, %Y')

    # get sample dates
    sample_numbers, dates = utils.get_sample_numbers(labs,args.samplelocation)
    n_rows = len(sample_numbers)
    sample_numbers = np.hstack(( np.array(dates)[:,None], np.array(sample_numbers)[:,None],np.zeros((n_rows,1)), np.zeros((n_rows,1)) ))
    
    sample_numbers = sample_numbers[sample_numbers[:,0].argsort()]
    first_sample = sample_numbers[0,0].strftime('%B %Y')
    last_sample = sample_numbers[-1,0].strftime('%B %Y')
    
    
    #first section of letter 
    
    pdf = fpdf.FPDF()
    pdf.add_page()
    
    pdf = header(pdf, paths,base_folder)
    
    
    pdf.set_text_color(0,0,0)
    pdf.set_xy(0, 0)
    pdf.ln(50)
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(150,0,today,new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='R')
    pdf.ln(5)
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)
    for line in mailing_address:
        pdf.cell(0,0,line,new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
        pdf.ln(5)
    pdf.ln(8)
    pdf.cell(0,0,'RE: Drinking Water Results - {}'.format(contacts[1]))
    pdf.ln(5)
    pdf.cell(0,0,'Spill Number: {}'.format(spill_num))
    pdf.ln(10)
    pdf.cell(0,0,'Dear {},'.format(dear))
    pdf.ln(5)
    
    
    if args.last != None:
        pdf.multi_cell(0,5,'On {}, I collected a water sample '.format(sample_date_str)+
                      '(Lab Number {}) at your property. '.format(sample_number_short)+
                      'The test used to analyze the sample for petroleum hydrocarbons was the '+
                      '{} Petroleum Hydrocarbons ({}) test. Petroleum hydrocarbons '.format(test_text[0],test_text[1])+
                      'were not detected.  On the enclosed laboratory report, this is indicated '+
                      'by "ND" in the result column.',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
        
        pdf.ln(5)
    
    pdf.multi_cell(0,5,'We have periodically monitored your drinking water '+
                   'between {} and {} '.format(first_sample,last_sample) +
                   'and the Maine Department of Environmental Protection believes that '+
                   'no further monitoring is necessary.',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    pdf.ln(5)
    pdf.multi_cell(0,5,'We appreciate your patience throughout this process. If you have further questions ' +
                   'or anything changes with your drinking water, '+
                   'I can be reached at (207) 272-6438 (call or text).',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    

    
    # signature 

    pdf.set_left_margin(100)
    pdf.ln(5)
    pdf.cell(0,10,'Sincerely,',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    pdf.image(base_folder+'/lookup/images/signature.png',None,None,30) #100,200
    pdf.ln(4)
    pdf.cell(0,0,'Lucas Beem GE#692',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    pdf.ln(5)
    pdf.cell(0,0,'Maine Department of Environmental Protection',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    pdf.ln(5)
    pdf.cell(0,0,'Bureau of Remediation and Waste Management',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    
    if args.last != None:
        pdf.ln(15)
        pdf.set_x(20)
        pdf.cell(0,0,'Attached: Laboratory Results',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    
    
    output = base_folder + '/letters/letter_{}_{}.pdf'.format(args.samplelocation,today_short)
    
    pdf.output(output)

    final_doc_name = base_folder + '/letters/{}_{}_final.pdf'.format(today_short,'_'.join(contacts[1].split(' ')))
    highlight_pages(pdf_path,sample,output,final_doc_name,tests[0])
    os.startfile(final_doc_name)
    
    # there was soem conditionals for merging in the code (re: highlight_pages)
    # when args.last == None. Not sure when that would be the case when code is used
    # as intended. Making note here just incase errors associated merging pdfs occurs.
    
def close(args):
    
    if args.close:
        Err = False
        if len(args.close) != 27:
            Err = True
        elif args.close[4:25:5] != '-----':
            Err = True
        if Err:
            print('The certified mail number does not appear to be the correct format')
            print('Code expects the form ####-####-####-####-####-##')
            exit()
    
    # load contact and site database
    labs,df,_,contacts = utils.load_from_pickle(paths.site_pickle)
   
    #determine sitename from location
    sitename = utils.site_from_location(args.samplelocation)
    if sitename is None:
        print('Sample location ({}) not in Spill_lab_tracking.xlsx'.format(args.samplelocation))
        print('check spelling or Spill_lab_tracking.xlsx')
        exit()
    
    #get spill number 
    spill_num = utils.get_id(sitename, 'spill')
    # check for contact information for sample location
    # parse contacts
    contacts = contacts[sitename.replace(' ','').lower()][args.samplelocation]
    
    if (contacts[0][0] == None) or (contacts[2][0] == None):
        print('No contact info for: {}'.format(args.samplelocation))
        exit()
    
   
    dear = contacts[0]
    mailing_address = contacts[2]

    # get todays date
    today = datetime.date.today().strftime('%B %#d, %Y')
    today_short = datetime.date.today().strftime('%Y%m%d')
 
    
    pdf = fpdf.FPDF()
    pdf.add_page()
    
    pdf = header(pdf, paths,base_folder)
    # pdf = footer(pdf)
    
    
    pdf.set_text_color(0,0,0)
    pdf.set_xy(0, 0)
    pdf.ln(50)
    pdf.set_font('Helvetica', '', 12)
    pdf.set_left_margin(100)
    pdf.cell(0,0,today,new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    pdf.ln(10)
    pdf.cell(0,0,'Certified Mail #:{}'.format(args.close),new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)
    for line in mailing_address:
        pdf.cell(0,0,line,new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
        pdf.ln(5)
    pdf.ln(5)
    pdf.cell(0,0,'RE: Spill Number {} : {}'.format(spill_num, contacts[1]))
    pdf.ln(10)
    pdf.cell(0,0,'Dear {},'.format(dear))
    pdf.ln(5)
    
    
    pdf.multi_cell(0,5,'This letter is to inform you that the petroleum discharge at '+
                   'the above-referenced property has been remediated to the satisfaction '+
                   'of the Commissioner of Environmental Protection in accordance with 38 MRSA '+
                   '{}548 and {}568. Using the Maine Remedial Action Guidelines (2023), we '.format('\u00A7','\u00A7')+
                   'conclude that the health risks have been adequately mitigated based on '+
                   'current site conditions and uses. No further remedial actions are planned '+
                   'at this time and the site has been taken off the Department''s Long-term Petroleum '+
                   'Remediation Priority List.',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    pdf.ln(5)
    pdf.multi_cell(0,5,'The Department reserves the right to require or undertake further investigation '+
                   'and remedial action if the site conditions change or new information is discovered. '+
                   'New information regarding site hydrology and geology, of the effectiveness of the '+ 
                   'remedial measures or changes in land use may warrant a reassessment of the health '+ 
                   'risk associated with the discharge. In the event of the need for further eligible '+ 
                   'cleanup expenses resulting from this spill, Maine Ground and Surface Waters Clean-up '+ 
                   'and Response Fund insurance coverage remains and is transferable to future owners in '+ 
                   'accordance with State statute.',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    pdf.ln(5)
    pdf.multi_cell(0,5,'That further clean up actions are not necessary at this time does not absolve any '+ 
                   'responsible party of liability under 38 MRSA §552 or §570 if additional measures are '+ 
                   'found to be needed in the future.  Responsible parties can pursue a liability waiver '+ 
                   'from the State of Maine by pursuing further investigation and remedial action under the '+ 
                   'Department''s Voluntary Response Action Program (VRAP) under 38 MRSA {}343-E.  For further '.format('\u00A7')+ 
                   'information, please call VRAP staff at (207) 287-2651.',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    pdf.ln(5)
    pdf.multi_cell(0,5,'Please retain a copy of this letter in your records. A complete record of the remedial '+ 
                   'actions taken at the property is available from the Department. If there are any questions '+ 
                   'or concerns, please call me at (207) 272-6438.',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    
        

    pdf.set_left_margin(100)
    pdf.ln(5)
    pdf.cell(0,10,'Sincerely,',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    pdf.image(base_folder+'/lookup/images/signature.png',None,None,30) #100,200
    pdf.ln(4)
    pdf.cell(0,0,'Lucas Beem GE#692',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    pdf.ln(5)
    pdf.cell(0,0,'Maine Department of Environmental Protection',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    pdf.ln(5)
    pdf.cell(0,0,'Bureau of Remediation and Waste Management',new_x=XPos.LMARGIN, new_y=YPos.NEXT,align='L')
    pdf.ln(15)

    
    output = base_folder + '/letters/{}_{}_closure.pdf'.format(today_short,'_'.join(contacts[1].split(' ')))
    
    
    pdf.output(output)

    os.startfile(output)


if __name__=="__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument('samplelocation', help="sample location that matches spill_tracking_xls >  contacts > sample location id (include quotes)")
    parser.add_argument('-close', help='Certified mail number in the form ####-####-####-####-####-##')
    parser.add_argument('-invoice',action='store_true', help='when using have the positional argument by sample number')
    parser.add_argument('-results', help='this is to generate typical results letters during monitoring, pass the sample number with subsample')
    parser.add_argument('-next', nargs='?', default=None, help="month and year for next sample contact default is to use three months after the last sample date. if 'skip' is passed as argument, sentence concerning next sample scheduling is omitted ")
    parser.add_argument('-last', help='This is to generate last results letters indicating ending monitoring, pass the sample number with subsample')
    args = parser.parse_args()

    
    
    if args.close is not None:
        args.samplelocation = args.samplelocation.lower()
        close(args)
    if args.invoice:
        invoice(args)
    if args.results is not None:
        if (len(args.results) != 11) or not args.results.startswith('L') :
            print('appears sample number is not in correct format L#######-##')
            print( args.results)
            exit()
        args.samplelocation = args.samplelocation.lower()
        results(args)
    if args.last is not None:
        args.samplelocation = args.samplelocation.lower()
        last(args)