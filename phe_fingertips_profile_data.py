import pandas as pd
profile = pd.read_json('https://fingertips.phe.org.uk/api/profiles')
# 'perinatal-mental-health', 102

perinatal_ids = pd.read_json('https://fingertips.phe.org.uk/api/indicator_metadata/by_profile_id?profile_id=102')

perinatal_ids.columns

# filter to get the dataset_ids
dataset_ref = pd.read_csv('2023-07-24_dataset_ref.csv')

perinatal_dataset_ref = dataset_ref.loc[dataset_ref.loc[:,'Indicator ID'].isin(perinatal_ids.columns)]
len(perinatal_dataset_ref)

perinatal_dataset_ref.to_csv('2023-07-24_dataset_ref_perinatal.csv', index=False)

# filter the values for only the dataset_ids of interest
values = pd.read_csv('2023-07-24_values.csv')
perinatal_values = pd.merge(perinatal_dataset_ref.loc[:,'dataset_id'],
                            values,
                            how='inner')

perinatal_values.to_csv('2023-07-24_values_perinatal.csv', index=False)


# filter the shapes for only the area types of interest
shapes = pd.read_csv('2023-05-19_shapes.csv')

shapes.loc[:,'area_type_id'].nunique()

dataset_ref.loc[:,'~area_type_id'].nunique()




# 2023-07-24_indicator_ref.csv
