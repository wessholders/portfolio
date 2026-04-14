# Galveston Bay Boat Ramp Finder

## Overview

The Galveston Bay Boat Ramp Finder is an interactive, mobile-friendly WebGIS application designed to help boaters in the Galveston, TX area choose the most suitable boat ramp for their needs at any given moment.

This application provides a real-time, map-centric view of boat ramp locations and combines it with live weather and tide data to give users a comprehensive operational picture. By clicking on a ramp, users can view detailed information, including ramp characteristics, fees, and photos, all within a single interface.

### Live Demo

**(Link to your live application here)**

### Application Screenshot

![Application Screenshot](https://github.com/wessholders/portfolio/blob/main/WebGIS/Boat%20Ramp%20Viewer/screenshots/gavestonBoatRamps.png?raw=true)

---

## Features

*   **Interactive Map:** A fast, responsive map built with Leaflet.js, featuring both satellite and street basemap options.
*   **Live Weather Data:** A dedicated panel displays the current temperature, wind speed/direction, humidity, and a short-term forecast, fetched directly from the National Weather Service (NWS) API.
*   **Live Tide & Water Data:**
    *   A tide widget in the header shows the day's high and low tides, with the next upcoming tide highlighted for quick reference.
    *   The current water temperature is displayed in the weather panel.
    *   All data is sourced from the NOAA Tides and Currents API.
*   **Detailed Ramp Information:** A slide-out sidebar provides comprehensive details for each boat ramp, including:
    *   Ramp Name & Access Type (e.g., Public, Private)
    *   Number of Lanes
    *   Launch Fees
    *   Recommended Vessel Size
    *   Minimum Tide requirements for usability
    *   Important operational notes
*   **Image Gallery:** View multiple photos of each boat ramp in a thumbnail gallery within the sidebar.
*   **Fullscreen Image Lightbox:** Click on any image to view it in a fullscreen, interactive carousel with next/previous controls.
*   **Responsive Design:** The interface is optimized for both desktop and mobile devices.

---

## How It Works

1.  **Map Initialization:** The application initializes a Leaflet map centered on the Galveston Bay area.
2.  **Data Loading:** It asynchronously fetches GeoJSON data (`boat_ramps.geojson`) containing the locations and attributes of all the boat ramps. These are then rendered as clickable points on the map.
3.  **API Calls:** On load, the application makes several API calls:
    *   It queries the **NWS API** for the specified coordinates to get the latest hourly weather forecast.
    *   It queries the **NOAA Tides and Currents API** using a station ID (`8771450` for Galveston Bay) to get tide predictions and the latest water temperature.
4.  **User Interaction:**
    *   When a user clicks on a map point, the sidebar slides into view.
    *   The sidebar is dynamically populated with the properties from the selected ramp's GeoJSON data, including its image URLs.
    *   Clicking an image in the sidebar opens a fullscreen lightbox carousel for easier viewing.
    *   Hovering over a tide "pill" in the header reveals the exact tide height in feet.

---

## Core Technologies & Data Sources

*   **Frontend Library:** Vanilla JavaScript (ES6)
*   **Mapping Library:** [Leaflet.js](https://leafletjs.com/)
*   **Basemaps:** Esri World Imagery & OpenStreetMap
*   **Styling:** Custom CSS3
*   **Data Sources:**
    *   **Boat Ramps:** Local `boat_ramps.geojson` file
    *   **Weather:** [National Weather Service (NWS) API](https://www.weather.gov/documentation/services-web-api)
    *   **Tides & Water Temperature:** [NOAA Tides and Currents API](https://api.tidesandcurrents.noaa.gov/api/prod/)

---

## Project Structure

The project consists of the following core files:

*   **index.html:** The main HTML structure of the application.
*   **script.js:** Contains all core application logic, map functions, and API calls.
*   **style.css:** All custom styling for the application interface.
*   **boat_ramps.geojson:** The GeoJSON data file for boat ramp locations and attributes.

---

## Local Setup & Usage

To run this project locally, you do not need a web server.

1.  Clone or download the repository to your local machine.
2.  Ensure all files (`index.html`, `script.js`, `style.css`, `boat_ramps.geojson`) are in the same directory.
3.  Open the `index.html` file in any modern web browser (like Chrome, Firefox, or Edge).

The application will load, and the map and data widgets should populate automatically.

