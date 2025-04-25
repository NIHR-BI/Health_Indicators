import pandas as pd
import os
from datetime import date

def save_obesity_area_type_ref_csv(ref_files_date):
    """
    Create and save area type reference CSV file for obesity study.
    
    Args:
        ref_files_date: Date string used in filenames
    
    Returns:
        DataFrame containing the area type reference data
    """
    # Map for area type classes
    class_dict = {
        'region-composite': 'Regions',
        'icb-composite': 'Integrated Care Boards',
        'sub-icb-composite': 'Sub-ICB Locations',
        'ccg-composite': 'Clinical Commissioning Groups',
        'ua-la-composite': 'Lower tier local authorities',
        'ua-county-composite': 'Upper tier local authorities'
    }
    
    # Load area type ID reference
    areatypeid_ref_file = f"{ref_files_date}_areatypeid_ref.csv"
    if not os.path.exists(areatypeid_ref_file):
        print(f"Error: {areatypeid_ref_file} not found.")
        return None
    
    areatypeid_ref = pd.read_csv(
        areatypeid_ref_file,
        usecols=['Id', 'Name', 'Short', 'Class', 'Sequence', 'Indicator Information Downloaded Date']
    ).replace(class_dict)
    
    # Replace 0 sequence with "Not applicable"
    sequence_dict = {0: 'Not applicable'}
    areatypeid_ref['Sequence'] = areatypeid_ref.loc[:,'Sequence'].replace(sequence_dict)
    
    # Fill null Class values with Short
    areatypeid_ref['Class'] = areatypeid_ref.loc[:,'Class'].fillna(areatypeid_ref.loc[:,'Short'])
    
    # Filter to only include area types relevant to obesity study
    # Typically these would be regions, ICBs, and sub-ICBs
    area_types_to_include = []
    
    # Include regions (usually ID starts with 6)
    region_ids = areatypeid_ref[
        (areatypeid_ref['Name'].str.contains('Region')) & 
        (areatypeid_ref['Id'].astype(str).str.startswith('6'))
    ]['Id'].tolist()
    area_types_to_include.extend(region_ids)
    
    # Include ICBs
    icb_ids = areatypeid_ref[
        areatypeid_ref['Name'].str.contains('Integrated Care Board')
    ]['Id'].tolist()
    area_types_to_include.extend(icb_ids)
    
    # Include Sub-ICBs
    sub_icb_ids = areatypeid_ref[
        areatypeid_ref['Name'].str.contains('Sub-ICB') | 
        areatypeid_ref['Name'].str.contains('Sub ICB')
    ]['Id'].tolist()
    area_types_to_include.extend(sub_icb_ids)
    
    # Filter areatypeid_ref to only include relevant area types
    obesity_areatypeid_ref = areatypeid_ref[areatypeid_ref['Id'].isin(area_types_to_include)]
    
    # Create map ID and hierarchy columns
    # This is a simplified version - in production you might want to define this more precisely
    obesity_areatypeid_ref['map_id'] = range(1, len(obesity_areatypeid_ref) + 1)
    
    # Define hierarchy - regions at top, then ICBs, then sub-ICBs
    def assign_hierarchy(row):
        name = row['Name'].lower()
        if 'region' in name:
            return 1
        elif 'integrated care board' in name and 'sub' not in name:
            return 2
        elif 'sub-icb' in name or 'sub icb' in name:
            return 3
        else:
            return 4
    
    obesity_areatypeid_ref['map_id_hierarchy'] = obesity_areatypeid_ref.apply(assign_hierarchy, axis=1)
    
    # Rename Id to area_type_id for consistency
    obesity_areatypeid_ref = obesity_areatypeid_ref.rename(columns={'Id': 'area_type_id'})
    
    # Save to CSV
    output_file = f"{ref_files_date}_obesity_area_type_ref.csv"
    obesity_areatypeid_ref.to_csv(output_file, index=False)
    print(f"{output_file} successfully saved with {len(obesity_areatypeid_ref)} area types")
    
    return obesity_areatypeid_ref

if __name__ == "__main__":
    # Use current date as ref_files_date
    today = str(date.today())
    save_obesity_area_type_ref_csv(today)