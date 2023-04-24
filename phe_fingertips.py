from datetime import date
import fingertips_py as ftp
from json import loads
import pandas as pd
from urllib.request import urlopen

def save_url_as_csv(url_dtype, url, filename):
    if url_dtype=='json':
        data = pd.read_json(url)
    elif url_dtype=='csv':
        data = pd.read_csv(url)   
    else:
        raise Exception("url_dtype: json or csv")
            
    today_as_str = str(date.today())
    csvname = today_as_str + '_' + filename + '.csv'
    data.to_csv(csvname, index = False)
    print(csvname + ' successfully saved')

def save_indicatorid_at_areatypeid():
    url = 'https://fingertips.phe.org.uk/api/available_data'
    filename = 'indicatorid_at_areatypeid'
    save_url_as_csv('json', url, filename)

def save_areatypeid_ref():
    url = 'https://fingertips.phe.org.uk/api/area_types'
    filename = 'areatypeid_ref'
    save_url_as_csv('json', url, filename)

def save_indicator_ref():
    url = 'https://fingertips.phe.org.uk/api/indicator_metadata/csv/all'
    filename = 'indicator_ref'
    save_url_as_csv('csv', url, filename)
        
def save_area_hierarchy():
    url = 'https://docs.google.com/spreadsheets/u/0/d/15RhWWsHPPMLWoxR5sJcpK-vraRkidRY8jsAb_Y_5GwI/gviz/tq?tqx=out:csv&tq&gid=963757659&headers=1'
    filename = 'area_hierarchy'
    save_url_as_csv('csv', url, filename)
    
def save_all():
    save_indicatorid_at_areatypeid()
    save_areatypeid_ref()
    save_indicator_ref()
    save_area_hierarchy()
    
save_all()







def load_csv(date, data_id):
    data_ref = {'a': 'indicatorid_at_areatypeid',
                'b': 'areatypeid_ref',
                'c': 'indicator_ref',
                'd': 'area_hierarchy'
    }
    
    filename = date + '_' + data_ref[data_id] + '.csv'
    
    data = pd.read_csv(filename, )
    return data


def load_all_csvs(date):
    a, b, c, d = (load_csv(date, 'a'),
                  load_csv(date, 'b'),
                  load_csv(date, 'c'),
                  load_csv(date, 'd'),
    )
    return a, b, c, d


def find_first_combo(data, map_position):
    '''Taking data combos with hierarchy and map_position, return 1 combo'''
    
    data = data[data['map_position']==map_position].loc[:, ['IndicatorId','hierarchy','AreaTypeId', 'map_position']]
    data['rank'] = data.groupby('IndicatorId')['hierarchy'].rank(method='dense')
    return data[data['rank']==1].drop('rank', axis=1)


def save_one_areatypeid_for_indicatorid(date):
    indicatorid_at_areatypeid = load_csv(date, 'a')
    area_hierarchy = load_csv(date, 'd')
    
    indicatorid_at_areatypeid_with_hierarchy = pd.merge(left=area_hierarchy, right=indicatorid_at_areatypeid,
                                                        left_on='AreaTypeId', right_on='AreaTypeId',
                                                        how='inner')
    
    one_areatypeid_for_indicatorid = pd.concat([find_first_combo(indicatorid_at_areatypeid_with_hierarchy, 'left'),
                                                find_first_combo(indicatorid_at_areatypeid_with_hierarchy, 'middle'),
                                                find_first_combo(indicatorid_at_areatypeid_with_hierarchy, 'right')]
    )
                                               
    one_areatypeid_for_indicatorid.to_csv('one_areatypeid_for_indicatorid.csv', index=False)
    
    print('one_areatypeid_for_indicatorid.csv successfully saved')
    

# save_one_areatypeid_for_indicatorid('2023-04-24')