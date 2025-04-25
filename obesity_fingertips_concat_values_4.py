from datetime import date 
from os import listdir
import pandas as pd
import os

def concat_files_in_folder_and_save(ref_files_date):
    """
    Concatenate all CSV files in the obesity values folder into a single file.
    
    Args:
        ref_files_date: Date string used in folder name
    """    
    values_folder_name = f"{ref_files_date}_obesity_values"
    
    if not os.path.exists(values_folder_name):
        print(f"Error: Folder {values_folder_name} does not exist.")
        return None
    
    file_names = [f for f in listdir(values_folder_name) if f.endswith('.csv')]
    
    if not file_names:
        print(f"Error: No CSV files found in {values_folder_name}.")
        return None
    
    print(f"Found {len(file_names)} CSV files to concatenate.")
    
    appended_data = pd.DataFrame()
    for i in file_names:
        try:
            filepath = os.path.join(values_folder_name, i)
            data = pd.read_csv(filepath)
            appended_data = pd.concat([appended_data, data])
            print(f"Added {len(data)} rows from {i}")
        except Exception as e:
            print(f"Error reading {i}: {e}")
    
    appended_data = appended_data.drop_duplicates()
    print(f"After removing duplicates, total rows: {len(appended_data)}")
    
    concat_file_path = os.path.join(values_folder_name, f"all_obesity_values.csv")
    appended_data.to_csv(concat_file_path, index=False)
    
    print(f"{concat_file_path} has successfully saved with {len(appended_data)} rows")
    
    return concat_file_path

if __name__ == "__main__":
    # Use current date as ref_files_date
    today = str(date.today())
    concat_files_in_folder_and_save(today)