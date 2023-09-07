# Health indicator data sources

## OHID Fingertips, indicator values

https://fingertips.phe.org.uk/profile/guidance/supporting-information/api

- An API exists for this.

- Python and R libraries also exist for this and don't seem to contain all of the API functionality.

- There are multiple ways to retrieve data. What makes most sense for this project is to retrieive data for a group of indicator ids for one `area_type_id` at a time.

``` python
import fingertips_py as ftp

data_for_multiple_ind_ids_for_one_area = ftp.retrieve_data.get_data_by_indicator_ids(indicator_ids=ids_as_str, # [Maximum 100]
                                                    area_type_id=area_type_id, # can be found in the documentation
                                                    include_sortable_time_periods=True, # includes an int format column for time period
                                                    is_test=False)
```

- ids_as_str must be in the format of the id numbers separated by %2C which is the character representation for a comma. e.g. 1204%2C1210%2C20401 is for the ids 1204, 1210 and 20401.


## ONS Open Geography, shape values

https://www.api.gov.uk/ons/open-geography-portal/#open-geography-portal

- An API exists for this.

- A data set follows the format: 'https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/' + dataset_name + '/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson'. e.g. https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Clinical_Commissioning_Groups_April_2019_Boundaries_EN_BUC_2022/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson
(Note - only FeatureServers can be downloaded, not MapServer)


- dataset_names can be found in this directory: https://services1.arcgis.com/ESMARspQHYMw9BZ9/ArcGIS/rest/services


# An overview of how the code works to save the data

## OHID Fingertips, indicator values

See the [pipeline script](https://github.com/NIHR-BI/Health_Indicators/blob/main/phe_fingertips_run_pipeline.py).

1. A table of `indicator_id`s available at `area_type_id`s is downloaded from the API.
2. For user chosen `area_type_id`s, save all `indicator_id` values that are available at these `area_type_id`s. These are in chunks of 100 indicators per file as this is the APIs limit.
3. Concatenate together all of the separate value files into one file.
4. Clean the concatenated values file to be in the structure that we need. Save a dataset_ref file which is metadata.
5. Save metadata for `area_type_id`.

## ONS Open Geography, shape values

See the [script](https://github.com/NIHR-BI/Health_Indicators/blob/main/ons_open_geography.ipynb) which is currently not a module.

1. For each of the shapes that you need, find the name of it in the [ONS directory](https://services1.arcgis.com/ESMARspQHYMw9BZ9/ArcGIS/rest/services).
2. Download the shape files.
3. Concatenate the shape files together and save them as one large file.
4. Clean the concatenated shape file to be in the structure that we need.

# Brief explanation of how the data is shown on QlikSense

QlikSense dashboards are currently internal.

Data for an indicator is available for:
- Different data collection periods, called `time_period_sortable` in the data
- Different age groups
- Different sex groups
- Different geographical groupings, called `area_type_id`. An `area_type_id` is an `area_type_class` at a specific `area_type_year_configuration`. For example, `area_type_id` 301 is the LTLA `area_type_class` at 2020 `area_type_year_configuration`

A unique indicator_dataset_id is made up of `indicator_id`, `time_period_sortable`, sex, age, and `area_type_id`. Only a single indicator_dataset_id can be mapped at a time.

For an `indicator_id`, we only want the latest `area_type_year_configuration` for each `area_type_class` and then we only want the latest time_period. 
1. For each unique combination of `indicator_id` and `area_type_class`, only keep the latest (max) `area_type_year_configuration`.
2. Keeping 1) above, for each unique combination of `indicator_id` and `area_type_class`, only keep the latest (max) `time_period_sortable`.
Now for each unique `indicator_id` and `area_type_class` combination, there will only be 1 `area_type_year_configuration` and 1 `time_period_sortable` left.
3. Then the rest of the data can be loaded in with `WHERE EXISTS` statements to only include what is left in previous steps.

![image](https://github.com/NIHR-BI/Health_Indicators/assets/87127667/06c9e5d7-1719-4256-8c2b-111b0c49a6c6)
