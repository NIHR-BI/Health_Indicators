import pandas as pd

# step 4
## clean concat values file
# 1 - create values table - area_code = Area Code + _ + area_type_id
# area_name = Area Name


# remove stuff
def remove_eng(dataframe:pd.DataFrame()):
    return dataframe.loc[dataframe.loc[:,'Area Type']!='England']


# create values.csv

# create dataset_ref.csv



def run(ref_files_date:str, values_download_date:str, remove_england:bool):
    values_folder_name = ref_files_date+'_values'
    filepath = values_folder_name + '/' + values_download_date + '_values_concatenated.csv'
    data = pd.read_csv(filepath)
    
    if remove_england:
        data = remove_eng(data)
    
    return data
        

a = run('2023-07-24', '2023-07-28', True)