import pandas as pd

profile = pd.read_json('https://fingertips.phe.org.uk/api/profiles')

# (profile.rename(columns={'Id':'profile_id',
#                          'Name': 'Profile',
#                          'Key': 'profile_key'})
#  .to_csv(f"2023-09-07_profile_ref.csv", index=False)
# )

# see all names
profile.loc[:,['Id', 'Name']]

profile.head()

# filter for those that have data
profile = profile[profile.loc[:,'HasAnyData']==True].reset_index(drop=True)

# list all group names inside their profile names
# for profile_index in range(len(profile)):
#     name = profile.loc[:,'Name'][profile_index]
#     print(f"--------PROFILE: {name}")    
#     group = profile.GroupMetadata.to_dict()[profile_index]
#     for group_index in group:
#         print(dict(group_index)['Name'])

def search_profile_names(profile, search_term:str):
    return profile.loc[profile.loc[:,'Name'].str.contains(search_term, case=False)]

search_profile_names(profile, search_term='wider')

# 'perinatal-mental-health', 102
# wider determinants of health 130
# palliative 95

def return_ind_ids_for_profile_id(profile_id:int):
    ind_ids = pd.read_json('https://fingertips.phe.org.uk/api/indicator_metadata/by_profile_id?profile_id=' + str(profile_id))
    return list(ind_ids.columns)


def return_values_for_ind_ids(all_values, ind_ids:list, ref_files_date:str):
    values = all_values.loc[all_values.loc[:,'~Indicator ID'].isin(ind_ids)]
    return values


def save_values_for_profile_id(all_values, short_profile_name:str, profile_id:int, ref_files_date:str):
    ind_ids = return_ind_ids_for_profile_id(profile_id)
    values = return_values_for_ind_ids(all_values, ind_ids, ref_files_date)
    
    file_name = f"{ref_files_date}_values_for_profiles/{ref_files_date}_values_{short_profile_name}.csv"
    values.to_csv(file_name, index=False)
    print(f"{file_name} successfully saved")
    

def save_profile_indicator_combos(date_str:str, profile_ids:list):
    combos_concat = pd.DataFrame()
    for profile_id in profile_ids:
        combos = pd.DataFrame()
        combos['Indicator ID'] = return_ind_ids_for_profile_id(profile_id)    
        combos['Profile ID'] = profile_id
        combos_concat = pd.concat([combos_concat, combos])
    file_name = f"{date_str}_profile_to_indicator.csv"
    combos_concat.to_csv(file_name, index=False)
    print(f"{file_name} has been successfully saved")
    # return combos_concat

# save_profile_indicator_combos(date_str='2023-09-07',
#                                   profile_ids=profile.loc[:,'Id'].unique())

 
ref_files_date='2023-08-18'
all_values = pd.read_csv(f"{ref_files_date}_values.csv")

for i, profile_id in enumerate(profile.loc[:,'Id']):
    short_profile_name = profile.loc[i,'Key']
    save_values_for_profile_id(all_values=all_values, short_profile_name=short_profile_name,
                            profile_id=profile_id, ref_files_date=ref_files_date)



# import pandas as pd

# a = pd.read_csv('2023-08-18_indicator_ref.csv')
# len(a)
# a.Indicator.nunique()