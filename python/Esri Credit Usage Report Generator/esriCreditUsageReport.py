"""
    ###----------------------------------------------###
    ###---------  PYTHON SCRIPT METADATA  -----------###
    ###----------------------------------------------###
    Create Credit Usage Report
    Version 9.0 - 1st October, 2025 - Updated code to collect a count of members/creators using each account
                                  - Updated code to convert input month to all caps
    Inputs - paths to features and parameters
    Outputs - new point feature layer with perpendicular symbolization
    Use - This script is designed to be run from an IDE

    Libraries - NOTE:YOU MUST INSTALL THE XLXSWRITER LIBRARY TO USE THIS TOOL

            Do that by copying and pasting the following code into the terminal and running:

                    pip install xlsxwriter
    
    Created and tested on:
    Windows 10 (64 bit) operating system
    ESRI ArcGIS Pro 3.2.2
    Python 3.11.8 (64 bit)
    Author - Wes Sholders
    Email - wessholders@gmail.com
    Created - 
    ###------------------------------------------------------------ Description ---------------------------------------------------------------------------###
    This stand alone python script will take an input of specified portals and create an excel report noting the credit usage during
    a specified month. 
    NOTE: Be sure to install the xlsxwriter library prior to running the script
    ###----------------------------------------------###
    ###---------  PYTHON SCRIPT METADATA  -----------###
    ###----------------------------------------------###
"""
# %%
####################
#####- INPUTS -#####
####################
# - Output Folder (full path)
output_folder = r'C:\path\to\your\output_folder' # - Test output
month = 'OCT'                                    # - What month do you want the report for? Use first three letters. Example: 'JAN'
year = '25'                                      # - Year in YY format (2024 -> 24)
POC_Administrator = 'Administrator Name'         # - Who is running the report?
null_character = '-'                             # - Symbol used when no data is available (non-existent)

# - Output excel file name (without extension)
output_excel_name = f'USACE-SWG_Credit_Usage_Report_{month.upper()}_20{year}' # - Example USACE-SWG_Credit_Usage_Report_JAN_2025.xlsx
extension = '.xlsx'  # - Output excel file extension (usually .xlsx)

#####################
#####- MODULES -#####
#####################
import datetime
line = '-'*50
print(line)
print('\nInitializing the Credit Usage Report Tool...\n')
start_time = datetime.datetime.now()
print(f'Started at {start_time}\n')
print(line)
print('Loading Modules...')
from openpyxl.styles import Border, Side
import xlsxwriter
import numpy as np
import pandas as pd
from arcgis.gis import GIS

pd.set_option('display.max_columns', None)
#####################
######- MONTH -######
#####################
leap_years = ['24', '28', '32', '36', '40', '44']
month_dict = {
    'JAN': (1, 31),
    'FEB': (2, 29 if year in leap_years else 28),
    'MAR': (3, 31),
    'APR': (4, 30),
    'MAY': (5, 31),
    'JUN': (6, 30),
    'JUL': (7, 31),
    'AUG': (8, 31),
    'SEP': (9, 30),
    'OCT': (10, 31),
    'NOV': (11, 30),
    'DEC': (12, 31)
}
if month.upper() in month_dict:
    start_day = datetime.datetime.strptime(f'01/{month_dict[month.upper()][0]}/{year}', '%d/%m/%y')
    last_day = datetime.datetime.strptime(f'{month_dict[month.upper()][1]}/{month_dict[month.upper()][0]}/{year} 23:59:59', '%d/%m/%y %H:%M:%S')
    print(f'\nThis report will be run from {start_day} to {last_day}.')
else:
    raise ValueError("Invalid month")

#######################
######- PORTALS -######
#######################
portals = {'Portal Description (output sheet name)': ["username", "password"]}

query_df = pd.DataFrame(columns=['Entitlement', 'Total', 'Assigned', 'Remaining', 'AGOL'])
cred_df = pd.DataFrame()
cred_avail_df = pd.DataFrame()

