# GeoJSON & Excel Conversion Utilities

## Overview

This repository contains two simple Python scripts designed to facilitate a common GIS data workflow: converting geographic data between Microsoft Excel (`.xlsx`) and GeoJSON (`.geojson`) formats.

These scripts are ideal for users who manage spatial data in spreadsheets but need to use it in web mapping applications (which often require GeoJSON) or, conversely, need to export GeoJSON data into a spreadsheet for easier bulk editing.

---

## Scripts

1.  **[`excel_to_geojson.py`](https://github.com/wessholders/portfolio/blob/main/python/excel%20and%20GEOJSON%20Integration/excel_to_geojson.py)**
    *   **Purpose:** Converts an Excel file with latitude and longitude columns into a valid GeoJSON file of Point features.
    *   **Use Case:** Preparing spreadsheet data for use in web maps (e.g., Leaflet, Mapbox, Esri ArcGIS Online).

2.  **[`geojson_to_excel.py`](https://github.com/wessholders/portfolio/blob/main/python/excel%20and%20GEOJSON%20Integration/geojson_to_excel.py)**
    *   **Purpose:** Converts a GeoJSON file into an Excel spreadsheet. It extracts all feature properties and adds the latitude and longitude as separate columns.
    *   **Use Case:** Exporting data from a web map or GIS application for easy review, bulk editing, or analysis in Excel.

---

## Requirements

These scripts require Python 3 and the following Python libraries:

*   `pandas`
*   `openpyxl`

You can install these dependencies using pip:

```bash
pip install pandas openpyxl
