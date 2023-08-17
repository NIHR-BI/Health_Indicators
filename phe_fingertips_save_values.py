from datetime import date
import fingertips_py as ftp
from math import ceil
from os import mkdir
import pandas as pd


def load_combos(ref_files_date:str):
    '''load the combos from the ref files'''
    filename = ref_files_date + '_' + 'indicatorid_at_areatypeid.csv'
    data = pd.read_csv(filename)
    return data


def return_ind_list_for_area_type(combos, AreaTypeId):
    '''return a list of indicator ids for an area type selected'''
    return combos[combos['AreaTypeId']==AreaTypeId]['IndicatorId'].values


def create_folder(ref_files_date, folder_name):
    '''create a folder named ref_files_date_folder_name'''
    dir_name = ref_files_date+'_'+folder_name
    mkdir(dir_name)
    print(dir_name + ' created successfully')
    

def save_values(ref_files_date:str, area_type_id:int, folder_name:str):
    '''save the values of all of the indicators for a chosen area type
    in batches of 100 due to the api limit'''
    combos = load_combos(ref_files_date)
    replace_comma = '%2C'
    today_as_str = str(date.today())
    
    indicator_list = return_ind_list_for_area_type(combos, area_type_id)
    batch_size = 100
    number_of_batches = ceil(len(indicator_list)/batch_size)
    
    # max 100 indicators can be retrieved at once so need to do this in batches
    for i in range(number_of_batches):
        start_index = i*batch_size
        end_index = (i+1)*batch_size
        batch_indicator_list = indicator_list[start_index: end_index]
        
        ids_as_str = replace_comma.join([str(i) for i in batch_indicator_list])
        
        values = ftp.retrieve_data.get_data_by_indicator_ids(indicator_ids=ids_as_str, # [Maximum 100]
                                                        area_type_id=area_type_id,
                                                        # parent_area_type_id=15,
                                                        # profile_id=None,
                                                        include_sortable_time_periods=True,
                                                        is_test=False)
        
        values['Dataset Downloaded Date'] = today_as_str
        values['area_type_id'] = area_type_id
        values = values.rename(columns={'Value': 'value'})
        values = values.drop_duplicates()
        
        filename = (folder_name + '/' + today_as_str + '_' +
                    str(area_type_id) + '_' +
                    str(start_index) + 'to' +
                    str(end_index-1) + '.csv'
        )
        
        values.to_csv(filename, index=False)
        
        print(filename + ' successfully saved')


def save_values_for_all_ind_area_combos(ref_files_date:str):
    '''run through all of the area types and repeatedly save all of the
    indicator values in batches'''
    create_folder(ref_files_date, 'values')
    combos = load_combos(ref_files_date)
    unique_area_type_ids = combos['AreaTypeId'].unique().tolist()
    
    for i in unique_area_type_ids:
        save_values(ref_files_date, i, ref_files_date+'_values')
    
    print('save_values_for_all_ind_area_combos function successfully complete')


def save_values_choose_areas(ref_files_date:str, areaids:list, folder_name:str):   
    '''save values for chosen areas'''
    for i in areaids:
        save_values(ref_files_date, i, folder_name)
    
    print('save_all_values function successfully complete')
    