// --- STEP 1: DEFINE YOUR BASEMAP CHOICES ---

// Main OpenStreetMap layer (the one you already had)
const street = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
});

// A "dark mode" basemap
const dark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19
});

// A satellite/imagery basemap
const satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
});


// --- INITIALIZE THE MAP ---

// Initialize the map and set it to display the 'street' layer by default
const map = L.map('map', {
    center: [29.35, -94.9], // Adjust to your data's center
    zoom: 12, // Adjust zoom level
    layers: [satellite] // This sets the default layer
});


// --- ADD YOUR GEOJSON DATA, DEFINE OVERLAYS, AND CREATE THE CONTROL ---

// 1. Create the layer group that will hold your marker symbols.
const waterMain = L.layerGroup().addTo(map);

// This will hold our new tide station marker(s)
const tideStationsLayer = L.layerGroup().addTo(map);

// 2. Fetch the data and add it to the 'waterMain' group.
fetch('Data/Aids_to_Navigation.geojson')
    .then(response => response.json())
    .then(data => {
        L.geoJSON(data, {
            // Your entire pointToLayer function goes here.
            // This function is correct from our previous steps, so no changes needed inside it.
            pointToLayer: function (feature, latlng) {
                const structureType = feature.properties.structure || '';
                const lightChars = feature.properties.characteristics || '';

                const isTR = /\bTR\b/i;
                const isSG = /\bSG\b/i;
                const isRangeMarker = /\bKRW\b/i;
                const isOnPile = /on pile/i;
                const isGreenICW = /-SY\b/i;
                const isRedICW = /-TY\b/i;
                const isNunBuoy = /\b(nun|Red(?!-TY|\s*nun))\b/i;
                const isCanBuoy = /\b(can|Green(?!-SY|\s*can))\b/i;

                let backgroundHtml = '';
                let foregroundHtml = '';
                let lightHtml = '';
                let animationStyle = '';

                if (lightChars) {
                    let match = lightChars.match(/([a-zA-Z\s\(\)0-9\+]+)\.?\s([A-Z])\s(\d+\.?\d*s)/);
                    if (!match) { match = lightChars.match(/([a-zA-Z]+)\s([A-Z])$/); }
                    if (match) {
                        const pattern = match[1] || '';
                        const colorCode = match[2] || 'W';
                        const period = match[3] || '1s';

                        let lightColor = '#FFFFFF';
                        if (colorCode === 'R') lightColor = '#FF0000';
                        if (colorCode === 'G') lightColor = '#00FF00';
                        if (colorCode === 'Y') lightColor = '#DAA520';

                        let animationName = 'flash';
                        if (pattern.toUpperCase().startsWith('Q')) animationName = 'quick-flash';
                        if (pattern.toUpperCase().startsWith('ISO')) animationName = 'flash';
                        if (pattern.toUpperCase().startsWith('OCC')) animationName = 'occulting';

                        lightHtml = `<circle cx="12" cy="5" r="3" fill="${lightColor}" class="light-anim light-glow" style="--animation-name: ${animationName}; --animation-duration: ${period};" />`;
                    }
                }

                if (isOnPile.test(structureType)) {
                    let pileX;
                    const pileWidth = 2;
                    if (isRangeMarker.test(structureType)) {
                        pileX = 8;
                    } else {
                        pileX = 11;
                    }
                    backgroundHtml = `<rect x="${pileX}" y="12" width="${pileWidth}" height="20" fill="#000000" />`;
                }

                if (isRedICW.test(structureType)) {
                    foregroundHtml = `<path d="M12 2 L2 22 L22 22 Z" fill="#FF0000" stroke="#000" stroke-width="1" /><path d="M12 8 L7 17 L17 17 Z" fill="#DAA520" />`;
                } else if (isGreenICW.test(structureType)) {
                    foregroundHtml = `<rect x="2" y="2" width="20" height="20" fill="#00ff00" stroke="#000" stroke-width="1" /><rect x="7" y="7" width="10" height="10" fill="#DAA520" />`;
                } else if (isRangeMarker.test(structureType)) {
                    foregroundHtml = `<rect x="0" y="0" width="6" height="24" fill="#FF0000" stroke="#000" stroke-width="1"/><rect x="6" y="0" width="6" height="24" fill="#FFFFFF" stroke="#000" stroke-width="1"/><rect x="12" y="0" width="6" height="24" fill="#FF0000" stroke="#000" stroke-width="1"/>`;
                } else if (isTR.test(structureType)) {
                    foregroundHtml = `<path d="M12 2 L2 22 L22 22 Z" fill="#FF0000" stroke="#000" stroke-width="1" />`;
                } else if (isSG.test(structureType)) {
                    foregroundHtml = `<rect x="2" y="2" width="20" height="20" fill="#00ff00" stroke="#000" stroke-width="1" />`;
                } else if (isNunBuoy.test(structureType)) {
                    foregroundHtml = `<path d="M12 5 L5 15 L19 15 Z" fill="#FF0000" stroke="#000" stroke-width="1" />`;
                } else if (isCanBuoy.test(structureType)) {
                    foregroundHtml = `<rect x="6" y="6" width="12" height="12" fill="#00ff00" stroke="#000" stroke-width="1" />`;
                } else {
                    foregroundHtml = `<circle cx="12" cy="12" r="10" fill="#808080" stroke="#000" stroke-width="1" />`;
                }

                const finalSvg = `<svg viewBox="0 0 24 32">${backgroundHtml}${foregroundHtml}${lightHtml}</svg>`;

                const iconAnchor = isOnPile.test(structureType) ? [10, 26] : [10, 14];
                const customIcon = L.divIcon({
                    html: finalSvg,
                    className: 'custom-marker',
                    iconSize: [20, 28],
                    iconAnchor: iconAnchor
                });

                return L.marker(latlng, { icon: customIcon });
            },

            // Your onEachFeature function is also correct and included here.
            onEachFeature: function (feature, layer) {
                if (feature.properties) {
                    let popupContent = `<strong>Structure Type:</strong> ${feature.properties.structure}`;
                    if (feature.properties.aidname) {
                        popupContent += `<br><strong>Aid Name:</strong> ${feature.properties.aidname}`;
                    }
                    layer.bindPopup(popupContent);
                }
            }
        }).addTo(waterMain);
    })
    .catch(error => console.error('Error loading the GeoJSON file:', error));

