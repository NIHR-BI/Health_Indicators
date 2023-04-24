from datetime import date
import fingertips_py as ftp
from json import loads
from math import ceil
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

save_all_values('2023-04-24')
