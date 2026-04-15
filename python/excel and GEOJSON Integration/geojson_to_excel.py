import pandas as pd
import json

def geojson_to_excel_compatible(geojson_path, excel_path):
    """
    Reads a GeoJSON file and converts it to a compatible Excel file.
    
    - For 'Point' geometries, it creates 'longitude' and 'latitude' columns.
    - For 'image_url' lists, it creates a single comma-separated string.

    Args:
        geojson_path (str): The path to the input GeoJSON file.
        excel_path (str): The path for the output Excel file.
    """
    try:
        with open(geojson_path, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)

        feature_data = []
        for feature in geojson_data['features']:
            properties = feature.get('properties', {})
            geometry = feature.get('geometry')

            # Handle Point geometry
            if geometry and geometry['type'] == 'Point':
                properties['longitude'] = geometry['coordinates'][0]
                properties['latitude'] = geometry['coordinates'][1]
            else:
                properties['geometry_string'] = json.dumps(geometry) if geometry else None
            
            # --- KEY CHANGE FOR IMAGES ---
            # If image_url is a list, join it into a single string for Excel
            if 'image_url' in properties and isinstance(properties['image_url'], list):
                properties['image_urls'] = ", ".join(properties['image_url'])
                del properties['image_url'] # Remove the original list property

            feature_data.append(properties)

        df = pd.DataFrame(feature_data)
        df.to_excel(excel_path, index=False, engine='openpyxl')
        print(f"Successfully converted {geojson_path} to a compatible Excel file at {excel_path}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    # Define your input and output file paths
    input_file =  r'Path\To\Your\Output.geojson'
    output_file = r'Path\To\Your\Excel.xlsx'

    # Note: Make sure to save the new GeoJSON data you provided into the input_file path.
    geojson_to_excel_compatible(input_file, output_file)