// --- ADD MULTIPLE NOAA TIDE STATIONS ---

// STEP 1: Create a list of the station IDs you want to display.
// You can find more IDs from the NOAA website.
const tideStationIds = [
    '8771450', // Galveston Pier 21
    '8771486', // Galveston Railroad Bridge, TX
    '8771341',  // Galveston Bay Entrance, North Jetty, TX
    '8771013',  // Eagle Point, Galveston Bay, TX
    '8771972',  // San Luis Pass, TX
    '8770613',  // Morgans Point, Barbours Cut, TX
    '8770971',   // Rollover
    '8770613',   // Barbours Cut
    '8770808'   // High Island
];

// STEP 2: Create a reusable function to add ONE tide station.
// This function takes a stationId as its input.
function addTideStation(stationId) {
    // Use template literals (the backticks ``) to easily insert the stationId variable into the URL.
    const metadataUrl = `https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/${stationId}.json?units=english`;
    const predictionsUrl = `https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=today&station=${stationId}&product=predictions&datum=STND&time_zone=lst&interval=hilo&units=english&format=json`;

    // Fetch the metadata first
    fetch(metadataUrl)
        .then(response => response.json())
        .then(metaData => {
            const stationInfo = metaData.stations[0];
            const stationName = stationInfo.name;
            const lat = parseFloat(stationInfo.lat);
            const lon = parseFloat(stationInfo.lng);

            // Now, fetch the predictions for the same station
            return fetch(predictionsUrl)
                .then(response => response.json())
                .then(predictionData => {
                    // Combine all the data into a single object
                    return { stationName, lat, lon, predictionData };
                });
        })
        .then(({ stationName, lat, lon, predictionData }) => {
            if (predictionData.error) {
                console.error(`Error from NOAA Predictions API for station ${stationId}:`, predictionData.error.message);
                predictionData.predictions = [];
            }

            let popupContent = `<strong>${stationName}</strong><br><hr>`;
            if (predictionData.predictions && predictionData.predictions.length > 0) {
                predictionData.predictions.forEach(prediction => {
                    popupContent += `Time: ${prediction.t}, Value: ${prediction.v} ft (${prediction.type})<br>`;
                });
            } else {
                popupContent += "No tide predictions available for today.";
            }

            const tideIconSvg = `
                <svg viewBox="0 0 24 24" width="18px" height="18px">
                    <path d="M12 0 L22 12 L12 24 L2 12 Z" fill="#0077c8" stroke="#000" stroke-width="1.5" />
                </svg>
            `;
            const customTideIcon = L.divIcon({
                html: tideIconSvg,
                className: 'custom-marker',
                iconSize: [20, 20],
                iconAnchor: [10, 10]
            });

            const tideMarker = L.marker([lat, lon], { icon: customTideIcon });
            tideMarker.bindPopup(popupContent);
            tideMarker.addTo(tideStationsLayer);
        })
        .catch(error => {
            console.error(`Error fetching data for station ${stationId}:`, error);
        });
}

