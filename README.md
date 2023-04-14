# Health indicator data sources

## 1. PHE Fingertips

https://fingertips.phe.org.uk/profile/guidance/supporting-information/api

- An API exists for this.

- Python and R libraries also exist for this and don't seem to contain all of the API functionality.

- There are multiple ways to retrieve data. What makes most sense for this project is to retrieive data for a group of indicator ids for one area_type_id at a time.


## 2. ONS Open Geography

https://www.api.gov.uk/ons/open-geography-portal/#open-geography-portal

- An API exists for this.

- A data set follows the format: 'https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/' + dataset_name + '/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson'

- dataset_names can be found on this directory: https://services1.arcgis.com/ESMARspQHYMw9BZ9/ArcGIS/rest/services