for key, value in portals.items():
    try:
        print('\nSigning into', key)
        gis = GIS(username=value[0], password=value[1])
        print('    - Getting license data')
        for license in gis.admin.license.all():
            try:
                print(f'       {license}')
                t_df = license.report
                t_df['AGOL'] = key

                query_df = pd.concat([query_df, t_df])  # ADDED by WS

            except:
                pass
        print('    - Getting user count')

        assigned_count = len([acc for acc in gis.users.search(max_users=500) if acc.level == "2"])

        all_users = gis.users.search(max_users=500)               

        user_role_dictionary = {} # - Not used, just in case we may want to
        for user in all_users:
            user_role_dictionary[user.username] = user.role
            
  

        print(f'        < Count: {assigned_count}')
        count_dictionary = {'AGOL': key, 'Entitlement': 'Creators', 'Assigned': assigned_count}

        count_series = pd.Series(count_dictionary)
        # Convert the series to a DataFrame and transpose it
        count_df = pd.DataFrame(count_series).T

        # Concatenate the original DataFrame and the transposed Series DataFrame along axis 0
        query_df = pd.concat([query_df, count_df], ignore_index=True)

        ###########################################################
        # - Getting used, available, and merging credit df's
        print('    - Pulling credit usage')
        cred = gis.admin.credits.credit_usage(start_time=last_day, end_time=start_day)
        cred['AGOL'] = key
        cred_series = pd.Series(cred)
        cred_df = pd.concat([cred_df, cred_series], axis=1, ignore_index=True)  # ADDED by WS
        transposed_cred_df = cred_df.T

        print('\n    - Pulling available credits')
        cred_avail = gis.properties.availableCredits
        cred_avail_dict = {'available_credits': cred_avail}
        cred_avail_series = pd.Series(cred_avail_dict)
        cred_avail_df = pd.concat([cred_avail_df, cred_avail_series], axis=1, ignore_index=True)
        transposed_cred_avail_df = cred_avail_df.T

        transposed_cred_df = pd.concat([transposed_cred_df, transposed_cred_avail_df], axis=1, ignore_index=False)
        print(f'        < Credits available: {cred_avail}')
        
    except Exception as e:
        print(e)

####################################################
print("\nGathering Stats...")
query_df['Entitlement'] = query_df['Entitlement'].str.rstrip('N')
portals_df = query_df.pivot_table(index="AGOL", columns="Entitlement", values="Assigned", aggfunc=np.sum)
portals_df = portals_df.fillna(0)
transposed_cred_df = transposed_cred_df.fillna(0)
transposed_cred_df = transposed_cred_df.loc[:, (transposed_cred_df != 0).any(axis=0)]
transposed_cred_df = transposed_cred_df.set_index('AGOL')
portals_df = pd.concat([transposed_cred_df, portals_df], axis=1)


# %%
#############################
######- WRITING EXCEL -######
#############################

