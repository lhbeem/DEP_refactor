# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 13:17:38 2026

@author: Lucas.Beem
"""


import argparse


#four details. 1) Name , 2) general grain size/ basic description, 3) drainage 4) parent material
soils ={
'Ad': ['Adams','Sandy','Somewate Excessively','Glacial-fluvial: Granite/Gneiess/Schist'],
'Ab': ['Abram','','excessively',''],
'Al': ['Allagash','Coarse Loam over sand','Well','Slate/Shale'],
'Ba': ['Bangor','Coarse loam','Well', 'Till'],
'Bg': ['Belgrade','Course-Silty','Moderately Well','Glaciomarine/lacustrine'],
'Bo': ['Biddeford','Fine/peat','Very Poorly','Glaciomarine/lacustrine: clays and silt' ],
'Bs': ['Brayton and Wetbury','','',''],
'Br': ['Brayton','','poorly',''],
'Bu': ['Buxton','Fine Clay and silt','Moderately Well','Glaciomarine/lacustrine'],
'Cb': ['Charles','Coarse Silt','Poorly','Alluvial: Slate, meta-siltstone'],
'Ch': ['Charles or Chesuncook','','',''],
'Co': ['Colton','Sandy-skeletal','Excessively','Glaciofluvial'],
'Cr': ['Cornish','Coarse-Silty','Somewhat Poorly','Alluvial: slate, meta-siltstone'],
'Da': ['Danforth','','',''],
'De': ['Deerfield','','',''],
'Di': ['Dixfield','','',''],
'El': ['Elliottsville','','',''],
'Em': ['Elmwood','Coarse Loam over clay','Moderately Well','Glaciomarine/lacustrine'],
'Gp': ['Gravel Pit','','',''],
'He': ['Hermon','Sandy Skeletial','Somewhat Excessively','Till:granite,gniess,shist'],
'Hl': ['Hinckley','Sandy Skeletial','Excessively Well','Glaciofluvial'],
'Hn': ['Hinckley (Hl) - Suffield (Su) Complex. Hl is 60%','','',''],
'Ho': ['Howland','','',''],
'Hr': ['Lyman-Tunbridge','Course Loam','Somewhat Excessively to Well','Till: Mica Schist plus some granite/meta'],
'Ln': ['Lyman','Coarse Loam','Somewhat Excessively','Mica Schist'],
'Ls': ['Limerick', 'Coarse Silty','Poorly', 'Alluvial'],
'Ly': ['Lyman','Course Loam','Somewhat Excessively','Mica Schist'],
'Ma': ['Marlow','Coarse Loam','Well','Schist/Granite'],
'Me': ['Melrose','','',''],
'Mk': ['Medomak','Coarse Silt','Very Poorly','Alluvial: Slate, meta-siltstone'],
'Mn': ['Monadnock','well','coarse loam over sand','Till: Granite, gneiss, schist'],
'Mo': ['Monarda','','',''],
'Mr': ['Marlow','Course loamy','Well','Till:mica schist, granite, gniess'],
'Ms': ['Monson','','',''],
'Mv': ['Monadnock','well','coarse loam over sand','Till: Granite, gneiss, schist'],
'Na': ['Naumburg','','',''],
'Od': ['Ondawa','fine sand','Well','Alluvium: Granite,Gneiss,Schist'],
'Pb': ['Paxton','Course Loamy in Till', 'Well','Till: Mica Schist / Granite'],
'Pc': ['Peacham','','',''], 
'Pn': ['Penquis','','',''],
'Pl': ['Plaisted','','',''],
'Po': ['Podunk','Coarse loam','Moderately Well','Granite/Gneiess/Schist' ],
'Pt': ['Podunk','Coarse loam','Moderately Well','Granite/Gneiess/Schist' ],
'Ra': ['Raynham','','',''],
'Ri': ['Ricker','','',''],
'Ru': ['Rumney','Coarse Loam','Poorly','Alluvial: Salte, meta-siltstone'],
'Sc': ['Scantic','clay','Poorly','Glaciomarine/lacustrine'],
'Se': ['Scantic','clay','Poorly','Glaciomarine/lacustrine'],
'Sk': ['Skerry','Course Loam', 'Moderately Well', 'Till: Granite, gniess, and schist'],
'Sn': ['Skerry','Course Loam', 'Moderately Well', 'Till: Granite, gniess, and schist'],
'Su': ['Suffield','Fine','Well','Glaciomarine/lacustrine: clays and silts'],
'Sz': ['Swanton','Course-loamy over clay','somewhat poorly','Glaciomarine/lacustrine: clays and silts'],
'Te': ['Telos','','',''],
'Th': ['Thorndike','','',''],
'Ty': ['Tunbruidge/Lyman','well','Coarse Loam','Till: Granite, gniess, and schist'],
'Wa': ['Wabash Peat','','',''],
'Wm': ['Windsor','Sandy','excessively','Glacial-fluvial:Granite, gniess, and schist'],
'Wo': ['Wonsqueak','','',''],

}


def main(args):
    print('')
    try:
        print('name:     {}\nType:     {}\nDrainage: {}\nSource:   {}'.format(*soils[args.soil.title()]))
    except:
        print('soil abbreviation not found: {}'.format(args.soil.title()))
    print('')

if __name__=="__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument('soil' ,help='2 letter soil abbreviation')

    args = parser.parse_args()
    main(args)