# ArcGIS SQL Query Generator from Excel

## Overview

The [SQL_Query_Generator.py](https://github.com/wessholders/portfolio/blob/main/python/Select%20by%20Attribute%20Query%20Generator/SQL_Query_Generator.py) Python script is a simple but powerful productivity tool for GIS analysts who work with the Esri ArcGIS suite. It automates the tedious process of creating long SQL `IN` clauses for use in tools like "Select By Attributes" or for creating definition queries.

In many GIS workflows, analysts receive a list of hundreds of specific features to select or display from a much larger dataset. This list is often provided as an Excel spreadsheet. Manually typing each value into a query is time-consuming and prone to errors. This script solves that problem by reading a specified column from an Excel file and instantly generating a perfectly formatted SQL query, which it then copies to the clipboard.

---

## The Workflow

The process is designed to be as simple as possible:

### 1. Prepare Your Excel File

Start with a simple Excel sheet containing a column with the unique identifiers you want to query.

![Excel Column Screenshot](https://github.com/wessholders/portfolio/blob/main/python/Select%20by%20Attribute%20Query%20Generator/screenshots/querySheet.png?raw=true)

### 2. Run the Script

Execute the Python script. It will interactively prompt you for the Excel file name, the name of the column containing your data, and the name of the GIS field you want to query against.

### 3. Paste the Query in ArcGIS

The script automatically copies the generated SQL query to your clipboard. Simply paste it into the SQL expression box in ArcGIS Pro's "Select By Attributes" tool or a layer's definition query editor.

![Pasted SQL Query Screenshot](https://github.com/wessholders/portfolio/blob/main/python/Select%20by%20Attribute%20Query%20Generator/screenshots/definitionQuerySQL.png?raw=true)

### 4. See the Result & Time Saved

After pasting, switching back to the "Clause" view in ArcGIS Pro shows how the tool has automatically built the query from your input. This demonstrates the immense amount of time saved compared to manually adding each value.

![Generated Query Clauses Screenshot](https://github.com/wessholders/portfolio/blob/main/python/Select%20by%20Attribute%20Query%20Generator/screenshots/definitionQuery.png?raw=true)

---

## Features

*   **Interactive Prompts:** Guides the user through the process of selecting their file and fields.
*   **Reads Excel Files:** Directly processes `.xlsx` files using the pandas library.
*   **Generates SQL `IN` Clause:** Creates a correctly formatted SQL `IN` clause, wrapping string values in single quotes.
*   **Copies to Clipboard:** Automatically copies the final query string to the clipboard for immediate use.
*   **Cross-Platform:** Runs on any system with a Python installation.

---

## Requirements

This script requires Python 3 and the following Python libraries:

*   `pandas`: For reading and processing the Excel file.
*   `openpyxl`: Required by pandas to work with `.xlsx` files.
*   `pyperclip`: For copying the query to the clipboard.

You can install these dependencies using pip:
```bash
pip install pandas openpyxl pyperclip