print('\nWriting results to XLSX')
workbook = xlsxwriter.Workbook(output_folder + '\\' + output_excel_name + extension)
for index, row in portals_df.iterrows():
    if 'notebooks' and 'schdnotebks' in row:
        a_count = row['notebooks'] + row['schdnotebks']
    elif 'notebooks' in row and 'schdnotebks' not in row:
        a_count = row['notebooks']
    elif 'schdnotebks' in row and 'notebooks' not in row:
        a_count = row['schdnotebks']
    else:
        a_count = 0

    s_count = row['features'] + row['scene'] + row['tiles'] + row['vectortiles'] + row['portal']
    total_count = a_count + s_count

    worksheet = workbook.add_worksheet(index)
    worksheet.set_column('A:A', 2)
    worksheet.set_column('B:R', 14)

    #############################
    #####- DEFINED FORMATS -#####
    #############################
    standardstyle = workbook.add_format({
        'bold' : False,
        'align': 'center',
        'valign': 'vcenter'  
    })
    boldstyle = workbook.add_format({
        'bold': True
    })
    boldright = workbook.add_format({
        'bold': True,
        'align': 'right',
        'valign': 'vcenter',
        'text_wrap': True
    })
    boldcenter = workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True
    })
    boldcentergray = workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'pattern': 1,
        'bg_color': '#e7e6e6'
    })
    input_tan_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'pattern': 1,
        'bg_color': '#ffcc99'
    })
    merge_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'bold': True
    })
    merge_format_input = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'bold': False,
        'bg_color': '#ffcc99'
    })
    merge_format_grey = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'bold': True,
        'bg_color': '#e7e6e6'
    })

    credits_total_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'bold': True,
        'bg_color': '#f2f2f2',
        'font_color': '#fa7d00'
    })

    ###########################
    #####- FILLING CELLS -#####
    ###########################

    worksheet.write('B2', 'Report Date', boldcentergray)
    worksheet.write('C2', 'From: ', boldcentergray)
    worksheet.write('D2', start_day.strftime("%m/%d/%Y"), input_tan_format)
    worksheet.write('E2', 'To: ', boldcentergray)
    worksheet.write('F2', last_day.strftime("%m/%d/%Y"), input_tan_format)

    worksheet.merge_range('B4:E4', 'Office Name', merge_format_grey)
    worksheet.merge_range('B5:E5', 'Headquarters', credits_total_format)
    worksheet.merge_range('F4:I4', 'POC/Administrator', merge_format_grey)
    worksheet.merge_range('F5:I5', POC_Administrator, merge_format_input)

    worksheet.merge_range('B7:G7', 'User Types', merge_format_grey)
    worksheet.write('B8', 'Professional Plus*', boldcenter)
    worksheet.write('C8', 'Professional*', boldcenter)
    worksheet.write('D8', 'Creator', boldcenter)
    worksheet.write('E8', 'Mobile Worker*', boldcenter)
    worksheet.write('F8', 'Contributor*', boldcenter)
    worksheet.write('G8', 'Viewer', boldcenter)
    if 'Proffesional_Plus' in row:
        worksheet.write('B9', str(int(row['Professional_Plus'])), input_tan_format)
    else:
        worksheet.write('C9', null_character, input_tan_format)
    if 'Proffesional' in row:
        worksheet.write('C9', str(int(row['Professional'])), input_tan_format)
    else:
        worksheet.write('B9', null_character, input_tan_format)
    if 'Creators' in row:
        worksheet.write('D9', str(int(row['Creators'])), input_tan_format)
    else:
        worksheet.write('D9', null_character, input_tan_format)
    if 'Mobile_worker' in row:
        worksheet.write('E9', str(int(row['Mobile_Worker'])), input_tan_format)
    else:
        worksheet.write('E9', null_character, input_tan_format)
    if 'Contributor' in row:
        worksheet.write('F9', str(int(row['Contributor'])), input_tan_format)
    else:
        worksheet.write('F9', null_character, input_tan_format)
    if 'Viewers' in row:
        worksheet.write('G9', str(int(row['Viewers'])), input_tan_format)
    else:
        worksheet.write('G9', null_character, input_tan_format)

    worksheet.merge_range('B11:F11', 'Credits Consumed', merge_format_grey)
    worksheet.write('B12', 'Credits Total', boldcenter)
    worksheet.write('C12', 'Storage', boldcenter)
    worksheet.write('D12', 'Analytics', boldcenter)
    worksheet.write('E12', 'Subscriber', boldcenter)
    worksheet.write('F12', 'Published', boldcenter)
    worksheet.write('B13', round((total_count), 3), credits_total_format)
    worksheet.write('C13', round((s_count), 3), input_tan_format)
    worksheet.write('D13', round((a_count), 3), input_tan_format)
    worksheet.write('E13', null_character, input_tan_format)
    worksheet.write('F13', null_character, input_tan_format)

    
    ##########################################################
    ###- Filling out the Locally Purchased Credts Section -###

    worksheet.merge_range('H11:K11', 'Locally Purchased Credits (24 Months)', merge_format_grey)
    worksheet.write('H12', 'Year', boldcentergray)
    worksheet.write('I12', 'Amount', boldcentergray)
    worksheet.write('J12', 'Year', boldcentergray)
    worksheet.write('K12', 'Amount', boldcentergray)
    worksheet.write('H13', ("20" + str((int(year)-2))), input_tan_format)

    worksheet.write('I13', '0', input_tan_format)
    worksheet.write('J13', ("20" + str((int(year)-1))), input_tan_format)
    worksheet.write('K13', '0', input_tan_format)


    #####################################################
    ###- Filling out the Core Products Count Section -###
    worksheet.merge_range('B15:D15', 'Core Product Counts', merge_format_grey)
    # - Pro Desktop Advanced
    worksheet.write('B16', 'Pro Desktop Advanced*', boldcenter)
    if 'desktopAdv' in row:
        worksheet.write('B17', int(row['desktopAdv']), input_tan_format)
    else:
        worksheet.write('B17', null_character, input_tan_format)

    # -Pro Desktop Basic
    worksheet.write('C16', 'Pro Desktop Basic*', boldcenter)
    if 'desktopBasic' in row:
        worksheet.write('C17', str(int(row['desktopBasic'])), input_tan_format)
    else:
        worksheet.write('C17', null_character, input_tan_format)

    # - Pro Desktop Standard
    worksheet.write('D16', 'Pro Desktop Standard*', boldcenter)
    if 'desktopStd' in row:
        worksheet.write('D17', str(int(row['desktopStd'])), input_tan_format)
    else:
        worksheet.write('D17', null_character, input_tan_format)
 

    ##########################################################
    ###- Filling out the middle section: Extension Counts -###
    worksheet.merge_range('F15:R15', 'Extension Counts', merge_format_grey)
    # - Pro 3D Analyst
    worksheet.write('F16', 'Pro 3D Analyst*', boldcenter)
    try:
        worksheet.write('F17', int(row['3DAnalyst']), input_tan_format)
    except:
        worksheet.write('F17', null_character, input_tan_format)

    # - Pro Aviation Airports
    worksheet.write('G16', 'Pro Aviation Airports*', boldcenter)
    try:
        worksheet.write('G17', int(row['airports']), input_tan_format)
    except:
        worksheet.write('G17', null_character, input_tan_format)

    # - Pro Data Reviewer
    worksheet.write('H16', 'Pro Data Reviewer*', boldcenter)
    try:
        worksheet.write('H17', int(row['dataReviewer']), input_tan_format)
    except:
        worksheet.write('H17', null_character, input_tan_format)

    # - Pro Defense Mapping
    worksheet.write('I16', 'Pro Defense Mapping*', boldcenter)
    try:
        worksheet.write('I17', int(row['defense']), input_tan_format)
    except:
        worksheet.write('I17', null_character, input_tan_format)

    # - Pro Geostatistical Analyst
    worksheet.write('J16', 'Pro Geostatistical Analyst*', boldcenter)
    try:
        worksheet.write('J17', int(row['geostatAnalyst']), input_tan_format)
    except:
        worksheet.write('J17', null_character, input_tan_format)

    # - Bathymetry
    worksheet.write('K16', 'Bathymetry*', boldcenter)
    try:
        worksheet.write('K17', int(row['bathymetry']), input_tan_format)
    except:
        worksheet.write('K17', null_character, input_tan_format)

    # - Pro Maritime Charting
    worksheet.write('L16', 'Pro Maritime Charting*', boldcenter)
    try:
        worksheet.write('L17', int(row['maritime']), input_tan_format)
    except:
        worksheet.write('L17', null_character, input_tan_format)

    # - Pro Image Analyst
    worksheet.write('M16', 'Pro Image Analyst*', boldcenter)
    try:
        # This needs to be coded to whatever image analyst name is
        worksheet.write('M17', int(row['imageAnalyst']), input_tan_format)
    except:
        worksheet.write('M17', null_character, input_tan_format)

    # - Pro Network Analyst
    worksheet.write('N16', 'Pro Network Analyst*', boldcenter)
    try:
        worksheet.write('N17', int(row['networkAnalyst']), input_tan_format)
    except:
        worksheet.write('N17', null_character, input_tan_format)

    # - Pro Production Mapping
    worksheet.write('O16', 'Pro Production Mapping*', boldcenter)
    try:
        worksheet.write('O17', int(row['productionMap']), input_tan_format)
    except:
        worksheet.write('O17', null_character, input_tan_format)

    # - Pro Publisher
    worksheet.write('P16', 'Pro Publisher*', boldcenter)
    try:
        worksheet.write('P17', int(row['publisher']), input_tan_format)
    except:
        worksheet.write('P17', null_character, input_tan_format)

    # - Pro Spatial Analyst
    worksheet.write('Q16', 'Pro Spatial Analyst*', boldcenter)
    try:
        worksheet.write('Q17', int(row['spatialAnalyst']), input_tan_format)
    except:
        worksheet.write('Q17', null_character, input_tan_format)

    # - Pro Workflow Manager
    worksheet.write('R16', 'Pro Workflow Manager*', boldcenter)
    try:
        worksheet.write('R17', int(row['workflowMgr']), input_tan_format)
    except:
        worksheet.write('R17', null_character, input_tan_format)

    ###################################################################################
    ###- Filling out the second to last section: ELA Provided Premium Applications -###
    worksheet.merge_range('B19:E19', 'ELA Provided Premium Applications', merge_format_grey)
    worksheet.write('B20', 'Insights', boldcenter)
    try:
        worksheet.write('B21', int(row['Insights']), input_tan_format)
    except:
        worksheet.write('B21', null_character, input_tan_format)
    ###
    worksheet.write('C20', 'Drone2Map', boldcenter)
    try:
        worksheet.write('C21', int(row['drone2MapAdv']), input_tan_format)
    except:
        worksheet.write('C21', null_character, input_tan_format)
    ###
    worksheet.write('D20', 'ArcGIS Maps for Power BI', boldcenter)
    try:
        worksheet.write('D21', int(row['workflowMgr']), input_tan_format)
    except:
        worksheet.write('D21', null_character, input_tan_format)
    ###
    worksheet.write('E20', 'App Studio Standard', boldcenter)
    try:
        worksheet.write('E21', int(row['appstudiostd']), input_tan_format)
    except:
        worksheet.write('E21', null_character, input_tan_format)
    ###