// STEP 3: Loop through your list of IDs and call the function for each one.
tideStationIds.forEach(addTideStation);

// --- ADD MULTIPLE NOAA CURRENT STATIONS ---

// 1. Create a new layer group just for the current stations.
const currentsLayer = L.layerGroup().addTo(map);

// 2. Create the list of current station IDs you provided.
const currentStationIds = [
    'g09010',
    'g11010',
    'g06010',
    'g08010',
    'g10010'
];

// 3. Create a reusable function to add ONE current station.
function addCurrentStation(stationId) {
    // --- UPDATED URL ---
    const dataUrl = `https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=latest&station=${stationId}&product=currents&time_zone=lst&units=english&application=HGAC_Markers&format=json`;

    fetch(dataUrl)
        .then(response => response.json())
        .then(data => {
            if (data.error || !data.metadata || !data.data || data.data.length === 0) {
                console.error(`Error or no data for current station ${stationId}:`, data.error ? data.error.message : "No data found");
                return;
            }

            const stationName = data.metadata.name;
            const lat = parseFloat(data.metadata.lat);
            const lon = parseFloat(data.metadata.lon);
            const latestReading = data.data[0];

            const speed = parseFloat(latestReading.s);
            const direction = parseInt(latestReading.d);

            // --- 1. Symbol Logic: Determine arrow LENGTH based on speed ---
            // Base length for the arrow shaft
            const baseLength = 2;
            // Exaggeration factor: multiply the speed by this to get the added length.
            // Increase this number for more dramatic length changes.
            const exaggerationFactor = 100;

            let shaftHeight = baseLength + (speed * exaggerationFactor);
            // Cap the max height to prevent ridiculously long arrows for very strong currents
            if (shaftHeight > 60) {
                shaftHeight = 60;
            }

            // --- 2. Build the Dynamic SVG with a separate shaft and head ---
            const arrowSvg = `
                <svg viewBox="0 0 24 24" width="28px" height="28px">
                    <!-- The Arrowhead: Always stays in the same place at the top -->
                    <path d="M12 0 L18 8 L6 8 Z" fill="#9400D3" />
                    
                    <!-- The Shaft: A rectangle whose height is dynamic -->
                    <rect x="9" y="8" width="6" height="${shaftHeight}" fill="#9400D3" />
                </svg>
            `;

            // --- 3. Create the Custom Icon with Rotation ---
            const customCurrentIcon = L.divIcon({
                html: `<div style="transform-origin: center; transform: rotate(${direction}deg);">${arrowSvg}</div>`,
                className: 'custom-marker',
                iconSize: [32, 32], // A consistent container size
                iconAnchor: [16, 16] // Keep it centered
            });

            // --- 4. Build the Pop-up Content (Unchanged) ---
            let popupContent = `<strong>${stationName} (Currents)</strong><br><hr>`;
            popupContent += `Time: ${latestReading.t}<br>`;
            popupContent += `Speed: ${speed.toFixed(2)} kts<br>`;
            popupContent += `Direction: ${direction}°`;

            // --- 5. Create and Add the Marker (Unchanged) ---
            const currentMarker = L.marker([lat, lon], { icon: customCurrentIcon });
            currentMarker.bindPopup(popupContent);
            currentMarker.addTo(currentsLayer);
        })
        .catch(error => {
            console.error(`Network error fetching data for current station ${stationId}:`, error);
        });
}




// 4. Loop through your list of IDs and call the function for each one.
currentStationIds.forEach(addCurrentStation);






// 3. Create an object for our basemaps
const baseMaps = {
    "Street View": street,
    "Dark Mode": dark,
    "Satellite": satellite
};

// 4. Create the dummy layer for the lights toggle
const lightsLayer = L.layerGroup().addTo(map);

// 5. Create the object for our overlays, now including the correctly defined waterMain
const overlayMaps = {
    "Navigation Lights": lightsLayer,
    "Marker Symbols": waterMain, // This will now work correctly
    "Tide Stations": tideStationsLayer, // Add this new line
    "Current Stations": currentsLayer // Add this new line
};

// 6. Add the layer control to the map
const layerControl = L.control.layers(baseMaps, overlayMaps).addTo(map);

// 7. Add the event listeners for the lights toggle
map.on('overlayadd', function (e) {
    if (e.layer === lightsLayer) {
        L.DomUtil.removeClass(map.getContainer(), 'lights-off');
    }
});
map.on('overlayremove', function (e) {
    if (e.layer === lightsLayer) {
        L.DomUtil.addClass(map.getContainer(), 'lights-off');
    }
});

