import pandas as pd

profile = pd.read_json('https://fingertips.phe.org.uk/api/profiles')

# see all names
profile.loc[:,['Id', 'Name']]

# filter for those that have data
profile = profile[profile.loc[:,'HasAnyData']==True].reset_index(drop=True)

# list all group names inside their profile names
for profile_index in range(len(profile)):
    name = profile.loc[:,'Name'][profile_index]
    print(f"--------PROFILE: {name}")    
    group = profile.GroupMetadata.to_dict()[profile_index]
    for group_index in group:
        print(dict(group_index)['Name'])

def search_profile_names(profile, search_term:str):
    return profile.loc[profile.loc[:,'Name'].str.contains(search_term, case=False)]

search_profile_names(profile, search_term='wider')

# 'perinatal-mental-health', 102
# wider determinants of health 130
# palliative 95

def return_ind_ids_for_profile_id(profile_id:int):
    ind_ids = pd.read_json('https://fingertips.phe.org.uk/api/indicator_metadata/by_profile_id?profile_id=' + str(profile_id))
    return list(ind_ids.columns)

def return_values_for_ind_ids(ind_ids:list, ref_files_date:str):
    all_values = pd.read_csv(f"{ref_files_date}_values.csv")
    values = all_values.loc[all_values.loc[:,'~Indicator ID'].isin(ind_ids)]
    return values

def save_values_for_profile_id(short_profile_name:str, profile_id:int, ref_files_date:str):
    ind_ids = return_ind_ids_for_profile_id(profile_id)
    values = return_values_for_ind_ids(ind_ids, ref_files_date)
    
    file_name = f"{ref_files_date}_values_{short_profile_name}.csv"
    values.to_csv(file_name, index=False)
    print(f"{file_name} successfully saved")
    

save_values_for_profile_id(short_profile_name='musculoskeletal_health', profile_id=76, ref_files_date='2023-08-18')



import pandas as pd

a = pd.read_csv('2023-08-18_indicator_ref.csv')
len(a)
a.Indicator.nunique()