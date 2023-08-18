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
                                 usecols=['area_type_id', 'map_id', 'map_id_hierarchy']
    )
    
    area_type_ref = (pd.merge(area_hierarchy, areatypeid_ref,
                     how='left',
                     left_on='area_type_id', right_on='Id')
             .drop(columns='Id')
    )
    
    area_type_ref.to_csv(ref_files_date + '_area_type_ref.csv', index=False)
    print(ref_files_date + '_area_type_ref.csv successfully saved')
    
    # return area_type_ref


if __name__ == '__main__':
    ref_files_date = '2023-08-18'
    test = save_area_type_ref_csv(ref_files_date)
    