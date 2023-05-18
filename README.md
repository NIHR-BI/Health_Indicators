# Health indicator data sources

## 1. PHE Fingertips

https://fingertips.phe.org.uk/profile/guidance/supporting-information/api

- An API exists for this.

- Python and R libraries also exist for this and don't seem to contain all of the API functionality.

- There are multiple ways to retrieve data. What makes most sense for this project is to retrieive data for a group of indicator ids for one area_type_id at a time.

``` python
import fingertips_py as ftp

data_for_multiple_ind_ids_for_one_area = ftp.retrieve_data.get_data_by_indicator_ids(indicator_ids=ids_as_str, # [Maximum 100]
                                                    area_type_id=area_type_id, # can be found in the documentation
                                                    include_sortable_time_periods=True, # includes an int format column for time period
                                                    is_test=False)
```

- ids_as_str must be in the format of the id numbers separated by %2C which is the character representation for a comma. e.g. 1204%2C1210%2C20401 is for the ids 1204, 1210 and 20401.


## 2. ONS Open Geography

https://www.api.gov.uk/ons/open-geography-portal/#open-geography-portal

- An API exists for this.

- A data set follows the format: 'https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/' + dataset_name + '/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson'. e.g. https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Clinical_Commissioning_Groups_April_2019_Boundaries_EN_BUC_2022/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson
(Note - only FeatureServers can be downloaded, not MapServer)


- dataset_names can be found on this directory: https://services1.arcgis.com/ESMARspQHYMw9BZ9/ArcGIS/rest/services