# - Filling out the bottom Section: Locally Purchased Premium Applications
    worksheet.merge_range('G19:Q19', 'Locally Purchased Premium Applications', merge_format_grey)
    worksheet.write('G20', 'Insights', boldcenter)
    try:
        worksheet.write('G21', int(row['Insights']), input_tan_format)
    except:
        worksheet.write('G21', null_character, input_tan_format)
    ###
    worksheet.write('H20', 'Business Analyst Online*', boldcenter)
    try:
        worksheet.write('H21', int(row['BusinessAnlyst']), input_tan_format)
    except:
        worksheet.write('H21', null_character, input_tan_format)
    ###
    worksheet.write('I20', 'Drone2Map Standard', boldcenter)
    try:
        worksheet.write('I21', int(row['drone2mapstandard']), input_tan_format)
    except:
        worksheet.write('I21', null_character, input_tan_format)
        ###
    worksheet.write('J20', 'Navigator*', boldcenter)
    try:
        worksheet.write('J21', int(row['Navigator']), input_tan_format)
    except:
        worksheet.write('J21', null_character, input_tan_format)
        ###
    worksheet.write('K20', 'Tracker', boldcenter)
    try:
        worksheet.write('K21', int(row['workflowMgr']), input_tan_format)
    except:
        worksheet.write('K21', null_character, input_tan_format)
    ###
    worksheet.write('L20', 'Community Analyst*', boldcenter)
    try:
        worksheet.write('L21', int(row['CommunityAnlyst']), input_tan_format)
    except:
        worksheet.write('L21', null_character, input_tan_format)
    ###
    worksheet.write('M20', 'Drone2Map Advanced', boldcenter)
    try:
        worksheet.write('M21', int(row['drone2MapAdv']), input_tan_format)
    except:
        worksheet.write('M21', null_character, input_tan_format)
    ###
    worksheet.write('N20', 'ArccGIS Maps for Power BI', boldcenter)
    try:
        worksheet.write('N21', int(row['workflowMgr']), input_tan_format)
    except:
        worksheet.write('N21', null_character, input_tan_format)
    ###
    worksheet.write('O20', 'App Studio Standard', boldcenter)
    try:
        worksheet.write('O21', int(row['appstudiostd']), input_tan_format)
    except:
        worksheet.write('O21', null_character, input_tan_format)
    ###
    worksheet.write('P20', 'ArcGIS Image for Online*', boldcenter)
    try:
        worksheet.write('P21', int(row['imageforonline']), input_tan_format)
    except:
        worksheet.write('P21', null_character, input_tan_format)
    ###
    worksheet.write('Q20', 'Location Sharing*', boldcenter)
    try:
        worksheet.write('Q21', int(row['locationsharing']), input_tan_format)
    except:
        worksheet.write('Q21', null_character, input_tan_format)
    ###

    ##############################
    #####- DEFINING BORDERS -#####
    ##############################

    def top_border(workbook, worksheet, first_row, first_col, last_col):
        # top
        worksheet.conditional_format(first_row, first_col, first_row, last_col,
                                     {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'top': 1})})

    def bottom_border(workbook, worksheet, first_row, first_col, last_col):
        # top
        worksheet.conditional_format(first_row, first_col, first_row, last_col,
                                     {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'bottom': 1})})

    bottom_border(workbook, worksheet, 0, 1, 5)
    bottom_border(workbook, worksheet, 1, 1, 5)

    bottom_border(workbook, worksheet, 2, 1, 8)
    bottom_border(workbook, worksheet, 4, 1, 8)

    bottom_border(workbook, worksheet, 5, 1, 6)
    bottom_border(workbook, worksheet, 8, 1, 6)

    bottom_border(workbook, worksheet, 9, 1, 5)
    bottom_border(workbook, worksheet, 12, 1, 5)

    bottom_border(workbook, worksheet, 9, 7, 10)
    bottom_border(workbook, worksheet, 12, 7, 10)

    bottom_border(workbook, worksheet, 13, 1, 3)
    bottom_border(workbook, worksheet, 16, 1, 3)

    bottom_border(workbook, worksheet, 13, 5, 17)
    bottom_border(workbook, worksheet, 16, 5, 17)

    bottom_border(workbook, worksheet, 17, 1, 4)
    bottom_border(workbook, worksheet, 20, 1, 4)

    bottom_border(workbook, worksheet, 17, 6, 16)
    bottom_border(workbook, worksheet, 20, 6, 16)

end_time = datetime.datetime.now()
run_time = ((end_time - start_time))

print(f'\nThe output excel file has been saved in this folder:\n{output_folder}')

print(f'\n\nTotal time to run: {run_time}\n')
print(line)
workbook.close()
