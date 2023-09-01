import pandas as pd

ref_files_date= '2023-08-18'
values_file_name = ref_files_date + '_values.csv'
values = pd.read_csv(values_file_name)

# # # # replace codes starting with nE with E
# values['area_code'] = values.loc[:,'area_code'].replace('^nE', 'E', regex=True)
# # # # save file
# values.to_csv(values_file_name, index=False)


shape_file_date = '2023-08-10'
shape_file_name = f"{shape_file_date}_shapes.csv"
shape = pd.read_csv(shape_file_name, sep='#')

# # # remove wales rows
# shape = shape.loc[~shape.loc[:,'area_code'].str.startswith('W0')]
# # # save file
# shape.to_csv(shape_file_name, sep='#', index=False)

# # # # remove scotland rows
# shape = shape.loc[~shape.loc[:,'area_code'].str.startswith('S12')]
# # # # save file
# shape.to_csv(shape_file_name, sep='#', index=False)


# # # # remove NI rows
# shape = shape.loc[~shape.loc[:,'area_code'].str.startswith('N0')]
# # # # save file
# shape.to_csv(shape_file_name, sep='#', index=False)


# look at how many match
values_subset = values.loc[:,['area_code', '~area_type_id']].drop_duplicates()
shape_subset = shape.loc[:,['area_code', 'area_type_id']].drop_duplicates()

merged = pd.merge(values_subset, shape_subset,
                  how='outer',
                  on='area_code',
                  indicator=True)

merged.loc[merged.loc[:,'_merge']=='right_only']
merged.loc[merged.loc[:,'_merge']=='left_only']
merged.loc[merged.loc[:,'_merge']=='left_only', '~area_type_id'].unique()

merged.groupby(['area_type_id', '_merge']).count()
merged.groupby(['~area_type_id', '_merge']).count()

merged[merged['~area_type_id']==66].area_code.values
