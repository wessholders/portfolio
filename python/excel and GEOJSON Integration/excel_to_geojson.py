import pandas as pd
import json

def excel_to_geojson_compatible(excel_path, geojson_path, lon_col='longitude', lat_col='latitude'):
    """
    Reads a compatible Excel file and converts it back to a GeoJSON file.
    - Uses 'longitude' and 'latitude' columns to create Point geometries.
    - Converts a comma-separated 'image_urls' string back into a list.

    Args:
        excel_path (str): The path to the input Excel file.
        geojson_path (str): The path for the output GeoJSON file.
        lon_col (str): The name of the column with longitude values.
        lat_col (str): The name of the column with latitude values.
    """
    try:
        df = pd.read_excel(excel_path).fillna('') # Use fillna to handle empty cells gracefully

        if lon_col not in df.columns or lat_col not in df.columns:
            raise ValueError(f"Input Excel must contain '{lon_col}' and '{lat_col}' columns.")

        features = []
        for _, row in df.iterrows():
            properties = row.to_dict()
            
            lat = properties.pop(lat_col, None)
            lon = properties.pop(lon_col, None)
            properties.pop('geometry_string', None)

            # --- KEY CHANGE FOR IMAGES ---
            # If 'image_urls' column exists, split the string back into a list
            if 'image_urls' in properties and properties['image_urls']:
                # Split by comma and trim whitespace from each URL
                properties['image_url'] = [url.strip() for url in str(properties['image_urls']).split(',')]
                del properties['image_urls'] # Remove the string version

            # Clean out any property values that are empty strings
            properties = {key: val for key, val in properties.items() if val != ''}

            geometry = None
            if lat != '' and lon != '':
                geometry = {'type': 'Point', 'coordinates': [float(lon), float(lat)]}
            
            feature = {'type': 'Feature', 'properties': properties, 'geometry': geometry}
            features.append(feature)

        feature_collection = {'type': 'FeatureCollection', 'features': features}

        with open(geojson_path, 'w', encoding='utf-8') as f:
            json.dump(feature_collection, f, indent=4)
            
        print(f"Successfully converted {excel_path} back to GeoJSON at {geojson_path}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    input_file = r'Path\To\Your\Excel.xlsx'
    output_file = r'Path\To\Your\Output.geojson'
    
    excel_to_geojson_compatible(input_file, output_file)
