from phe_fingertips_save_ref_files import save_all_ref_files
from phe_fingertips_save_values import save_values_for_all_ind_area_combos
from phe_fingertips_concat_values import concat_files_in_folder_and_save


str_date='2023-07-24'


# step 1
## save the ref files from the phe fingertips website and from google sheets
save_all_ref_files()


# step 2
## save values for all indicator and area type combos
save_values_for_all_ind_area_combos(str_date=str_date)


# step 3
## concat
values_folder_name = str_date+'_values'
concat_file_name = values_folder_name + '/' + 'values_concatenated'
concat_files_in_folder_and_save(folder=values_folder_name, save_as_fname=concat_file_name)


# step 4
## clean concat values file
# check if the files for non-15 area types include England(15) on rows and remove these?...
# 1 - create values table - area_code = Area Code + _ + area_type_id
# area_name = Area Name 
