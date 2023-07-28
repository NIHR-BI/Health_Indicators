from os import listdir
import pandas as pd


def concat_files_in_folder_and_save(str_date:str):    
    values_folder_name = str_date+'_values'
    file_names = listdir(values_folder_name)
    
    appended_data = pd.DataFrame()
    for i in file_names:
        filepath = values_folder_name + '/' + i
        data = pd.read_csv(filepath)
        appended_data = pd.concat([appended_data, data])
        
    concat_file_path = values_folder_name + '/' + 'values_concatenated'
    appended_data.to_csv(concat_file_path + '.csv', index=False)
    
    print(concat_file_path  + '.csv ' + ' has successfully saved')
