import pandas as pd
import numpy as np
import os

def remove_eng(dataframe):
    """Remove England rows from the dataframe."""
    return dataframe.loc[dataframe.loc[:,'Area Type']!='England']

def concat_str_cols(dataframe, cols, concat_str):
    """Concatenate string columns with a specified separator."""
    return dataframe.loc[:,cols].astype(str).agg(concat_str.join, axis=1)

def create_col_by_concat_cols(new_col_name, dataframe, cols, concat_str):
    """Create a new column by concatenating existing columns."""
    dataframe[new_col_name] = concat_str_cols(dataframe, cols, concat_str)
    return dataframe

def create_col_with_col_plus_brackets(new_col_name, dataframe, col_first_outside_brackets, cols_in_brackets):
    """Create a new column with one column followed by bracketed, comma-separated columns."""
    dataframe[new_col_name] = (
        dataframe.loc[:,col_first_outside_brackets] + 
        ' [' + 
        concat_str_cols(dataframe, cols_in_brackets, ', ') + 
        ']'
    )
    return dataframe

def create_value_is_null_col(dataframe):
    """Create a column indicating if the value is null."""
    dataframe['value_is_null'] = dataframe.loc[:,'Value'].isna().astype(int)
    return dataframe

def replace_nulls_with_val(dataframe, col, null_val, replace_null_val):
    """Replace nulls in a column with a specified value."""
    dataframe[col] = dataframe.loc[:,col].replace(null_val, replace_null_val)
    return dataframe

def save_obesity_dataset_ref_values_csvs(ref_files_date, remove_england=True):
    """
    Process the concatenated obesity values file to create dataset_ref and values files.
    
    Args:
        ref_files_date: Date string used in filenames
        remove_england: Whether to remove England data
    """
    values_folder_name = f"{ref_files_date}_obesity_values"
    filepath = os.path.join(values_folder_name, "all_obesity_values.csv")
    
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} not found.")
        return None, None
    
    print(f"Processing {filepath}...")
    data = pd.read_csv(filepath)
    print(f"Loaded {len(data)} rows.")
    
    # Remove England data if requested
    if remove_england:
        data = remove_eng(data)
        print(f"After removing England data: {len(data)} rows.")
    
    # Create area_code
    data = create_col_by_concat_cols('area_code', data, ['Area Code', 'area_type_id'], '_')
    
    # Create indicator_dataset_id
    data = create_col_by_concat_cols(
        'indicator_dataset_id', 
        data, 
        ['Indicator ID', 'Time period Sortable', 'Sex', 'Age', 'area_type_id'], 
        '_'
    )
    
    # Create Indicator Dataset
    data = create_col_with_col_plus_brackets(
        new_col_name='Indicator Dataset', 
        dataframe=data,
        col_first_outside_brackets='Indicator Name',
        cols_in_brackets=['Age', 'Sex', 'Time period', 'Area Type']
    )
    
    # Create indicator_dataset_group_id
    data = create_col_by_concat_cols(
        'indicator_dataset_group_id', 
        data, 
        ['Indicator ID', 'Time period Sortable', 'Sex', 'Age'], 
        '_'
    )
    
    # Create Indicator Dataset Group
    data = create_col_with_col_plus_brackets(
        new_col_name='Indicator Dataset Group', 
        dataframe=data,
        col_first_outside_brackets='Indicator Name',
        cols_in_brackets=['Age', 'Sex', 'Time period']
    )
    
    # Create dataset_group_id
    data = create_col_by_concat_cols(
        'dataset_group_id', 
        data, 
        ['Age', 'Sex', 'Time period Sortable'], 
        '_'
    )
    
    # Create Dataset Group
    data = create_col_by_concat_cols(
        'Dataset Group', 
        data, 
        ['Age', 'Sex', 'Time period'], 
        ', '
    )
    
    # Create value_is_null and replace nulls with null value
    data = create_value_is_null_col(data)
    data = replace_nulls_with_val(data, 'Value', np.nan, -99999)
    
    # Replace value note NAs with empty string
    data = replace_nulls_with_val(data, 'Value note', np.nan, '')
    
    # Rename columns
    rename_cols_dict = {
        'Time period': 'Time Period',
        'Time period Sortable': 'Time Period Sortable',
        'Time period range': 'Time Period Range',
        'Value note': 'Value Note',
        'Value': 'value'
    }
    data = data.rename(columns=rename_cols_dict)
    
    # Create dataset_ref.csv
    dataset_cols = [
        'Dataset Downloaded Date', 'indicator_dataset_id', 'Indicator ID', 
        'Indicator Dataset', 'indicator_dataset_group_id', 'Indicator Dataset Group', 
        'dataset_group_id', 'Dataset Group', 'Time Period', 'Time Period Sortable', 
        'Time Period Range', 'Sex', 'Age', 'area_type_id'
    ]
    dataset_cols_dict = {'area_type_id': '~area_type_id'}
    dataset_ref = data.loc[:,dataset_cols].rename(columns=dataset_cols_dict).drop_duplicates()
    
    dataset_ref_file = f"{ref_files_date}_obesity_dataset_ref.csv"
    dataset_ref.to_csv(dataset_ref_file, index=False)
    print(f"{dataset_ref_file} successfully saved with {len(dataset_ref)} rows")
    
    # Create values.csv
    values_cols = [
        'area_code', 'Area Name', 'indicator_dataset_id', 'value', 'Count', 
        'Denominator', 'value_is_null', 'Value Note', 'area_type_id', 
        'Time Period Sortable', 'Age', 'Sex', 'Indicator ID'
    ]
    values_cols_dict = {
        'area_type_id': '~area_type_id',
        'Time Period Sortable': '~Time Period Sortable',
        'Age': '~Age',
        'Sex': '~Sex',
        'Indicator ID': '~Indicator ID'
    }
    values = data.loc[:,values_cols].rename(columns=values_cols_dict).drop_duplicates()

    values_file = f"{ref_files_date}_obesity_values.csv"
    values.to_csv(values_file, index=False)
    print(f"{values_file} successfully saved with {len(values)} rows")

    return dataset_ref, values

if __name__ == "__main__":
    # Use current date as ref_files_date
    from datetime import date
    today = str(date.today())
    
    dataset_ref, values = save_obesity_dataset_ref_values_csvs(
        ref_files_date=today,
        remove_england=True
    )