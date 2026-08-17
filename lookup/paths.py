    # -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 07:52:58 2025

@author: Lucas.Beem


'global' paths
"""
import os
base_folder = os.path.dirname(__file__) #folder that contains this script 


# folders
documents = 'C:/Users/Lucas.Beem/OneDrive - State of Maine/Documents'
projects = os.path.join(documents, 'Projects')
data = os.path.join(documents, 'data')
notes = os.path.join(base_folder , '..' , '..', '..', 'notes')
edd = data +'/edd'
pdf = data +'/pace_pdf' #pace pdfs
xRoy = 'H:/DEP_All_Users/BRWM INVOICES/_DIVISION/TECH SERVICES/xRoy Louise'
aerial_images = data +'/aerial_image'
sop_dir = notes + '/SOP'
rules_dir = notes + '/rules'

# lab tracking data xls and related 
xls = base_folder + '/Spill_lab_tracking.xlsx'
location_list = base_folder +'/location_list.xlsx'
site_pickle = base_folder +'/tracking.pkl'
compounds_xls = base_folder + '/edd_compounds.xlsx'

# pfas geo layers
fields = data + '/geo_files/Licensed Field.gpkg'
soil_polygons = data +'/geo_files/PFAS_LD1600_Soil_Sample_Polygons.gpkg'
sample_locations = data + '/geo_files/PFAS Groundwater Results.gpkg'
nonLD_gw = data + '/geo_files/Non-LD1600 PFAS Groundwater Results.gpkg'
PFOA_soil_pred = data +'/geo_files/PFOA_prediction_model.gpkg'
PFOS_soil_pred = data +'/geo_files/PFOS_prediction_model.gpkg'

# pfas supporting files
comp_pfas_gw_pkl = projects + '/PFAS_comprehensive/data_files/pfas_gw.pkl'
field_distance = base_folder + '/lookup/field_dist.pkl'
sample_distance =  base_folder + '/lookup/sample_dist.pkl'
nonLD_distance =  base_folder + '/lookup/nonLD_dist.pkl'
# pfas_source =  projects + '/PFAS_comprehensive/data_files/sources.pkl'
pfas_source = base_folder + '/pfas_source.pkl'
pfas_source_xls = data +'/misc_data/Land_App_Data_Copy2.xlsx'


# misc geo layers
landfill_polygons = data + '/geo_files/Estimated Waste Area.gpkg'
roads = data +'/geo_files/MaineDOT_Public_Roads.gpkg'
streams = data +'/geo_files/streams.gpkg'
rivers = data +'/geo_files/rivers.gpkg'
me_outline = data +'/geo_files/Maine_State_outline.gpkg'
quadrangle = data +'/geo_files/24k_grid.gpkg'
surficial = data + '/geo_files/surficial24k.gpkg'
bedrock = data + '/geo_files/bedrock500k.gpkg'
soil = data +'/geo_files/Map Unit Polygons - ME.gpkg'

towns =  data +'/geo_files/Maine_Town_Boundary.gpkg'
zips = data +'/geo_files/zip_code.gpkg'
tax = data + '/geo_files/parcels.gpkg'
ts_area = data+ '/geo_files/Boundary_Area_BRWM.gpkg'
ts_line = data + '/geo_files/Boundary_Line_BRWM.gpkg'
ts_pt = data + '/geo_files/Reference_Point_BRWM.gpkg'

egad_type =  data +'/geo_files/EGAD Site Types.gpkg'
egad_sites =  data +'/geo_files/EGAD_Site_Locations.gpkg'
egad_samples = data +'/geo_files/EGAD_Sample_Locations.gpkg'

site_pts = data +'/waypoints/site_pts.gpkg' # a representative point sites where I have responsibility

def dem_contour_path(num):
    dem = data + '/dem/10_meter_state_tiles/dem_{}_2m_contour.gpkg'.format(num)
    return dem

def dem_tif_path(num):
    dem = data + '/dem/10_meter_state_tiles/dem_{}.tif'.format(num)
    return dem


# letter and other document generator files
letter_image = projects +'/letter_generator/images'
dep_blue = data +'/logo/deplogo_blue.png'
dep_color = data +'/logo/deplogo_color.png'

pfas_coc = base_folder +'/pfas_coc.pdf'
petrol_coc = base_folder +'/petrol_coc.pdf'
al_coc  = base_folder +'/al_coc.pdf'

