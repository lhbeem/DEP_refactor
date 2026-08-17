## refactor commands

function juxta { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\refactor\juxtapose.py" @args }
function make_site { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\refactor\make_site.py" @args }
function site { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\refactor\site.py" @args }
function rag { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\refactor\compare_rags.py" @args }
function lab { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\refactor\lab.py" @args }
function edd_test { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\refactor\edd_test.py" @args }
function folder { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\refactor\folder.py" @args }

function letter { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\gen_letter.py" @args }
function egad { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\egad.py" @args }
function coc { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\coc_generator.py" @args }
function site_pt { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\egad_site_pt.py" @args }
function ll2utm { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\ll2utm.py" @args}
function ec {& python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\ec.py" @args}

function load_profile {. $profile ;
			Copy-Item -Path "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1" -Destination "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\lookup\"} 

function pfas_setup { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\pfas_utils\pfas_data_setup.py" @args}
function pfas_map   { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\pfas_utils\pfas_map.py" @args}
function pfas_table { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\pfas_utils\pfas_table.py" @args}
function pfas_table_edd { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\pfas_utils\pfas_table_edd.py" @args}
function haz { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\pfas_utils\haz_index.py" @args}
function pfas_query { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\pfas_utils\pfas_query.py" @args}


function sop { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\sop.py" @args}
function rule { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\rules.py" @args}
function make_site_folder { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\make_site_folder.py" @args}
function soil_type { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\soil_legend.py" @args }

function allshp	{ & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\all_shp_convert.py"}
function shp2gpkg { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\shp2gpkg.py" @args}

function new_site { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\site_bg_info.py" @args}
function all_folder { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\omni_folder.py" @args }


## py distribution testing 
function py_dist { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\utils\py_distribution.py" @args}
function test_find { & python "G:\brwm\Lucas_Beem\py\pfas_comprehensive\seq2site.py" @args }
function test_map  { & python "G:\brwm\Lucas_Beem\py\pfas_comprehensive\pfas_map.py" @args }


## Letter Functions (slowly being replaced by refactor)
function letter_filter { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\letter_generator\gen_filter_letter.py" @args }
function letter_pfas { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\py\pfas_letter\gen_pfas_letter.py" @args }
# function invoice { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\letter_generator\gen_pace_stamp.py" @args }
# function letter { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\letter_generator\gen_letter.py" @args }
# function letter_final { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\letter_generator\gen_last_sample_letter.py" @args }
# function letter_close { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\letter_generator\gen_closure_letter.py" @args }
# function pfas_soil { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\data_parse\pfas_soil_table.py" @args}


## functions that do not utilize python

function proj { cd "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\"}
function lab_track { start "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\refactor\lookup\Spill_lab_tracking.xlsx"}
function doc2pdf { & "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\WindowsPowerShell\d2p.ps1"}
function profile {notepad $profile}

function launch_egad {MSTSC "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\rdps\egad.rdp"; pass }
function arc {MSTSC "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\rdps\arcpro.rdp" ; pass }
function pass {Set-Clipboard -Value "j,h%&x-P7<7WtC&}"}
function pass_or {Set-Clipboard -Value "2p7n^D0b1,!)m-Y"}

## geo commands 

# function shp2gpkg { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\utils\shp2gpkg.py" @args}
# function allshp	{ & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\utils\all_shp_convert.py"}
function egad_dist { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\utils\egad_dist.py" @args }
function pt2town { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\utils\town_from_point.py" @args }


## document search and manipualtion 

function heic { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\utils\heic_convert.py" @args}
function search { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\utils\pdf_search.py" @args}
# function sop { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\utils\sop.py" @args}
# function rule { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\utils\rules.py" @args}
# Set-Alias -name rules -Value rule
function open_edd {& python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\utils\open_edd.py" @args}


## maps 

function map { &  python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\make_map\make_map.py" @args}
function site_map { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\make_map\site_map.py" @args }


## other 

function egad_desc { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\utils\egad_desc.py" @args }
# function all_folder { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\utils\omni_folder.py" @args }
function tax_map { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\utils\tax.py" @args}
function azimuth { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\utils\azimuth.py" @args}



### abondoned functions 

# function site  {  & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\site_tracking\sites.py" @args }
# Set-Alias -name sites -Value site
#function make_site { python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\site_tracking\sites.py" -make_pickle}
#		      python  "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\site_tracking\make_site_pt.py" }
#Set-Alias -name make_sites -Value make_site
# function lab  { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\site_tracking\lab.py" @args }
# Set-Alias -name labs -Value lab
# function folder { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\site_tracking\folder.py" @args }
# function rag { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\data_parse\compare_rags.py" @args }
# Set-Alias -name rags -Value rag
# function juxta { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\data_parse\juxtapose.py" @args }
# function egad ($arg1, $arg2) {if ($PSBoundParameters.ContainsKey('arg2')){
#					python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\utils\all_egad.py" $arg1 | sls $arg2 }
#				else {python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\utils\all_egad.py" $arg1 }}
# function site_pt { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\utils\egad_site_pt.py" @args }
# function ll2utm { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\utils\llto26919.py" @args}
# function pfas_table { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\PFAS_comprehensive\pfas_table.py" @args}
# function haz { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\data_parse\haz_index.py" @args}
# function pfas_setup { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\PFAS_comprehensive\pfas_data_setup.py" @args}
# function pfas_map   { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\PFAS_comprehensive\pfas_map.py" @args}
# function pfas_findsite { & python "C:\Users\Lucas.Beem\OneDrive - State of Maine\Documents\Projects\PFAS_comprehensive\seq2site.py" @args}






