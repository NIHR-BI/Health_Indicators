import pandas as pd

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


# # drop england
# data = pd.read_csv('region/6.csv')
# data = data.loc[data['Area Name']!='England']
# # # save the file    
# data.to_csv('region/6.csv', index=False)


data = pd.read_csv('region/6.csv')


data