# Esri ArcGIS Online Credit Usage Report Generator

## Overview

This Python script automates the generation of a detailed, organization-wide credit usage report for an Esri ArcGIS Online portal. It is designed for administrators who need to monitor, track, and report on the total credit consumption of their entire organization for a specific month.

This process, which can take hours to perform manually through the web interface, is **completed in seconds** with this script. This automation saves valuable administrator time and resources by providing a quick, consolidated view of the organization's spending.

The script connects to your ArcGIS Online organization, fetches the credit usage data for a specified time frame, and exports the results into an Excel file (`.xlsx`).

---

## Sample Report Output

The script generates an Excel file summarizing the entire organization's credit usage, with a breakdown by service type (e.g., Geocoding, Service Hosting, Analytics).

![Sample Credit Usage Report](https://github.com/wessholders/portfolio/blob/main/python/Esri%20Credit%20Usage%20Report%20Generator/screenshots/creditUsage.png?raw=true)

---

## Features

*   **Massive Time Savings:** Reduces a manual reporting task that can take hours of clicking and data compilation down to a script that runs in mere seconds.
*   **Organization-Wide Reporting:** Generates a single, consolidated report for the entire ArcGIS Online organization.
*   **Monthly Granularity:** Fetches and processes data for any specified month and year.
*   **Breakdown by Service:** The report details credit consumption by specific service types.
*   **Excel Export:** Outputs the final report to a well-formatted `.xlsx` file for easy analysis and distribution.
*   **Secure Connection:** Uses the ArcGIS API for Python for secure authentication to your ArcGIS Online organization.

---

## Requirements

### Python Libraries

These scripts require Python 3 and the following libraries:

*   `arcgis`: The Esri ArcGIS API for Python to interact with your organization.
*   `pandas`: For data manipulation and aggregation.

You can install these dependencies using pip:
```bash
pip install arcgis pandas


```

### ArcGIS Online Account

*   You must have credentials for an ArcGIS Online account that has **administrator privileges** in order to access the credit usage reports.

---

## Configuration & Usage

Before running the script, you must update the configuration variables within the file.

1.  Open the [esriCreditUsageReport.py](https://github.com/wessholders/portfolio/blob/main/python/Esri%20Credit%20Usage%20Report%20Generator/esriCreditUsageReport.py) file in a text editor.
2.  Locate the configuration section at the top of the script.
3.  Update the following variables:
    *   `portal_url`: The URL to your ArcGIS Online organization (e.g., `"https://yourorg.maps.arcgis.com"`).
    *   `username`: Your ArcGIS Online administrator username.
    *   `password`: Your ArcGIS Online password.
    *   `year`: The year for the report you want to generate (e.g., `2024`).
    *   `month`: The month number for the report (e.g., `4` for April).
4.  Save the `esriCreditUsageReport.py` file.
5.  Open your terminal or command prompt and navigate to the directory containing the script.
6.  Run the script:
    ```bash
    python esriCreditUsageReport.py
    ```
7.  Upon successful execution, a file named `credit_usage_YYYY-MM.xlsx` (e.g., `credit_usage_2024-04.xlsx`) will be created in the same directory.

**Security Note:** For enhanced security, consider using environment variables or other secure methods to handle your username and password instead of hardcoding them directly in the script, especially in a production environment.
