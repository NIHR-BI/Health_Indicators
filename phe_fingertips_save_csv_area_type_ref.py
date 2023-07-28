import pandas as pd


def fill_with_col_b_if_null_col_a(dataframe:pd.DataFrame(), col_a:str, col_b:str):
    dataframe.loc[:,col_a]
    

def save_area_type_ref_csv(ref_files_date):
    class_dict = {'stp-composite': 'Sustainability and Transformation Footprints',
                  'ccg-composite': 'Clinical Commissioning Groups',
                  'ua-la-composite': 'Lower tier local authorities',
                  'ua-county-composite': 'Upper tier local authorities'}
    
    areatypeid_ref = (pd.read_csv(ref_files_date + '_areatypeid_ref.csv',
                                usecols=['Id', 'Name', 'Short', 'Class',
                                         'Sequence', 'Indicator Information Downloaded Date']
                                )
                          .replace(class_dict)
        )
    
    sequence_dict = {0: 'Not applicable'}
    areatypeid_ref['Sequence'] = areatypeid_ref.loc[:,'Sequence'].replace(sequence_dict)

    areatypeid_ref['Class'] = areatypeid_ref.loc[:,'Class'].fillna(areatypeid_ref.loc[:,'Short'])
    
    area_hierarchy = pd.read_csv(ref_files_date + '_area_hierarchy.csv',
                                 usecols=['AreaTypeId', 'map_id', 'hierarchy']
    )
    

    area_type_ref = (pd.merge(area_hierarchy, areatypeid_ref,
                     how='left',
                     left_on='AreaTypeId', right_on='Id')
             .drop(columns='Id')
    )
    
    col_dict = {'AreaTypeId': 'area_type_id',
                'hierarchy': 'map_id_hierarchy',
                'Name': 'Area Type Name',
                'Short': 'Area Type Short Name',
                'Class': 'Area Type Class',
                'Sequence': ' Area Type Year Configuration'}
    
    area_type_ref = area_type_ref.rename(columns=col_dict)
    
    area_type_ref.to_csv(ref_files_date + '_area_type_ref.csv')
    
    # return area_type_ref

