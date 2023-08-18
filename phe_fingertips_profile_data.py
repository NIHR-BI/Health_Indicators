import pandas as pd
profile = pd.read_json('https://fingertips.phe.org.uk/api/profiles')
# 'perinatal-mental-health', 102

perinatal_ids = pd.read_json('https://fingertips.phe.org.uk/api/indicator_metadata/by_profile_id?profile_id=102')
len(perinatal_ids.columns)

# # filter to get the dataset_ids
dataset_ref = pd.read_csv('2023-08-18_dataset_ref.csv')
perinatal_dataset_ref = dataset_ref.loc[dataset_ref.loc[:,'Indicator ID'].isin(perinatal_ids.columns)]

# filter the values for only the dataset_ids of interest
values = pd.read_csv('2023-08-18_values.csv')
perinatal_values = pd.merge(perinatal_dataset_ref.loc[:,'indicator_dataset_id'],
                            values,
                            how='inner')

perinatal_values.to_csv('2023-08-18_values_perinatal.csv', index=False)
