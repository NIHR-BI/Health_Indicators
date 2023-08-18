import pandas as pd

from phe_fingertips_save_ref_files import save_all_ref_files
from phe_fingertips_save_values import save_values_choose_areas
from phe_fingertips_concat_values import concat_files_in_folder_and_save
from phe_fingertips_save_csvs_value_dataset_ref import save_dataset_ref_values_csvs
from phe_fingertips_save_csv_area_type_ref import save_area_type_ref_csv

################################
# # # please note that if you run this, it takes about 1 hour to run

# # # it can error at step 2 at certain area_ids where it times out. you can rerun the area_ids from where it errored.
################################

# # # step 1 - this takes about a min
# # # save the ref files from the phe fingertips website and from google sheets
save_all_ref_files()

ref_files_date = '2023-08-18'

# # # step 2 - this takes about 30 minutes to 45 minutes depending on how many area types are included
# # # save values for chosen area types
chosen_area_ids = pd.read_csv(ref_files_date + '_area_hierarchy.csv', usecols=['area_type_id']).values.tolist()
chosen_area_ids = [i for sublist in chosen_area_ids for i in sublist]
folder_name = ref_files_date + '_values/'

save_values_choose_areas(ref_files_date=ref_files_date, areaids=chosen_area_ids, folder_name=folder_name)
# save_values_choose_areas(ref_files_date=ref_files_date, areaids=[501, 502], folder_name=folder_name)
# 7 is gps, # 501 is 2023 ltlas, # 502 is utlas

# chosen_area_ids
# save_values_choose_areas(ref_files_date=ref_files_date, areaids=[201], folder_name=folder_name)
# save_values_choose_areas(ref_files_date=ref_files_date, areaids=[101, 402, 302, 202, 102], folder_name=folder_name)

values_download_date = '2023-08-18'

# # # step 3 - this takes about 7 minutes but depends on how much data was saved in the last step
# # # save concat csv of all of the values files together
concat_files_in_folder_and_save(ref_files_date=ref_files_date, values_download_date=values_download_date)


# # # step 4 - this takes about 15 minutes
# # # save dataset_ref.csv and values.csv
save_dataset_ref_values_csvs(ref_files_date=ref_files_date,
                             values_download_date=values_download_date,
                             remove_england=True)


# # # step 5 - this takes about a min
# # # save area_type_ref.csv
save_area_type_ref_csv(ref_files_date)


# # # steps complete! The csvs that go into the dashboard are:
# # # values.csv
# # # dataset_ref.csv
# # # indicator_ref.csv
# # # the rest of the csvs are for reference and can be included in the dashboard if preferred