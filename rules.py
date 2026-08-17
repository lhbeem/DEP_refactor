# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 14:21:49 2025

@author: Lucas.Beem
"""

import argparse
import os
import sys
base_folder = os.path.dirname(__file__) #folder that contains the script
sys.path.append(base_folder+'/lookup')
import paths
import glob
 

toc =   ('096 Ch. 2 - Processing of Applications and Other Administrative Matters\n' +
'096 Ch. 3 - Rules Concerning the Conduct of Licensing Hearings\n' +
'096 Ch. 4 - Rule Governing Hearings on Appeals of Certain Emergency or Administrative Commissioner Orders\n' +
'096 Ch. 40 - Conduct of Enforcement Hearings\n' +
'096 Ch. 80 - Reduction of Toxics in Packaging\n' +
'096 Ch. 81 - Designation of Priority Toxic Chemicals\n' +
'096 Ch. 82 - Priority Toxic Chemical Reporting and Pollution Prevention Planning\n' +
'096 Ch. 90 - Products Containing Perfluoroalkyl and Polyfluoroalkyl Substances\n' +
'096 Ch. 100 - Definitions Regulation\n' +
'096 Ch. 101 - Visible Emissions Regulation\n' +
'096 Ch. 102 - Open Burning\n' +
'096 Ch. 103 - Fuel Burning Equipment Particulate Emission Standard\n' +
'096 Ch. 104 - Incinerator Particulate Emission Standard\n' +
'096 Ch. 105 - General Process Source Particulate Emission Standard\n' +
'096 Ch. 106 - Low Sulfur Fuel Regulation\n' +
'096 Ch. 107 - Sulfur Dioxide Emission Standards for Sulfite Pulp Mills\n' +
'096 Ch. 109 - Emergency Episode Regulations\n' +
'096 Ch. 110 - Ambient Air Quality Standards\n' +
'096 Ch. 111 - Petroleum Liquid Storage Vapor Control\n' +
'096 Ch. 112 - Bulk Terminal Petroleum Liquid Transfer Requirements\n' +
'096 Ch. 113 - Growth Offset Regulation\n' +
'096 Ch. 114 - Classification of Air Quality Control Regions\n' +
'096 Ch. 115 - Major and Minor Source Air Emission License Regulations\n' +
'096 Ch. 116 - Prohibited Dispersion Techniques\n' +
'096 Ch. 117 - Source Surveillance - Emissions Monitoring\n' +
'096 Ch. 118 - Gasoline Dispensing Facilities Vapor Control\n' +
'096 Ch. 119 - Motor Vehicle Fuel Volatility Requirements\n' +
'096 Ch. 120 - Gasoline Tank Truck Tightness Self-Certification\n' +
'096 Ch. 121 - Emission Limitations and Emission Testing of Resource Recovery Facilities\n' +
'096 Ch. 123 - Control of Volatile Organic Compounds from Paper Film and Foil Coating Operations\n' +
'096 Ch. 124 - Total Reduced Sulfur Control from Kraft Pulp Mills\n' +
'096 Ch. 125 - Perchloroethylene Dry Cleaner Regulation\n' +
'096 Ch. 126 - Capture Efficiency Test Procedures\n' +
'096 Ch. 127 - New Motor Vehicle Emission Standards\n' +
'096 Ch. 129 - Surface Coating Facilities\n' +
'096 Ch. 130 - Solvent Cleaners\n' +
'096 Ch. 131 - Cutback Asphalt and Emulsified Asphalt\n' +
'096 Ch. 132 - Graphic Arts - Rotogravure and Flexography\n' +
'096 Ch. 133 - Petroleum Liquids Transfer Vapor Recovery at Bulk Gasoline Plants\n' +
'096 Ch. 134 - Reasonably Available Control Technology for Facilities that Emit Volatile Organic Compounds\n' +
'096 Ch. 137 - Emission Statements\n' +
'096 Ch. 138 - Reasonably Available Control Technology for Facilities that Emit Nitrogen Oxides\n' +
'096 Ch. 139 - Transportation Conformity\n' +
'096 Ch. 140 - Part 70 Air Emission License Regulations\n' +
'096 Ch. 143 - New Source Performance Standards (NSPS)\n' +
'096 Ch. 144 - National Emission Standards for Hazardous Air Pollutants (NESHAP)\n' +
'096 Ch. 145 - NOx Control Program\n' +
'096 Ch. 146 - Diesel-Powered Motor Vehicle Emissions Standards\n' +
'096 Ch. 147 - Hydrofluorocarbon Prohibitions\n' +
'096 Ch. 148 - Emissions from Smaller-Scale Electric Generating Facilities\n' +
'096 Ch. 149 - General Permit for Nonmetallic Mineral Processing Plants\n' +
'096 Ch. 150 - Control of Emissions from Outdoor Wood Boilers\n' +
'096 Ch. 151 - Architectural and Industrial Maintenance (AIM) Coatings\n' +
'096 Ch. 152 - Control of Emissions of Volatile Organic Compounds from Consumer Products\n' +
'096 Ch. 153 - Mobile Equipment Repair and Refinishing\n' +
'096 Ch. 154 - Control of Volatile Organic Compounds from Flexible Package Printing\n' +
'096 Ch. 156 - CO2 Budget Trading Program\n' +
'096 Ch. 157 - CO2 Budget Trading Program Waiver and Suspension\n' +
'096 Ch. 158 - CO2 Budget Trading Program Auction Provisions\n' +
'096 Ch. 159 - Control of Volatile Organic Compounds from Adhesives and Sealants\n' +
'096 Ch. 161 - Graphic Arts - Offset Lithography and Letterpress Printing\n' +
'096 Ch. 162 - Control for Fiberglass Boat Manufacturing Materials\n' +
'096 Ch. 163 - Residential Wood Stove Replacement and Rebate Program\n' +
'096 Ch. 164 - General Permit for Concrete Batch Plants\n' +
'096 Ch. 165 - General Permit for Class IV-A Incinerators\n' +
'096 Ch. 166 - Industrial Cleaning Solvents\n' +
'096 Ch. 167 - Tracking and Reporting Gross and Net Annual Greenhouse Gas Emissions\n' +
'096 Ch. 168 - Statewide Greenhouse Gas Emissions Regulation\n' +
'096 Ch. 169 - Stationary Generators\n' +
'096 Ch. 170 - Degassing of Petroleum Storage Tanks Marine Vessels and Transport Vessels\n' +
'096 Ch. 171 - Control of Petroleum Storage Facilities\n' +
'096 Ch. 180 - Appliance Efficiency Standards\n' +
'096 Ch. 200 - Metallic Mineral Exploration Advanced Exploration and Mining\n' +
'096 Ch. 263 - Maine Comprehensive and Limited Environmental Laboratory Accreditation Rule (jointly with 10-144)\n' +
'096 Ch. 305 - Natural Resources Protection Act - Permit by Rule Standards\n' +
'096 Ch. 310 - Wetlands and Waterbodies Protection\n' +
'096 Ch. 315 - Assessing and Mitigating Impacts to Existing Scenic and Aesthetic Uses\n' +
'096 Ch. 321 - Shoreland Zoning Ordinance for Municipality of Freedom\n' +
'096 Ch. 335 - Significant Wildlife Habitat\n' +
'096 Ch. 342 - Significant Groundwater Wells\n' +
'096 Ch. 355 - Coastal Sand Dune Rules\n' +
'096 Ch. 371 - Definitions of Terms Used in Site Location of Development Law and Regulations\n' +
'096 Ch. 372 - Policies and Procedures Under Site Location Law\n' +
'096 Ch. 373 - Financial and Technical Capacity Standards of the Site Location of Development Act\n' +
'096 Ch. 375 - No Adverse Environmental Effect Standards of the Site Location of Development Act\n' +
'096 Ch. 376 - Soil Types Standard of Site Location Law\n' +
'096 Ch. 377 - Review of Roads Under Site Location of Development Law\n' +
'096 Ch. 378 - Variance Criteria for the Excavation of Rock Borrow Topsoil Clay or Silt and Performance Standards for the Storage of Petroleum Products\n' +
'096 Ch. 379 - Compensation for Impacts to High-Value Agricultural Land from Solar Energy Development\n' +
'096 Ch. 380 - Long-Term Construction Projects under the Site Location of Development Act\n' +
'096 Ch. 382 - Wind Energy Act Standards\n' +
'096 Ch. 400 - Solid Waste Management Rules: General Provisions\n' +
'096 Ch. 401 - Solid Waste Management Rules: Landfill Siting Design and Operation\n' +
'096 Ch. 402 - Solid Waste Management Rules: Transfer Stations and Storage Sites for Solid Waste\n' +
'096 Ch. 403 - Solid Waste Management Rules: Incineration Facilities\n' +
'096 Ch. 405 - Solid Waste Management Rules: Water Quality Monitoring Leachate Monitoring and Waste Characterization\n' +
'096 Ch. 409 - Solid Waste Management Rules: Processing Facilities\n' +
'096 Ch. 410 - Solid Waste Management Rules: Composting Facilities\n' +
'096 Ch. 411 - Solid Waste Management Rules: Non-Hazardous Waste Transporter Licenses\n' +
'096 Ch. 415 - Solid Waste Management Rules: Reasonable Costs for the Handling Transportation and Recycling of Electronic Wastes\n' +
'096 Ch. 418 - Solid Waste Management Rules: Beneficial Use of Solid Wastes\n' +
'096 Ch. 419 - Solid Waste Management Rules: Agronomic Utilization of Residuals\n' +
'096 Ch. 420 - Solid Waste Management Rules: Septage Management Rules\n' +
'096 Ch. 424 - Solid Waste Management Rules: Lead Management Regulations\n' +
'096 Ch. 425 - Solid Waste Management Rules: Asbestos Management Regulations\n' +
'096 Ch. 426 - Responsibilities under the Returnable Beverage Container Law\n' +
'096 Ch. 428 - Stewardship Program for Packaging\n' +
'096 Ch. 450 - Administrative Regulations for Hydropower Projects\n' +
'096 Ch. 500 - Stormwater Management\n' +
'096 Ch. 501 - Stormwater Management Compensation Fees and Mitigation Credit\n' +
'096 Ch. 502 - Direct Watersheds of Lakes Most at Risk from New Development and Urban Impaired Streams\n' +
'096 Ch. 514 - Use of Aquatic Pesticides\n' +
'096 Ch. 517 - Certification of Persons Servicing and Repairing Sanitary Waste Treatment Facility\n' +
'096 Ch. 519 - Interim Effluent Limitations and Controls for the Discharge of Mercury\n' +
'096 Ch. 520 - Definitions for the Waste Discharge Permitting Program\n' +
'096 Ch. 521 - Applications for Waste Discharge Licenses\n' +
'096 Ch. 522 - Application Processing Procedures for Waste Discharge Licenses\n' +
'096 Ch. 523 - Waste Discharge License Conditions\n' +
'096 Ch. 524 - Criteria and Standards for Waste Discharge Licenses\n' +
'096 Ch. 525 - Effluent Guidelines and Standards\n' +
'096 Ch. 526 - Cooling Water Intake Structures\n' +
'096 Ch. 528 - Pretreatment Program\n' +
'096 Ch. 529 - General Permits for Certain Wastewater Discharges\n' +
'096 Ch. 530 - Surface Waters Toxics Control Program\n' +
'096 Ch. 531 - Wastewater Treatment Plant Operator Certification\n' +
'096 Ch. 532 - Large Commercial Passenger Vessels\n' +
'096 Ch. 534 - Wastewater Treatment Plant Operator Certifications - Revocation or Suspension\n' +
'096 Ch. 543 - Rules to Control the Subsurface Discharge of Pollutants\n' +
'096 Ch. 550 - Discontinuance of Wastewater Treatment Lagoons\n' +
'096 Ch. 555 - Standards for the Addition of Transported Wastes to Wastewater Treatment Facilities\n' +
'096 Ch. 570 - Combined Sewer Overflow Abatement\n' +
'096 Ch. 573 - Snow Dumps: Best Management Practices for Pollution Prevention\n' +
'096 Ch. 574 - Siting and Operation of Road Salt and Sand-Salt Storage Areas\n' +
'096 Ch. 579 - Classification Attainment Evaluation Using Biological Criteria for Rivers and Streams\n' +
'096 Ch. 580 - Regulations Relating to Sampling Procedures and Analytic Procedures\n' +
'096 Ch. 581 - Regulations Relating to Water Quality Evaluations\n' +
'096 Ch. 582 - Regulations Relating to Temperature\n' +
'096 Ch. 583 - Nutrient Criteria for Class AA A B and C Fresh Surface Waters\n' +
'096 Ch. 584 - Surface Water Quality Criteria for Toxic Pollutants\n' +
'096 Ch. 585 - Identification of Fish Spawning Areas and Designation Salmonid Spawning Areas\n' +
'096 Ch. 586 - Rules Pertaining to Discharges to Class A Waters\n' +
'096 Ch. 587 - In-stream Flows and Lake and Pond Water Levels\n' +
'096 Ch. 592 - The Small Community Wastewater Program\n' +
'096 Ch. 594 - State Contribution to Overboard Discharge Replacement\n' +
'096 Ch. 595 - State Revolving Fund\n' +
'096 Ch. 596 - Overboard Discharges: Licensing and Abandonment\n' +
'096 Ch. 600 - Oil Discharge Prevention and Pollution Control Rules for Marine Oil Terminal Facilities \n' +
'096 Ch. 680 - Tanker Anchorage Rules\n' +
'096 Ch. 685 - Payment and Reimbursement of Oil Transfer Fees\n' +
'096 Ch. 686 - Standards for Assessing Ability to Pay Deductibles under the State Insurance Program for \n' +
'096 Ch. 691 - Rules for Underground Oil Storage Facilities\n' +
'096 Ch. 692 - Siting of Oil Storage Facilities\n' +
'096 Ch. 693 - Operator Training for Underground Oil Hazardous Substance and Field Constructed \n' +
'096 Ch. 695 - Rules for Underground Hazard Substance Storage Facilities\n' +
'096 Ch. 696 - Oil Discharge and Pollution Control Rules for Rail Tank Cars\n' +
'096 Ch. 700 - Wellhead Protection: Siting of Facilities that Pose a Significant Threat to Drinking Water\n' +
'096 Ch. 800 - Identification of Hazardous Matter\n' +
'096 Ch. 801 - Discharge of Hazardous Matter: Removal and Written Reporting Procedures\n' +
'096 Ch. 850 - Identification of Hazardous Wastes\n' +
'096 Ch. 851 - Standards for Generators of Hazardous Waste\n' +
'096 Ch. 852 - Land Disposal Restrictions\n' +
'096 Ch. 853 - Licensing of Transporters of Hazardous Waste\n' +
'096 Ch. 854 - Standards for Hazardous Waste Facilities\n' +
'096 Ch. 855 - Interim Licenses for Waste Facilities for Hazardous Waste\n' +
'096 Ch. 856 - Licensing of Hazardous Waste Facilities\n' +
'096 Ch. 857 - Hazardous Waste Manifest Requirements\n' +
'096 Ch. 858 - Universal Waste Rules\n' +
'096 Ch. 860 - Waste Oil Management Rules\n' +
'096 Ch. 870 - Labeling of Mercury-added Products\n' +
'096 Ch. 872 - Exemptions from the Ban on Sale of Mercury-added Switches Relays and Measuring Devices\n' +
'096 Ch. 880 - Regulation of Chemical Use in Childrens Products\n' +
'096 Ch. 881 - Fees: Chemical Use in Childrens Products\n' +
'096 Ch. 882 - Designation of Bisphenol A as a Priority Chemical and Regulation of Bisphenol A in Children’s Products\n' +
'096 Ch. 883 - Designation of the Chemical Class Nonylphenol and Nonylphenol Ethoxylates as a Priority Chemical\n' +
'096 Ch. 884 - Designation of Cadmium as a Priority Chemical and Regulation of Cadmium in Childrens Products\n' +
'096 Ch. 885 - Designation of Formaldehyde as a Priority Chemical and Regulation of Formaldehyde in Childrens Products\n' +
'096 Ch. 886 - Designation of Mercury as a Priority Chemical and Regulation of Mercury in Childrens Products\n' +
'096 Ch. 887 - Designation of Arsenic as a Priority Chemical and Regulation of Arsenic in Childrens Products\n' +
'096 Ch. 888 - Designation of Four Members of the Chemical Class Phthalates as Priority Chemicals\n' +
'096 Ch. 889 - Designation of Two Flame Retardants as Priority Chemicals\n' +
'096 Ch. 890 - Designation of PFOS and Its Salts as Priority Chemicals\n' +
'096 Ch. 900 - Biomedical Waste Management Rules\n' +
'096 Ch. 1000 - Guidelines for Municipal Shoreland Zoning Ordinances\n' +
'096 Ch. 1243 - Shoreland Zoning Ordinance for Municipality of Troy\n' +
'096 Ch. 1244 - Shoreland Zoning Ordinance for Municipality of Whitefield\n' +
'096 Ch. 1245 - Shoreland Zoning Ordinance for Municipality of Athens\n' +
'096 Ch. 1247 - Shoreland Zoning Ordinance for Municipality of Bradford\n' +
'096 Ch. 1249 - Shoreland Zoning Ordinance for Municipality of Charlotte\n' +
'096 Ch. 1250 - Shoreland Zoning Ordinance for Municipality of Chester\n' +
'096 Ch. 1251 - Shoreland Zoning Ordinance for Municipality of Columbia\n' +
'096 Ch. 1253 - Shoreland Zoning Ordinance for Municipality of Edinburg\n' +
'096 Ch. 1254 - Shoreland Zoning Ordinance for Municipality of Hanover\n' +
'096 Ch. 1255 - Shoreland Zoning Ordinance for Municipality of Knox\n' +
'096 Ch. 1256 - Shoreland Zoning Ordinance for Municipality of Limerick\n' +
'096 Ch. 1257 - Shoreland Zoning Ordinance for Municipality of Moose River\n' +
'096 Ch. 1261 - Shoreland Zoning Ordinance for Municipality of Springfield\n' +
'096 Ch. 1262 - Shoreland Zoning Ordinance for Municipality of Steuben\n' +
'096 Ch. 1263 - Shoreland Zoning Ordinance for Municipality of Talmadge\n' +
'096 Ch. 1264 - Shoreland Zoning Ordinance for Municipality of Passadumkeag\n' +
'096 Ch. 1265 - Shoreland Zoning Ordinance for Municipality of Waite\n' +
'096 Ch. 1266 - Shoreland Zoning Ordinance for Municipality of Woodville\n' +
'096 Ch. 1267 - Shoreland Zoning Ordinance for Municipality of Amity\n' +
'096 Ch. 1268 - Shoreland Zoning Ordinance for Municipality of Bancroft\n' +
'096 Ch. 1270 - Shoreland Zoning Ordinance for Municipality of Cooper\n' +
'096 Ch. 1271 - Shoreland Zoning Ordinance for Municipality of Corinth\n' +
'096 Ch. 1272 - Shoreland Zoning Ordinance for Municipality of Hersey\n' +
'096 Ch. 1273 - Shoreland Zoning Ordinance for Municipality of Hiram\n' +
'096 Ch. 1275 - Shoreland Zoning Ordinance for Municipality of Lagrange\n' +
'096 Ch. 1277 - Shoreland Zoning Ordinance for Municipality of Ludlow\n' +
'096 Ch. 1279 - Shoreland Zoning Ordinance for Municipality of Medford\n' +
'096 Ch. 1281 - Shoreland Zoning Ordinance for Municipality of Merrill\n' +
'096 Ch. 1282 - Shoreland Zoning Ordinance for Municipality of Orient\n' +
'096 Ch. 1283 - Shoreland Zoning Ordinance for Municipality of Stacyville\n' +
'096 Ch. 1285 - Shoreland Zoning Ordinance for Municipality of Vanceboro\n' +
'096 Ch. 1286 - Shoreland Zoning Ordinance for Municipality of Wade\n' +
'096 Ch. 1288 - Shoreland Zoning Ordinance for Municipality of Aurora\n' +
'096 Ch. 1289 - Shoreland Zoning Ordinance for Municipality of Bowerbank\n' +
'096 Ch. 1292 - Shoreland Zoning Ordinance for Municipality of Carthage\n' +
'096 Ch. 1293 - Shoreland Zoning Ordinance for Municipality of Exeter\n' +
'096 Ch. 1294 - Shoreland Zoning Ordinance for Municipality of Farmingdale\n' +
'096 Ch. 1295 - Shoreland Zoning Ordinance for Municipality of Frankfort\n' +
'096 Ch. 1296 - Shoreland Zoning Ordinance for Municipality of Guilford\n' +
'096 Ch. 1301 - Shoreland Zoning Ordinance for Municipality of Milo\n' +
'096 Ch. 1304 - Shoreland Zoning Ordinance for Municipality of North Haven\n' +
'096 Ch. 1307 - Shoreland Zoning Ordinance for Municipality of Penobscot\n' +
'096 Ch. 1308 - Shoreland Zoning Ordinance for Municipality of Plymouth\n' +
'096 Ch. 1312 - Shoreland Zoning Ordinance for Municipality of Waldo\n' +
'096 Ch. 1320 - Shoreland Zoning Ordinance for Municipality of Crystal\n' +
'096 Ch. 1321 - Shoreland Zoning Ordinance for Municipality of Durham\n' +
'096 Ch. 1322 - Shoreland Zoning Ordinance for Municipality of Etna\n' +
'096 Ch. 1323 - Shoreland Zoning Ordinance for Municipality of Isle Au Haut\n' +
'096 Ch. 1326 - Shoreland Zoning Ordinance for Municipality of Stow\n' +
'096 Ch. 1333 - Shoreland Zoning Ordinance for Municipality of Swanville\n' +
'096 Ch. 1334 - Shoreland Zoning Ordinance for Municipality of Columbia Falls\n' +
'096 Ch. 1335 - Shoreland Zoning Ordinance for Municipality of Danforth\n' +
'096 Ch. 1337 - Shoreland Zoning Ordinance for Municipality of Wellington\n' +
'096 Ch. 1339 - Shoreland Zoning Ordinance for Municipality of Lubec\n' +
'481 Ch. 1 - Administrative Rules\n' +
'481 Ch. 2 - Rules of Practice and Procedure Governing Adjudicatory Proceedings\n' +
'481 Ch. 3 - Certification of Underground Oil Tank Installers\n' +
'481 Ch. 6 - Certification of Underground Oil Storage Tank Inspectors')






def main(args):

    if (args.num is None):
        print(toc)
        exit()
        
    if args.num.startswith('96') or args.num.startswith('096'):
        agency = '096'
    elif args.num.startswith('481'):
        agency = '481'
    else:
        print('agency not recognized: {}\n'.format(args.num))
        print('chapter needs to begin with either 96 or 481')
        exit()
    
    if agency == '096':
        chapter = args.num.split('96')[-1]
    elif agency == '481':
        chapter = args.num.split('481')[-1]
        
        
    sop = glob.glob(paths.rules_dir+'/{}c{:03d}.pdf'.format(agency,int(chapter)))
    if len(sop) == 0:
        print('No rule found with number: {}'.format(args.num))
        exit()
    sop = sop[0]
    
    
    os.startfile(sop)





if __name__=="__main__":
    parser= argparse.ArgumentParser()
    
    
    parser.add_argument('num' , nargs= '?' , default = None, help='rule chapter number to open, agency numer and chapter number (e.g. 962,4816)')
   
    args = parser.parse_args()
    main(args)