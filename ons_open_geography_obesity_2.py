import pandas as pd
import json
import urllib.request
import os
from datetime import date

def create_directory_if_not_exists(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def create_geojson_url(dataset_name):
    """Create URL for a GeoJSON dataset from ONS Open Geography Portal."""
    url = f'https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/{dataset_name}/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson'
    return url

def retrieve_geojson_from_url(url):
    """Retrieve GeoJSON data from a URL and convert to DataFrame."""
    with urllib.request.urlopen(url) as contents:
        geojson_data = json.loads(contents.read())
    
    shape_data = pd.json_normalize(geojson_data['features'])
    return shape_data

def save_geojson_from_url(url, filename):
    """Save GeoJSON data from a URL to a CSV file."""
    shape_data = retrieve_geojson_from_url(url)
    shape_data.to_csv(filename, index=False)
    print(f"{filename} successfully saved")
    return shape_data

def save_geojson_from_dataset_name(dataset_name, directory=None):
    """Save GeoJSON data for a specific dataset to a CSV file."""
    url = create_geojson_url(dataset_name)
    if directory:
        filename = os.path.join(directory, f"{dataset_name}.csv")
    else:
        filename = f"{dataset_name}.csv"
    return save_geojson_from_url(url, filename)

def get_shape_directory():
    """Get a directory of available shape datasets from ONS."""
    shape_directory_url = 'https://services1.arcgis.com/ESMARspQHYMw9BZ9/ArcGIS/rest/services?f=pjson'
    with urllib.request.urlopen(shape_directory_url) as contents:
        shape_directory = json.loads(contents.read())
    shape_directory = pd.json_normalize(shape_directory['services'])
    shape_directory = shape_directory.loc[shape_directory['type']=='FeatureServer']
    return shape_directory

def shape_name_contains(shape_directory, *args):
    """Filter shape directory for entries containing specified strings."""
    query = shape_directory.copy()
    for arg in args:
        arg = arg.lower()
        query = query[query['name'].str.lower().str.contains(arg)]
    return query

def find_latest_shape_for_area_type(shape_directory, area_type):
    """Find the most recent shape dataset for a specified area type."""
    if area_type == "region":
        # Find region boundaries
        matches = shape_name_contains(shape_directory, "region", "boundar")
    elif area_type == "icb":
        # Find ICB (Integrated Care Board) boundaries
        icb_matches = [
            shape_name_contains(shape_directory, "integrated_care_board"),
            shape_name_contains(shape_directory, "icb")
        ]
        icb_matches = [match for match in icb_matches if not match.empty]
        matches = pd.concat(icb_matches) if icb_matches else pd.DataFrame()
    elif area_type == "sub_icb":
        # Find Sub-ICB boundaries
        sub_icb_matches = [
            shape_name_contains(shape_directory, "sub", "integrated_care_board"),
            shape_name_contains(shape_directory, "sub", "icb")
        ]
        sub_icb_matches = [match for match in sub_icb_matches if not match.empty]
        matches = pd.concat(sub_icb_matches) if sub_icb_matches else pd.DataFrame()
    else:
        raise ValueError(f"Unsupported area type: {area_type}")
    
    # Sort by name to get the most recent first (assumes naming convention includes dates)
    if not matches.empty:
        matches = matches.sort_values('name', ascending=False)
        return matches.iloc[0]
    else:
        print(f"No match found for {area_type}")
        return None

def get_shapes_for_obesity_study():
    """Get and save shape files for regions, ICBs, and sub-ICBs."""
    today = str(date.today())
    shape_directory = get_shape_directory()
    
    # Create shape files directory
    shapes_dir = f"{today}_obesity_shapes"
    create_directory_if_not_exists(shapes_dir)
    
    # Dictionary to store the shape datasets
    shape_datasets = {}
    
    # Find and save shape files for each area type
    for area_type in ["region", "icb", "sub_icb"]:
        dataset_info = find_latest_shape_for_area_type(shape_directory, area_type)
        if dataset_info is not None:
            dataset_name = dataset_info['name']
            shape_datasets[area_type] = dataset_name
            print(f"Found {area_type} dataset: {dataset_name}")
            save_geojson_from_dataset_name(dataset_name, shapes_dir)
    
    # Save shape datasets info
    shape_info = pd.DataFrame([
        {"area_type": area_type, "dataset_name": dataset_name} 
        for area_type, dataset_name in shape_datasets.items()
    ])
    shape_info.to_csv(f"{shapes_dir}/shape_datasets_info.csv", index=False)
    print(f"{shapes_dir}/shape_datasets_info.csv successfully saved")
    
    # Combine all shapes into one file
    all_shapes = pd.DataFrame()
    for area_type, dataset_name in shape_datasets.items():
        file_path = os.path.join(shapes_dir, f"{dataset_name}.csv")
        try:
            shapes = pd.read_csv(file_path)
            # Add area_type column
            shapes['area_type'] = area_type
            all_shapes = pd.concat([all_shapes, shapes])
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    # Save combined shapes
    combined_file = f"{shapes_dir}/combined_shapes.csv"
    all_shapes.to_csv(combined_file, index=False)
    print(f"{combined_file} successfully saved")
    
    return shapes_dir, shape_datasets

if __name__ == "__main__":
    get_shapes_for_obesity_study()