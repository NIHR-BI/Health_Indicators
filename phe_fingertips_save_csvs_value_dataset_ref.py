import pandas as pd
import numpy as np


def remove_eng(dataframe:pd.DataFrame()):
    return dataframe.loc[dataframe.loc[:,'Area Type']!='England']


def concat_str_cols(dataframe:pd.DataFrame(), cols:list, concat_str:str):
    return dataframe.loc[:,cols].astype(str).agg(concat_str.join, axis=1)


def create_col_by_concat_cols(new_col_name:str, dataframe:pd.DataFrame(), cols:list, concat_str:str):
    dataframe[new_col_name] = concat_str_cols(dataframe, cols, concat_str)
    return dataframe


def create_col_with_col_plus_brackets(new_col_name:str, dataframe:pd.DataFrame(),
                                      col_first_outisde_brackets:str,
                                      cols_in_brackets:list):
    dataframe[new_col_name] = dataframe.loc[:,col_first_outisde_brackets] + ' [' + concat_str_cols(dataframe, cols_in_brackets, ', ') + ']'
    return dataframe


def create_value_is_null_col(dataframe:pd.DataFrame()):
    dataframe['value_is_null'] = dataframe.loc[:,'Value'].isna().astype(int)
    return dataframe


def replace_nulls_with_val(dataframe:pd.DataFrame(), col:str, null_val, replace_null_val):
    dataframe[col] = dataframe.loc[:,col].replace(null_val, replace_null_val)
    return dataframe


# valuescsv_required_cols = ['Area Code', 'Area Name', 'Indicator ID', 'Time period Sortable',
#                            'Sex', 'Age', 'area_type_id', 'Value', 'Count', 'Denominator',
#                            'Value Note']

# dataset_refcsv_required_cols = ['Dataset Downloaded Date', 'indicator_dataset_id', 'Indicator ID',
#                                 'Time period', 'Time period Sortable', 'Time period range',
#                                 'Sex', 'Age', 'area_type_id']


def save_dataset_ref_values_csvs(ref_files_date:str, values_download_date:str, remove_england:bool):
    values_folder_name = ref_files_date+'_values'
    filepath = values_folder_name + '/' + values_download_date + '_values_concatenated.csv'
    # filepath = values_folder_name + '/' + values_download_date + '_102_700to799.csv'
    data = pd.read_csv(filepath)
    
    # remove england
    if remove_england:
        data = remove_eng(data)
        
    # create area_code
    data = create_col_by_concat_cols('area_code', data, ['Area Code', 'area_type_id'], '_')
    
    # create indicator_dataset_id
    data = create_col_by_concat_cols('indicator_dataset_id', data, ['Indicator ID', 'Time period Sortable', 'Sex', 'Age', 'area_type_id'], '_')
    
    # create Indicator Dataset
    data = create_col_with_col_plus_brackets(new_col_name='Indicator Dataset', dataframe=data,
                                      col_first_outisde_brackets='Indicator Name',
                                      cols_in_brackets=['Age', 'Sex', 'Time period', 'Area Type'])
    
    # create indicator_dataset_group_id
    data = create_col_by_concat_cols('indicator_dataset_group_id', data, ['Indicator ID', 'Time period Sortable', 'Sex', 'Age'], '_')
    
    # create Indicator Dataset Group
    data = create_col_with_col_plus_brackets(new_col_name='Indicator Dataset Group', dataframe=data,
                                      col_first_outisde_brackets='Indicator Name',
                                      cols_in_brackets=['Age', 'Sex', 'Time period'])
    
    # create dataset_group_id
    data = create_col_by_concat_cols('dataset_group_id', data, ['Age', 'Sex', 'Time period Sortable'], '_')   
    
    # create Dataset Group
    data = create_col_by_concat_cols('Dataset Group', data, ['Age', 'Sex', 'Time period'], ', ')
    
    # create value_is_null and replace nulls with null value
    data = create_value_is_null_col(data)
    data = replace_nulls_with_val(data, 'Value', np.nan, -99999)
    # replace value note nas with something
    data = replace_nulls_with_val(data, 'Value note', np.nan, '')
    # rename cols
    rename_cols_dict = {'Time period': 'Time Period',
                        'Time period Sortable': 'Time Period Sortable',
                        'Time period range': 'Time Period Range',
                        'Value note': 'Value Note',
                        'Value': 'value'}
    data = data.rename(columns=rename_cols_dict)
    
    # create dataset_ref.csv
    dataset_cols = ['Dataset Downloaded Date', 'indicator_dataset_id', 'Indicator ID', 'Indicator Dataset', 'indicator_dataset_group_id', 'Indicator Dataset Group', 'dataset_group_id', 'Dataset Group', 'Time Period', 'Time Period Sortable', 'Time Period Range', 'Sex', 'Age', 'area_type_id']
    dataset_cols_dict = {'area_type_id': '~area_type_id'}
    dataset_ref = data.loc[:,dataset_cols].rename(columns=dataset_cols_dict).drop_duplicates()
    
    dataset_ref.to_csv(ref_files_date + '_dataset_ref.csv', index=False)
    print(ref_files_date + '_dataset_ref.csv successfully saved')
    
    # create values.csv
    values_cols = ['area_code', 'Area Name', 'indicator_dataset_id', 'value', 'Count', 'Denominator',
                   'value_is_null', 'Value Note', 'area_type_id', 'Time Period Sortable', 'Age', 'Sex', 'Indicator ID']
    values_cols_dict = {'area_type_id': '~area_type_id',
                         'Time Period Sortable': '~Time Period Sortable',
                         'Age': '~Age',
                         'Sex': '~Sex',
                         'Indicator ID': '~Indicator ID'}
    values = data.loc[:,values_cols].rename(columns=values_cols_dict).drop_duplicates()

    values.to_csv(ref_files_date + '_values.csv', index=False)
    print(ref_files_date + '_values.csv successfully saved')

    # return data, dataset_ref, values


if __name__ == '__main__':
    data, dataset_ref, values = save_dataset_ref_values_csvs(ref_files_date='2023-08-18',
                                        values_download_date='2023-08-18',
                                        remove_england=True)
    
    # print(dataset_ref.columns)
    # print(values.columns)
    # print(values.head())