'''
- Description: This script takes a smartsheet and an Esri Feature layer and will push updates from the smartsheet to the feature layer.
  The purpose of this script is to demonstrate how this process works. 
- Author: Wes Sholders
- Special thanks to Kelsey Ciarrocca for help developing this process!
- Contact: wessholders@gmail.com
'''

#####################
#####- Modules -#####
#####################
import pytz
import datetime
current_time = datetime.datetime.now(pytz.utc)
cst_timezone = pytz.timezone('US/Central')
current_time_cst = current_time.astimezone(cst_timezone)
print(f'Initiating the GIS to Smartsheet script...\nStarted at {current_time_cst.strftime("%m/%d/%Y %H:%M:%S")}\n')
import smartsheet
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import pandas as pd
separator = ('-'*75)

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

#################
#####- GIS -#####
#################
###- Initialize ArcGIS client
print('Connecting to feature layers...')
try:
    gis = GIS(portal_url)
    all_layer_items = gis.content.get(feauture_layer_ID)
    all_layers = all_layer_items.layers
except:
    raise Exception(f'Error connecting to the GIS portal.\nPossible causes:\n    - Incorrect portal_url: {portal_url}\n    - Incorrect feature_layer_ID: {feauture_layer_ID}')

###- Initialize the empty layer dictionary, this is helpful as you will be able to sort by keys later (good way to track multiple feauture layers)
layer_dictionary = {}

###- Connect to the feature sublayer and append to dictionary
def sublayer_connector(sublayer_index, tag):
    flayer_URL = all_layers[sublayer_index].url
    flayer = FeatureLayer(flayer_URL)
    flayer_query = flayer.query()
    layer_dictionary[tag] = flayer_query
    print(f'    - {str(all_layers[sublayer_index].properties.name)}')

sublayer_connector(0,'Test Environment') ###- Corresponds with the sublayer index and an arbitrary tag
print('Connected to feature layers.\n')

#####################################
#####- Building the dictionary -#####
#####################################
###- Each pair in the dictionary corresponds to a column header and associated value in the smartsheet
print('Creating the dataframe...')
attribute_list = []
for key, value in layer_dictionary.items():
    for feature in value:
        created_timestamp = feature.attributes['created_date']  ###- This method is needed to display Arc timestamps in the Smartsheet
        created_dt_s = datetime.datetime.fromtimestamp(created_timestamp / 1000)
        GIS_created_date = created_dt_s.strftime('%m/%d/%Y %H:%M:%S') 

        ###- This method creates a dictionary including the specified attributes below for every record in the feature layer.
        ###- Each dictionary is then appended to a list to create a list of dictionaries, which are then turned into a pandas DF.
        attribute_dictionary = {
                #'Smartsheet Column Name': feature.attributes['esriFieldName'],     ###- This is the syntax of the below portions of the dictionary
                'Unique ID': feature.attributes['uniqueid'],
                'State': feature.attributes['state'],
                'City': feature.attributes['city'],
                'Zip Code': feature.attributes['zip_code'],
                'Editor Name': feature.attributes['editor_name'],
                'Layer Name': key,
                'GIS Created By': feature.attributes['created_user'],
                'GIS Created Date': GIS_created_date,
                'Global ID': feature.attributes['globalid']
            }
        ###- Create a list of dictionaries
        attribute_list.append(attribute_dictionary)

###- Create merged recently edited utility dictionary
to_be_updated_df = pd.DataFrame(attribute_list)
to_be_updated_df.sort_values(by='Unique ID', ascending=True, inplace=True)
print('Dataframe created.\n')
print(f'{separator}\n{separator}')

###############################################
######- Connect to the smartsheet client -#####
###############################################
print('\nConnecting to the smartsheet client...')
try:
    smartsheet_client = smartsheet.Smartsheet(access_token=token, api_base=smartsheet.__gov_base__) ###- We have to use the GOV version
    ###- Fetch the existing sheet details
    sheet = smartsheet_client.Sheets.get_sheet(sheet_id)
    print(f'    - Loaded Sheet: {sheet.name}')
except:
    raise Exception(f'Error connecting to the sheet.\nPossible causes:\n    - The API token: {token} may be incorrect\n    - The sheet_id: {sheet_id} may be incorrect')
print('Connected to the smartsheet client.\n')

print('Updating the smartsheet...')
###- Create a dictionary mapping column IDs to column names
print('    - Column mapping')
column_map = {col.id: col.title for col in sheet.columns}

