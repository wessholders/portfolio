# Smartsheet & Esri ArcGIS Feature Layer Synchronization

## Overview

This project provides a set of two Python scripts for bidirectional data synchronization between a Smartsheet grid and an Esri ArcGIS Feature Layer. This enables a powerful workflow where non-GIS users can manage data in a familiar Smartsheet interface, with their changes reflected in a geospatial web layer, and vice-versa.

This is ideal for collaborative projects where field crews, project managers, and GIS analysts need to work from a single, unified dataset.

---

## Scripts

1.  **[`GIS_to_SS.py`](https://github.com/wessholders/portfolio/blob/main/python/Smartsheet%20and%20GIS%20Integration/GIS_to_SS.py)**
    *   **Direction:** Esri ArcGIS → Smartsheet
    *   **Purpose:** Reads all features from a specified ArcGIS Feature Layer and updates or adds corresponding rows in a target Smartsheet grid.

2.  **[`SS_to_GIS.py`](https://github.com/wessholders/portfolio/blob/main/python/Smartsheet%20and%20GIS%20Integration/SS_to_GIS.py)**
    *   **Direction:** Smartsheet → Esri ArcGIS
    *   **Purpose:** Reads all rows from a specified Smartsheet grid and updates or adds corresponding features in a target ArcGIS Feature Layer.

---

## How It Works

The synchronization is based on a **unique identifier** that must exist in both systems to link records.

*   The `GIS_to_SS.py` script uses the `GlobalID` field from the Esri feature to populate a `GlobalID` column in Smartsheet.
*   The `SS_to_GIS.py` script uses the Smartsheet row `id` to populate a `Smartsheet_ID` field in the Esri feature layer.

When a script is run, it fetches all records from the source system and iterates through them. For each record, it checks if a corresponding record exists in the target system based on the unique ID.

*   If a match is found, the attributes/cell values are **updated**.
*   If no match is found, a new feature/row is **added**.

---

## Requirements

### Python Libraries

These scripts require Python 3 and the following Python libraries:

*   `smartsheet-python-sdk`: To interact with the Smartsheet API.
*   `arcgis`: The Esri ArcGIS API for Python to interact with Feature Layers.

You can install these dependencies using pip:
```bash
pip install smartsheet-python-sdk arcgis
```

### System & Account Setup

1.  **Smartsheet API Token:**
    *   You must have a Smartsheet API Access Token.
    *   This token should be set as an environment variable named `SMARTSHEET_ACCESS_TOKEN`.

2.  **ArcGIS Online/Portal Account:**
    *   You need credentials for an ArcGIS Online or ArcGIS Enterprise portal account that has permission to edit the target feature layer.

3.  **Data Schema:**
    *   **Smartsheet:** Create a column named `GlobalID` (Text/Number type) to store the unique ID from Esri.
    *   **ArcGIS Feature Layer:** Create a field named `Smartsheet_ID` (Integer type) to store the unique row ID from Smartsheet.
    *   Ensure all other columns/fields you wish to sync have matching names and compatible data types between both systems.

---

## Configuration & Usage

Before running, you must configure the variables inside each script.

### 1. GIS to Smartsheet (`GIS_to_SS.py`)

1.  Open the `GIS_to_SS.py` file in a text editor.
2.  Update the `ARCGIS PORTAL`, `USERNAME`, and `PASSWORD` variables with your Esri account credentials.
3.  Set the `SHEET_ID` variable to the ID of your target Smartsheet.
4.  Set the `FEATURE_LAYER_URL` variable to the URL of the source Esri Feature Layer.
5.  Run the script from your terminal:
    ```bash
    python GIS_to_SS.py
    ```

### 2. Smartsheet to GIS (`SS_to_GIS.py`)

1.  Open the `SS_to_GIS.py` file in a text editor.
2.  Update the `ARCGIS PORTAL`, `USERNAME`, and `PASSWORD` variables with your Esri account credentials.
3.  Set the `SHEET_ID` variable to the ID of your source Smartsheet.
4.  Set the `FEATURE_LAYER_URL` variable to the URL of the target Esri Feature Layer.
5.  Run the script from your terminal:
    ```bash
    python SS_to_GIS.py
    ```

**Note:** These scripts can be scheduled to run at regular intervals using tools like Windows Task Scheduler or cron (on Linux/macOS) to achieve automated, near real-time synchronization.

