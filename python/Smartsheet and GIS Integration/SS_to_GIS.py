'''
- Description: This script takes a smartsheet and an Esri Feature layer and will push updates from the smartsheet to the feature layer.
  The purpose of this script is to demonstrate how this process works. 
- Author: Wes Sholders
- Special thanks to Kelsey Ciarrocca for help developing this process!
- Contact: wessholders@gmail.com
'''

#####################
#####- MODULES -#####
#####################
print('Initializing the Smartsheet to GIS update script')
import pytz
import datetime
current_time = datetime.datetime.now(pytz.utc)
cst_timezone = pytz.timezone('US/Central')
current_time_cst = current_time.astimezone(cst_timezone)
print(f'Started at {current_time_cst.strftime("%m/%d/%Y %H:%M:%S")}')
print('\nImporting Modules...')
import smartsheet
from arcgis.gis import GIS
import pandas as pd
import numpy as np
import arcgis as arcgis
print('Modules imported.\n')

####################
#####- INPUTS -#####
####################
portal_url = 'url path to your portal/AGOL'     ###- URL to portal connection
feauture_layer_ID = '1q2w3e4r5t6y7u8i9o0p'      ###- ID of desired feature layer from prtal connection
token = '0p9o8i7u6y5t4r3e2w1q'                  ###- Smartsheet API token
sheet_id = 1234567890                           ###- Smartsheet ID

#########################
#####- SOURCE CODE -#####
#########################
###- Connect to GIS and get the layer
print('Connecting to feature layers...')
gis = GIS(portal_url)
layer_item = gis.content.get(feauture_layer_ID)  
layers = layer_item.layers

###- Connect to feature layer
fset = layers[0].query()
features = fset.features
flayer = layers[0]
print(f'    - {str(flayer.properties.name)}')
print('Connected to feature layers.\n')

###- Connect to Smartsheet
print('Connecting to the smartsheet client...')
smartsheet_client = smartsheet.Smartsheet(access_token=token, api_base=smartsheet.__gov_base__)
sheet = smartsheet_client.Sheets.get_sheet(sheet_id)
print(f'    - Loaded sheet: {sheet.name}')
print('Connected to the smartsheet client.\n')

###- Function to convert Smartsheet data to DataFrame
def simple_sheet_to_dataframe(sheet):
    col_names = [col.title for col in sheet.columns]
    rows = []
    for row in sheet.rows:
        cells = []
        for cell in row.cells:
            cells.append(cell.value)
        rows.append(cells)
    data_frame = pd.DataFrame(rows, columns=col_names)
    return data_frame

###- Convert Smartsheet to DataFrame and replace NaNs with None
print('Creating df from smartsheet...')
df = simple_sheet_to_dataframe(sheet)
df = df.replace({np.nan: None})
df = df.replace({'<Null>': None})

def assemble_updates(row, feature_key, failures, updates_to_push):
    try:
        global_id = row['Global ID']
        edit_feature = {'objectid': feature_key[global_id]}
        
        #edit_feature['EsriFieldName'] = row['SmartsheetFieldName'] ###- This is the syntax of the below records
        edit_feature['unique_id']=row['Unique ID']
        edit_feature['state'] = row['State']
        edit_feature['city'] = row['City']
        edit_feature['zip_code'] = row['Zip Code']
        edit_feature['editor_name'] = row['Editor Name']       
        feat = {'attributes': edit_feature}
        updates_to_push.append(feat)

    except KeyError as ke:
        print(f'KeyError in row {global_id}: {ke}')
        failures[global_id] = str(ke)
    except Exception as e:
        print(f'Error in row {global_id}: {e}')
        failures[global_id] = str(e)

if not df.empty:
    failures = {}
    updates_to_push = []

    ###- Apply the assemble_updates function to each row
    print('Initiating feature layer update...')

    ###- Create a dictionary of GlobalID to OBJECTID for easier reference
    print('    - Creating feature keys')
    feature_keys = {f.attributes['globalid']: f.attributes['objectid'] for f in features}

    ###- Update flayer
    print('    - Assembling updates')
    df.apply(lambda row: assemble_updates(row, feature_keys, failures, updates_to_push), axis=1)

    ###- Debugging: Check for missing GLOBAL_IDs
    print('    - Searching for possible missing GLOBAL_IDs')
    missing_ids = [row['Global ID'] for _, row in df.iterrows() if row['Global ID'] not in feature_keys]
    if missing_ids:
        print('The following GLOBAL_IDs are missing in the feature_keys dictionary:')
        for gid in missing_ids:
            print(gid)
        print()
        
    ###- Attempt to push updates to GIS
    print('    - Attempting to push updates')
    try:
        update_result = flayer.edit_features(updates=updates_to_push, rollback_on_failure=True)
        
        ###- Check if there are any errors in the update result
        if 'updateResults' in update_result:
            for res in update_result['updateResults']:
                if 'error' in res:
                    print(f"Error updating OBJECTID {res['objectId']}: {res['error']['description']}")
                    failures[res['objectId']] = res['error']['description']
        
        if len(failures) > 0:
            print('The following updates failed:')
            for k, v in failures.items():
                print(f'{k} --- {v}')
        else:
            print(f'    - {len(updates_to_push)} records updated.')
            print('Feature layer successfully updated.')
    except Exception as e:
        print(f'An error occurred during the update operation: {e}')

# Capture the end time
end_time = datetime.datetime.now(pytz.utc)
end_time_cst = end_time.astimezone(cst_timezone)
elapsed_time = end_time - current_time
print(f'\nTotal run time: {elapsed_time}\n')