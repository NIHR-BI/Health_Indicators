import pandas as pd
import json
import fingertips_py as ftp
from math import ceil

data = pd.read_csv('region/6.csv')

def get_data_batches(indicator_list, area_type_id, batch_size, folder_name):
    replace_comma = '%2C'

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
        
        filename = (folder_name + '/' +
                    str(area_type_id) + '_' +
                    str(start_index) + 'to' +
                    str(end_index-1) + '.csv'
        )
        
        values.to_csv(filename, index=False)
        
        print(filename + ' successfully saved')

# # concat all of the separate files for 6
# file_names = ['region/6_0to99.csv',
#               'region/6_100to199.csv',
#               'region/6_200to299.csv',
#               'region/6_300to399.csv',
#               'region/6_400to499.csv']

# data = pd.DataFrame()

# for file in file_names:
#     file_data = pd.read_csv(file)
#     data = pd.concat([data, file_data])

# # save the file    
# data.to_csv('region/6.csv', index=False)

# file_name = 'region/302_0to99.csv'

# # drop england
# data = pd.read_csv(file_name)
# data = data.loc[data['Area Name']!='England']
# # # save the file    
# data.to_csv(file_name, index=False)

# # filter data to only include max time period only
# max_time_period = pd.DataFrame(data.groupby(['Indicator ID', 'Sex', 'Age'])['Time period Sortable'].max()).reset_index().drop_duplicates()
# data_max_time = pd.merge(left=max_time_period,
#          right=data,
#          how='inner')
# data_max_time.to_csv(file_name, index=False)

# len(data_max_time)
# len(data)


# # number of sex values for indicators
# data.loc[:,['Indicator ID', 'Sex']].groupby('Indicator ID').nunique()
# # number of age values for indicators
# data.loc[:,['Indicator ID', 'Age']].groupby('Indicator ID').nunique().describe()


# # shape file
# shape_file_name = 'region/9_region_shapes.json'
# with open(shape_file_name, 'r') as contents:
#     shape_json = json.loads(contents)
# shape_json


# # retrieve value data are different areas
# raw_available_indicator_at_area = pd.read_json('https://fingertips.phe.org.uk/api/available_data').fillna(value='null')
# area_ref = pd.read_json('https://fingertips.phe.org.uk/api/area_types').fillna(value='null')

# ids = [90285,90812,90284,90832,92758,93114,93219,93224,93372,342,384,93086,93090,93375]
# ids = (raw_available_indicator_at_area.loc[(raw_available_indicator_at_area['IndicatorId'].isin(ids))
#                                           & (raw_available_indicator_at_area['AreaTypeId']==6)]
#        ['IndicatorId'].values
#        )

# pain_ind_area = raw_available_indicator_at_area.loc[(raw_available_indicator_at_area['IndicatorId'].isin(ids))]

# pd.merge(left = pain_ind_area.pivot_table(values='IndicatorId',
#                           index='AreaTypeId',
#                           aggfunc='count')
#          ,left_on = 'AreaTypeId'
#          ,right = area_ref
#          ,right_on = 'Id'
#          ).sort_values('IndicatorId', ascending=False)


# # use func to save data
# get_data_batches(ids, 302, 100, 'region')