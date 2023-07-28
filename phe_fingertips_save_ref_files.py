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
    data['Indicator Information Downloaded Date'] = today_as_str
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
    url = 'https://docs.google.com/spreadsheets/u/0/d/1yWPMu8cHllEdVl0kuUjjJR5V8yVrnU4jZTIlM1a1XGg/gviz/tq?tqx=out:csv&tq&gid=963757659&headers=1'
    filename = 'area_hierarchy'
    save_url_as_csv('csv', url, filename)
    
def save_all_ref_files():
    save_indicatorid_at_areatypeid()
    save_areatypeid_ref()
    save_indicator_ref()
    save_area_hierarchy()
    