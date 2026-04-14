# NOAA Streamgauge Water Level Chart

## Overview

This HTML file provides a self-contained, embeddable widget that displays a 24-hour water level chart for a specific NOAA streamgauge. It fetches real-time data from the NOAA Water API, processes it, and renders a clean, responsive line chart using Chart.js.

The chart is designed to be easily embedded into dashboards or other web pages using an `<iframe>`.

---

## Features

*   **Real-time Data:** Fetches the latest streamgauge data directly from the NOAA API.
*   **24-Hour View:** Filters and displays only the data from the last 24 hours.
*   **Responsive Chart:** The chart automatically resizes to fit its container, making it suitable for various dashboard layouts.
*   **Data Thinning:** Reduces the number of data points to ensure a smooth, clean line graph without sacrificing accuracy.
*   **Dynamic Y-Axis:** The vertical axis automatically scales based on the water levels in the 24-hour period.
*   **Latest Reading Annotation:** A dashed horizontal line clearly marks the most recent water level reading.
*   **Timezone Aware:** All times are displayed in the `America/Chicago` timezone.
*   **Interactive Tooltips:** Hovering over the chart reveals tooltips with the precise date, time, and water level.

---

## Dependencies

This widget relies on three external JavaScript libraries delivered via a Content Delivery Network (CDN). No local installation is required.

| Library | Purpose |
| :--- | :--- |
| **Chart.js** | The core library for creating the chart. |
| **chartjs-adapter-date-fns** | Enables Chart.js to correctly interpret and display date/time values. |
| **chartjs-plugin-annotation**| Used to draw the horizontal line and label for the latest water level. |

---

## How it Works

1.  **Data Fetching:** On page load, a `fetch` request is sent to the NOAA NWPS API for the specified gauge.
2.  **Data Processing:** The JSON response is parsed, and the data is filtered to include only valid readings from the past 24 hours. A thinning algorithm is applied to reduce data density for a cleaner visual.
3.  **Chart Rendering:** The processed data is passed to Chart.js, which renders a responsive line chart on the HTML `<canvas>` element.

---

## Configuration

### Adjusting the Streamgauge

This widget can be used for **any NOAA streamgauge** that has stage/flow data available via the NWPS v1 API. To change the gauge:

1.  Open the HTML file in a text editor.
2.  Locate the following line in the `<script>` section:
    ```javascript
    const url = 'https://api.water.noaa.gov/nwps/v1/gauges/ADDT2/stageflow';
    ```
3.  Replace `ADDT2` with the desired NOAA gauge ID (e.g., `LBUT2`, `CHII2`, etc.).

### Adjusting Data Thinning

To change the minimum time between data points on the chart, modify the `MINIMUM_INTERVAL_MINUTES` constant:

```javascript
const MINIMUM_INTERVAL_MINUTES = 15; // Set to 0 to disable thinning
