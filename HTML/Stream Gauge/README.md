# NOAA Streamgauge Water Level Chart

## Overview

This HTML file provides a self-contained, embeddable widget that displays a detailed 24-hour water level chart for a specific NOAA streamgauge. It fetches real-time data directly from the NOAA Water API and renders a clean, responsive line chart using Chart.js.

While map-based platforms provide an excellent overview of gauge locations, this widget is designed for a **detailed, historical deep-dive on a single gauge**.

### Example Widget

![Addicks Stream Gauge Widget Screenshot](https://github.com/wessholders/portfolio/blob/main/HTML/Stream%20Gauge/screenshots/addicksStreamGaugeWidget.png?raw=true)

---

## Esri Living Atlas & Dashboard Integration

This widget is an ideal companion to the **USA Live Stream Gauges layer** found in the **Esri Living Atlas of the World**.

You can use an Esri map to visualize the location and status of all gauges, and then use this widget to embed a detailed 24-hour chart for a specific gauge of interest directly into an **Esri Dashboard** or **Experience Builder** application.

This allows users to go from a macro, geographic view to a micro, time-series analysis without leaving the application.

---

## Features

*   **Real-time Data:** Fetches the latest streamgauge data directly from the NOAA API.
*   **24-Hour View:** Filters and displays only the data from the last 24 hours.
*   **Dynamically Resizable:** The chart is fully responsive and automatically resizes to fit its container, making it ideal for various dashboard layouts and screen sizes.
*   **Current Level Indicator:** A **red, dashed horizontal line** indicates the current (most recent) water level for at-a-glance status checks.
*   **Data Thinning:** Reduces data density to ensure a smooth, clean line graph.
*   **Dynamic Y-Axis:** The vertical axis automatically scales based on the 24-hour water levels.
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
2.  **Data Processing:** The JSON response is parsed, and the data is filtered to include only valid readings from the past 24 hours.
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

---

## Usage & Embedding

### Standalone

Simply open the `.html` file in any modern web browser to view the chart.

### Embedding in a Dashboard or Experience

This file is designed to be embedded into other web pages or platforms using an `<iframe>`. This is the method used to add it to Esri Dashboards (via the *Embedded Content* element) or Esri Experience Builder (via the *Embed* widget).

```html
<iframe src="/path/to/your/file.html" width="100%" height="300px" style="border:none;"></iframe>
