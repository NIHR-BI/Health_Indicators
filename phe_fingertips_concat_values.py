from os import listdir
import pandas as pd


def concat_files_in_folder_and_save(folder, save_as_fname):    
    file_names = listdir(folder)
    print(len(file_names))
    
    appended_data = pd.DataFrame()
    for i in file_names:
        filepath = folder + '/' + i
        data = pd.read_csv(filepath)
        appended_data = pd.concat([appended_data, data])
    appended_data.to_csv(save_as_fname + '.csv', index=False)
    
    print(save_as_fname  + '.csv ' + ' has successfully saved')