###- Retrieve all Global IDs from Smartsheet
smartsheet_GLOBALIDs = set()
for row in sheet.rows:
    for cell in row.cells:
        column_name = column_map[cell.column_id]
        if column_name == 'Global ID':
            smartsheet_GLOBALIDs.add(cell.value)

print('    - Identifying missing GLOBALIDs')
###- Extract GLOBALIDs from the dataframe
gis_GLOBALIDs = set(to_be_updated_df['Global ID'])

###- Find GLOBALIDs in GIS that are not in Smartsheet
missing_GLOBALIDs = gis_GLOBALIDs - smartsheet_GLOBALIDs

###- This "if" statement will add any rows that are in the feature layer, but are not in the smartsheet
if missing_GLOBALIDs:
    print(f"    - There are GLOBALIDs in GIS but not in Smartsheet\n        - {missing_GLOBALIDs}")
    missing_GLOBALIDs_df = to_be_updated_df[to_be_updated_df['Global ID'].isin(missing_GLOBALIDs)]
    
    ###- Convert DataFrame to list of dictionaries
    GLOBALID_list_of_dictionaries = missing_GLOBALIDs_df.to_dict(orient='records')
    column_map_missing_GIDs = {}
    for column in sheet.columns:
        column_map_missing_GIDs[column.title] = column.id

    ###- Prepare rows for Smartsheet
    print('    - Preparing to add missing GLOBALIDs from GIS to smartsheet')
    rows = []
    for row_data in GLOBALID_list_of_dictionaries:
        cells = []
        for column_title, cell_value in row_data.items():
            column_id = column_map_missing_GIDs.get(column_title)
            if column_id is not None:
                ###- Ensure cell_value is not None
                cell_value = '' if pd.isnull(cell_value) else cell_value
                cells.append({
                    'column_id': column_id,
                    'value': cell_value
                })
        rows.append(smartsheet.models.Row({'to_bottom': True, 'cells': cells}))
    ###- Add rows to the sheet
    try:
        smartsheet_client.Sheets.add_rows(sheet_id, rows)
    except smartsheet.exceptions.SmartsheetException as e:
        print(f"        - Error adding rows: {e}")
    print('    - Rows added from GIS to smartsheet')   

###- List to hold rows that need to be updated
gis_global_IDs = set(to_be_updated_df['Global ID'])
rows_to_update = []
print('    - Appending data')
###- Loop through each row in the Smartsheet
for row in sheet.rows:
    global_ID = None
    for cell in row.cells:
        column_name = column_map[cell.column_id]
        if column_name == 'Global ID':
            global_ID = cell.value
            break

    ###- Only process rows where global_ID is in the GIS dataframe
    if global_ID in gis_global_IDs:
        gis_row = to_be_updated_df[to_be_updated_df['Global ID'] == global_ID].iloc[0]

        ###- Create a new row object for updates
        update_row = smartsheet.models.Row()
        update_row.id = row.id

        ###- Loop through each cell in the Smartsheet row
        for cell in row.cells:
            column_name = column_map[cell.column_id]

            if column_name in to_be_updated_df.columns:
                smartsheet_value = cell.value
                gis_value = gis_row[column_name]

                ###- Handle date conversion
                if pd.isna(gis_value):
                    gis_value = ''  ###- Convert None to an empty string if the date is missing
                elif isinstance(gis_value, pd.Timestamp):
                    ###- Convert Timestamp to string
                    gis_value = gis_value.strftime('%Y-%m-%d')

                ###- Compare and update if necessary
                ###- if smartsheet_value != gis_value and gis_value is not None and gis_value != '':
                if smartsheet_value != gis_value:
                    new_cell = smartsheet.models.Cell()
                    new_cell.column_id = cell.column_id
                    new_cell.value = gis_value
                    update_row.cells.append(new_cell)

        if update_row.cells:
            rows_to_update.append(update_row)

###- Update the rows in Smartsheet
if rows_to_update:
    smartsheet_client.Sheets.update_rows(sheet_id, rows_to_update)

print(f'Smartsheet update complete.\n')

# Capture the end time
end_time = datetime.datetime.now(pytz.utc)
end_time_cst = end_time.astimezone(cst_timezone)
elapsed_time = end_time - current_time
print(f'\nTotal run time: {elapsed_time}\n')