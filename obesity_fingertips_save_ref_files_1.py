from datetime import date
import fingertips_py as ftp
import pandas as pd
import json
import urllib.request

def save_url_as_csv(url_dtype, url, filename):
    """Generic function to save data from a URL to a CSV file."""
    if url_dtype == 'json':
        data = pd.read_json(url)
    elif url_dtype == 'csv':
        data = pd.read_csv(url)   
    else:
        raise Exception("url_dtype: json or csv")
            
    today_as_str = str(date.today())
    data['Indicator Information Downloaded Date'] = today_as_str
    csvname = today_as_str + '_' + filename + '.csv'
    data.to_csv(csvname, index=False)
    print(csvname + ' successfully saved')
    return data

def save_indicatorid_at_areatypeid():
    """Save indicator ID to area type ID mappings."""
    url = 'https://fingertips.phe.org.uk/api/available_data'
    filename = 'indicatorid_at_areatypeid'
    return save_url_as_csv('json', url, filename)

def save_areatypeid_ref():
    """Save area type ID reference data."""
    url = 'https://fingertips.phe.org.uk/api/area_types'
    filename = 'areatypeid_ref'
    return save_url_as_csv('json', url, filename)

def save_indicator_ref():
    """Save indicator reference metadata."""
    url = 'https://fingertips.phe.org.uk/api/indicator_metadata/csv/all'
    filename = 'indicator_ref'
    return save_url_as_csv('csv', url, filename)

def save_obesity_indicators(indicator_metadata):
    """Filter indicators to only include obesity-related ones."""
    today_as_str = str(date.today())
    
    # Search for obesity-related terms in indicator metadata
    obesity_terms = ['obesity', 'overweight', 'weight', 'bmi', 'body mass index', 'diet', 'nutrition']
    
    obesity_indicators = indicator_metadata[
        indicator_metadata['Indicator'].str.lower().str.contains('|'.join(obesity_terms)) |
        indicator_metadata['Definition'].str.lower().str.contains('|'.join(obesity_terms))
    ]
    
    print(f"Found {len(obesity_indicators)} obesity-related indicators")
    
    # Save the list of obesity indicators for reference
    obesity_file = today_as_str + '_obesity_indicators.csv'
    obesity_indicators.to_csv(obesity_file, index=False)
    print(f"{obesity_file} successfully saved")
    
    return obesity_indicators

def save_all_ref_files():
    """Save all reference files needed for obesity indicators study."""
    indicator_at_area = save_indicatorid_at_areatypeid()
    area_ref = save_areatypeid_ref()
    indicator_metadata = save_indicator_ref()
    obesity_indicators = save_obesity_indicators(indicator_metadata)
    
    print("All reference files successfully saved.")
    
    return {
        'indicator_at_area': indicator_at_area,
        'area_ref': area_ref,
        'indicator_metadata': indicator_metadata,
        'obesity_indicators': obesity_indicators
    }

if __name__ == "__main__":
    save_all_ref_files()