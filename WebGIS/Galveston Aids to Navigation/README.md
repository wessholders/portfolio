# Galveston Bay - Aids to Navigation Viewer

## Overview

This project is an interactive web map designed to visualize marine Aids to Navigation (ATON) within the greater Galveston Bay complex. As my first complete Web GIS application, its primary goal was to serve as a learning exercise in several key areas:

*   **Custom Symbology:** Moving beyond default markers to create accurate, data-driven visualizations.
*   **Dynamic Styling:** Using data attributes to change the appearance and behavior of features on the fly.
*   **Live API Integration:** Fetching and displaying real-time information from external services.

The application displays various types of navigation markers, such as buoys and daybeacons, and overlays them with live tide and current data from NOAA, providing a comprehensive operational picture for mariners in the area.

### Live Demo

*(Link to your live application here)*

### Application Screenshot

![Galveston Bay Aids to Navigation Viewer](https://github.com/wessholders/portfolio/blob/main/WebGIS/Galveston%20Aids%20to%20Navigation/screenshots/HGACNavAids.png?raw=true)

---

## Features

*   **Dynamic & Accurate Symbology:** The application intelligently reads the attributes of each navigation aid from the GeoJSON data and renders a custom SVG symbol that accurately represents it. This includes:
    *   **Daybeacons:** Red triangles (TR) and green squares (SG).
    *   **Buoys:** Red "nun" buoys and green "can" buoys.
    *   **ICW Markers:** Special square and triangle symbols with yellow decals.
    *   **Range Markers:** Distinctive red and white `KRW` range markers.
*   **Animated Lights:** For lighted aids, the script parses the `characteristics` string (e.g., `Fl G 2.5s`) to create an animated light on the symbol that mimics the real-world aid's color, pattern (flashing, quick-flashing, occulting), and timing.
*   **Live NOAA Data Integration:**
    *   **Tide Predictions:** Displays markers for multiple NOAA tide stations. Clicking a marker reveals a popup with today's high and low tide predictions.
    *   **Real-time Currents:** Visualizes live current data from several NOAA stations using dynamic arrows. The **direction** of the arrow rotates to match the current's bearing, and its **length** changes to represent the current's speed.
*   **Interactive Map Controls:**
    *   A full layer control to toggle basemaps (Street, Dark, Satellite) and data overlays.
    *   A custom "Navigation Lights" toggle that turns the light animations on and off, simulating day/night viewing conditions.
*   **Informative Popups:** Clicking on any aid or station reveals a popup with its key attributes.

---

## How It Works

The core of this application's custom visualization lies within the `pointToLayer` function in the Leaflet GeoJSON options.

1.  **Data Loading:** The app fetches the `Aids_to_Navigation.geojson` file.
2.  **Symbol Rendering:** For each point feature, the `pointToLayer` function is executed:
    *   It uses regular expressions to parse the `structure` and `characteristics` properties.
    *   Based on the text found (e.g., "TR", "SG", "on pile"), it dynamically constructs an SVG string for the marker's shape and color.
    *   If light characteristics are present, it creates an additional SVG `<circle>` element and assigns it CSS variables for `--animation-name` and `--animation-duration`.
3.  **Light Animation:** Custom `@keyframes` in the `style.css` file define the different flash patterns (flash, quick-flash, occulting). The `light-anim` class on the SVG circle reads the CSS variables to apply the correct animation, creating a realistic lighting effect.
4.  **API Calls:** The app loops through predefined lists of NOAA station IDs for tides and currents, making asynchronous `fetch` calls to the NOAA Tides and Currents API for each one and adding the returned data to the map.
5.  **Layer Toggling:** The "Navigation Lights" toggle adds or removes a `.lights-off` class to the main map `div`. A corresponding CSS rule (`.lights-off .light-anim`) disables the animations and sets the opacity to 0, effectively turning the lights "off".

---

## Core Technologies & Data Sources

*   **Mapping Library:** [Leaflet.js](https://leafletjs.com/)
*   **Frontend:** Vanilla JavaScript (ES6), HTML5, CSS3
*   **Basemaps:** OpenStreetMap, Carto, Esri World Imagery
*   **Data Sources:**
    *   **Aids to Navigation:** Local `Aids_to_Navigation.geojson` file.
    *   **Tides & Currents:** [NOAA Tides and Currents API](https://api.tidesandcurrents.noaa.gov/api/prod/)

---

## Local Setup

To run this project locally:

1.  Clone or download the repository.
2.  Ensure the `index.html`, `style.css`, `script_v2.js`, and the `Data` folder containing the GeoJSON are in the same root directory.
3.  Open the `index.html` file in any modern web browser.
