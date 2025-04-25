from datetime import date
import fingertips_py as ftp
from math import ceil
import os
import pandas as pd

def create_directory_if_not_exists(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
        return True
    return False

def load_obesity_indicators(ref_files_date):
    """Load obesity indicators from the reference files."""
    filename = f"{ref_files_date}_obesity_indicators.csv"
    if os.path.exists(filename):
        data = pd.read_csv(filename)
        return data['Indicator ID'].tolist()
    else:
        raise FileNotFoundError(f"Obesity indicators file not found: {filename}")

def get_area_type_ids_for_obesity(area_ref):
    """Get the latest area type IDs for regions, ICBs, and sub-ICBs."""
    # Find latest region area type
    region_id = area_ref[(area_ref['Name'].str.contains('Region')) & 
                        (area_ref['Id'].astype(str).str.startswith('6'))]['Id'].max()
    
    # Find latest ICB area type
    icb_id = area_ref[area_ref['Name'].str.contains('Integrated Care Board')]['Id'].max()
    
    # Find latest Sub-ICB area type
    sub_icb_id = area_ref[(area_ref['Name'].str.contains('Sub-ICB')) | 
                         (area_ref['Name'].str.contains('Sub ICB'))]['Id'].max()
    
    area_ids = [region_id, icb_id, sub_icb_id]
    print(f"Using area IDs: Regions={region_id}, ICBs={icb_id}, Sub-ICBs={sub_icb_id}")
    
    return area_ids

def load_indicator_area_combos(ref_files_date, obesity_indicator_ids, area_ids):
    """Load the combinations of obesity indicators and area types."""
    filename = f"{ref_files_date}_indicatorid_at_areatypeid.csv"
    if os.path.exists(filename):
        combos = pd.read_csv(filename)
        # Filter to only include obesity indicators and selected area types
        obesity_combos = combos[
            (combos['IndicatorId'].isin(obesity_indicator_ids)) & 
            (combos['AreaTypeId'].isin(area_ids))
        ]
        return obesity_combos
    else:
        raise FileNotFoundError(f"Indicator-area combinations file not found: {filename}")

def return_ind_list_for_area_type(combos, area_type_id):
    """Return a list of indicator IDs for an area type selected."""
    return combos[combos['AreaTypeId'] == area_type_id]['IndicatorId'].values

def save_values(ref_files_date, area_type_id, indicator_list, folder_name):
    """Save the values of obesity indicators for a chosen area type in batches."""
    replace_comma = '%2C'
    today_as_str = str(date.today())
    
    batch_size = 100
    number_of_batches = ceil(len(indicator_list) / batch_size)
    
    # Max 100 indicators can be retrieved at once, so do this in batches
    for i in range(number_of_batches):
        start_index = i * batch_size
        end_index = min((i + 1) * batch_size, len(indicator_list))
        batch_indicator_list = indicator_list[start_index:end_index]
        
        ids_as_str = replace_comma.join([str(i) for i in batch_indicator_list])
        
        try:
            values = ftp.retrieve_data.get_data_by_indicator_ids(
                indicator_ids=ids_as_str,
                area_type_id=area_type_id,
                include_sortable_time_periods=True,
                is_test=False
            )
            
            values['Dataset Downloaded Date'] = today_as_str
            values['area_type_id'] = area_type_id
            values = values.drop_duplicates()
            
            filename = os.path.join(
                folder_name,
                f"{today_as_str}_obesity_{area_type_id}_{start_index}to{end_index-1}.csv"
            )
            
            values.to_csv(filename, index=False)
            print(f"{filename} successfully saved with {len(values)} rows")
        
        except Exception as e:
            print(f"Error retrieving data for area type {area_type_id}, batch {start_index}-{end_index-1}: {e}")

def save_obesity_values_choose_areas(ref_files_date, areaids, obesity_indicator_ids):
    """Save obesity indicator values for chosen area types."""
    # Create values folder
    values_folder = f"{ref_files_date}_obesity_values"
    create_directory_if_not_exists(values_folder)
    
    for area_id in areaids:
        # Get indicators available for this area type
        combos = load_indicator_area_combos(ref_files_date, obesity_indicator_ids, [area_id])
        area_indicators = return_ind_list_for_area_type(combos, area_id)
        
        if len(area_indicators) == 0:
            print(f"No obesity indicators available for area type ID {area_id}")
            continue
        
        print(f"Saving values for {len(area_indicators)} obesity indicators for area type ID {area_id}")
        save_values(ref_files_date, area_id, area_indicators, values_folder)
    
    print("save_obesity_values_choose_areas function successfully complete")
    return values_folder

if __name__ == "__main__":
    # Example usage:
    today = str(date.today())
    
    # Load area reference data to get area type IDs
    area_ref = pd.read_csv(f"{today}_areatypeid_ref.csv")
    area_ids = get_area_type_ids_for_obesity(area_ref)
    
    # Load obesity indicators
    obesity_indicators = load_obesity_indicators(today)
    
    # Save values for the obesity indicators at the selected area types
    save_obesity_values_choose_areas(today, area_ids, obesity_indicators)