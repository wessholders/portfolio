"""
Script Name: SQL Query Generator
Description: This script uses the pandas library to access a specified excel workbook and
             read a specified column as a pandas data frame. It will then use other user
             inputs to generate serveral "Or" statements that can be pasted into the SQL
             portion of the "Select by Attributes" tool. This tool was created for 
             searching for many unique ID's, but may be adapted for other purposes.
             You must pip install pyperclip. Sometimes you need that for long queries.
  
Author: Wes Sholders
Contact: wessholders@gmail.com
Creation Date: 03/28/2024
Python Version: 3.11.11
Tool Version: 4.0
Version Date: 04/15/2026
"""
import pandas as pd
import re
import datetime
import pyperclip


###---------------------------------###
###---------- USER INPUTS---------- ###
###---------------------------------###

path_to_excel = r"C:\Path\To\Your\Excel.xlsx"     ### Path to the Excel Spreadsheet with your Query Items 
sheet_name = 'Sheet1'                            ### Name of the worksheet in the input workbook with your Query items 
excel_column_name = 'Item Number'                ### Header of the column containing your query items
field_name = 'itemnumber'                        ### Field name (NOTE: NOT FIELD ALIAS) of the desired field to query in Arc Pro
operator = 'Or'                                  ### The type of search operator used in your query (usually Or)

###---------------------------------###
###---------- SOURCE CODE ----------###
###---------------------------------###
formatted_time = datetime.datetime.now().strftime("%m/%d/%Y %H:%M")
def title_block():
     print(f'###------------------------------------------###\n###---------- SQL QUERY GENERATOR -----------###\n###------------ {formatted_time} ------------###\n')

###- Check for valid field name
if not re.match(r'^[a-zA-Z_]\w*$', field_name):
        title_block()
        print(f"Error: Invalid field name\nInvalid name: '{field_name}'\n\nThe field name cannot begin with a number. The rest of the name cannot contain\nany characters that are not alphanumeric character or an underscore\nYou should just copy and paste this from Pro.\n")
        quit()

###- Read the specified excel workbook and worksheet
title_block()
df = pd.read_excel(path_to_excel,sheet_name = sheet_name)
print(f"The tool is being run on the excel column with the header: '{excel_column_name}'.")
print(f"The tool is searching the Arc Pro field named: '{field_name}'.\n")
print('Here are the first 5 rows of the data frame being used.')
print(df.head(5))

###- Generate a list of query items
query_column_list = df[excel_column_name].tolist()
print('\n')

###- Generate a list of full query statement
query_list = []
counter = 0
for item in query_column_list:
    counter += 1
    if counter != len(query_column_list):
        query_list.append(field_name)
        query_list.append("= '" + item + "'")
        query_list.append('' + operator + '')
    else:
        query_list.append(field_name)
        query_list.append("= '" + item + "'")


###- Create SQL query string from the query_list
SQL_Query = ' '.join([str(item) for item in query_list])
print(f'The output SQL query string can be found below. This query should locate {len(query_column_list)} features.\n')
print(SQL_Query)
pyperclip.copy(SQL_Query)
print('\nThe SQL Query has been copied to your clipboard.\nPaste the output string into the SQL section of the "Select by Attributes" tool.\n')
 
