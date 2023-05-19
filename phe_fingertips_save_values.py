from datetime import date
import fingertips_py as ftp
from json import loads
import numpy as np
from math import ceil
from os import listdir
import pandas as pd
from urllib.request import urlopen


def load_combos(str_date:str):
    filename = str_date + '_' + 'one_areatypeid_for_indicatorid.csv'
    data = pd.read_csv(filename)
    return data


def return_ind_list_for_area_type(combos, AreaTypeId):
    return combos[combos['AreaTypeId']==AreaTypeId]['IndicatorId'].values


def save_values(str_date, area_type_id:int):
    combos = load_combos(str_date)
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
        
        filename = ('values/' + today_as_str + '_' +
                    str(area_type_id) + '_' +
                    str(start_index) + 'to' +
                    str(end_index-1) + '.csv'
        )
        
        values.to_csv(filename, index=False)
        
        print(filename + ' successfully saved')


def save_all_values(str_date):
    combos = load_combos(str_date)
    unique_area_type_ids = combos['AreaTypeId'].unique().tolist()
    
    for i in unique_area_type_ids:
        save_values(str_date, i)
    
    print('save_all_values function successfully complete')

# save_all_values('2023-04-24')


def save_values_choose_areas(str_date, areaids:list):   
    for i in areaids:
        save_values(str_date, i)
    
    print('save_all_values function successfully complete')


# save_values_choose_areas('2023-04-24', [201,
#  101,
#  402,
#  302,
#  202,
#  102])


# combos = load_combos('2023-04-24')
# counts = combos.groupby('AreaTypeId')['IndicatorId'].count().values.tolist()
# batch_size = 100
# number_of_batches = [ceil(i/batch_size) for i in counts]
# sum(number_of_batches) # i should have this number of files

def concat_files_in_folder_and_save(folder, save_as_fname):    
    file_names = listdir(folder)
    print(len(file_names))
    return
    appended_data = pd.DataFrame()
    for i in file_names:
        filepath = folder + '/' + i
        data = pd.read_csv(filepath)
        appended_data = pd.concat([appended_data, data])
    appended_data.to_csv(save_as_fname + '.csv', index=False)
    
    print(save_as_fname  + '.csv ' + ' has successfully saved')


concat_files_in_folder_and_save('values', '2023-04-24_values_appended')

data = pd.read_csv('2023-04-24_values_appended.csv')

area_ref = pd.read_csv('2023-04-24_area_hierarchy.csv')
map1 = area_ref.loc[:, ['AreaTypeId', 'Short']].set_index('AreaTypeId').loc[:, 'Short'].to_dict()
map2 = {v: k for k, v in map1.items()}
# map2['England'] = np.nan
map2['Districts & UAs (2021/22-2022/23)'] = 401
map2['Counties & UAs (2021/22-2022/23)'] = 402

data.shape

data['area_type_id'] = data['Area Type'].replace(map2)
data['area_type_id'].unique()

data['indicator_dataset_id'] = data['Indicator ID'].astype(str) + '_' + data['Time period Sortable'].astype(str) + '_' + data['Sex'].astype(str) + '_' + data['Age'].astype(str) + '_' + data['area_type_id'].astype(str)

4014688 * 27 / (400000)

#5,000,000 cells, with a maximum of 256 columns per sheet. Uploaded spreadsheet files that are converted to the Google spreadsheets format can't be larger than 20 MB, and need to be under 400,000 cells and 256 columns per sheet. Check out our detailed spreadsheet size limits tip.
data['indicator_dataset_id'].unique()[0:5]

data.columns

['Area Code',
 'Area Name',
 
 'Indicator ID', 'Indicator Name', 'Parent Code', 'Parent Name',
       ,  'Area Type', 'Sex', 'Age', 'Category Type',
       'Category', 'Time period', 'Value', 'Lower CI 95.0 limit',
       'Upper CI 95.0 limit', 'Lower CI 99.8 limit', 'Upper CI 99.8 limit',
       'Count', 'Denominator', 'Value note', 'Recent Trend',
       'Compared to England value or percentiles', 'Compared to percentiles',
       , 'New data', 'Compared to goal',
       'Time period range']

data['Area Type'].unique()