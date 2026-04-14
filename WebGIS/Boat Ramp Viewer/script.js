/* =============================================================================
   SCRIPT.JS (FINAL VERSION WITH LIGHTBOX CAROUSEL)
   ============================================================================= */

document.addEventListener('DOMContentLoaded', function () {

    // --- MAP SETUP (UNCHANGED) ---
    var satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { attribution: 'Tiles © Esri' });
    var streets = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; OpenStreetMap contributors' });
    var map = L.map('map', { center: [29.25, -94.99], zoom: 11, layers: [satellite], zoomControl: false });
    var baseMaps = { "Satellite": satellite, "Streets": streets };
    L.control.layers(baseMaps).addTo(map);
    L.control.zoom({ position: 'bottomright' }).addTo(map);

    // --- SIDEBAR & LIGHTBOX ELEMENTS ---
    const infoSidebar = document.getElementById('info-sidebar');
    const sidebarContent = document.getElementById('sidebar-content');
    const closeSidebarBtn = document.getElementById('close-sidebar-btn');

    // Lightbox elements
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = lightbox.querySelector('img');
    const lightboxPrevBtn = document.getElementById('lightbox-prev');
    const lightboxNextBtn = document.getElementById('lightbox-next');
    const lightboxCloseBtn = document.getElementById('lightbox-close');

    // --- NEW: Global variables for the carousel ---
    let currentGalleryUrls = [];
    let currentImageIndex = 0;

    // --- NEW: Lightbox Carousel Functions ---
    function showLightbox(imageUrls, startIndex) {
        currentGalleryUrls = imageUrls;
        currentImageIndex = startIndex;
        lightboxImg.src = currentGalleryUrls[currentImageIndex];
        lightbox.classList.add('show');
    }

    function hideLightbox() {
        lightbox.classList.remove('show');
    }

    function showNextImage() {
        currentImageIndex = (currentImageIndex + 1) % currentGalleryUrls.length;
        lightboxImg.src = currentGalleryUrls[currentImageIndex];
    }

    function showPreviousImage() {
        currentImageIndex = (currentImageIndex - 1 + currentGalleryUrls.length) % currentGalleryUrls.length;
        lightboxImg.src = currentGalleryUrls[currentImageIndex];
    }

    // --- Event Listeners ---
    function closeSidebar() { document.body.classList.remove('sidebar-active'); }
    closeSidebarBtn.addEventListener('click', closeSidebar);
    map.on('click', () => { closeSidebar(); hideLightbox(); });

    // Lightbox Listeners
    lightbox.addEventListener('click', hideLightbox);
    lightboxCloseBtn.addEventListener('click', hideLightbox);
    lightboxNextBtn.addEventListener('click', (e) => { e.stopPropagation(); showNextImage(); });
    lightboxPrevBtn.addEventListener('click', (e) => { e.stopPropagation(); showPreviousImage(); });
    lightboxImg.addEventListener('click', (e) => e.stopPropagation()); // Prevent closing when clicking the image itself

    // --- GEOJSON & FEATURE INTERACTION ---
    function onEachFeature(feature, layer) {
        layer.bindPopup(`<b>${feature.properties.name}</b>`);
        layer.on('click', function (e) {
            L.DomEvent.stopPropagation(e);
            map.flyTo(e.latlng, 15);

            const props = feature.properties;
            let mainImageUrl = 'https://via.placeholder.com/350x200.png?text=No+Image';
            let galleryHTML = '';
            let imageGalleryUrls = []; // To store urls for the current feature

            if (props.image_url && Array.isArray(props.image_url) && props.image_url.length > 0) {
                imageGalleryUrls = props.image_url;
                mainImageUrl = imageGalleryUrls[0];

                imageGalleryUrls.forEach((url, index) => {
                    galleryHTML += `<div class="gallery-thumbnail" data-index="${index}"><img src="${url}" alt="Thumbnail"></div>`;
                });
            }

            // ... (rest of your HTML building for fee, notes, etc.)
            let feeText = "Free";
            if (props.fee && props.fee > 0) { feeText = `$${props.fee.toFixed(2)}`; }
            let newSidebarHTML = `
                <div class="sidebar-image-container" data-index="0">
                    <img src="${mainImageUrl}" alt="${props.name}">
                </div>
                ${galleryHTML ? `<div class="sidebar-gallery">${galleryHTML}</div>` : ''}
                <div class="sidebar-text-content">
                    <h2 class="sidebar-title">${props.name}</h2>
                    <p class="sidebar-access">${props.access || 'N/A'}</p>
                    <div class="sidebar-details-grid">
                        <div class="detail-item"><strong>Lanes</strong><span>${props.lanes || 'N/A'}</span></div>
                        <div class="detail-item"><strong>Launch Fee</strong><span>${feeText}</span></div>
                        <div class="detail-item"><strong>Vessel Size</strong><span>${props.vessel_size || 'N/A'}</span></div>
                        <div class="detail-item"><strong>Minimum Tide</strong><span>${props.minimum_tide || 'N/A'}</span></div>
                    </div>
                    ${props.notes ? `<div class="sidebar-notes"><h3>Notes</h3><p>${props.notes}</p></div>` : ''}
                </div>
            `;

            sidebarContent.innerHTML = newSidebarHTML;
            document.body.classList.add('sidebar-active');

            // --- MODIFIED: Attach click listeners to open the lightbox carousel ---
            if (imageGalleryUrls.length > 0) {
                sidebarContent.querySelector('.sidebar-image-container').addEventListener('click', (e) => {
                    const index = parseInt(e.currentTarget.dataset.index, 10);
                    showLightbox(imageGalleryUrls, index);
                });

                sidebarContent.querySelectorAll('.gallery-thumbnail').forEach(thumb => {
                    thumb.addEventListener('click', (e) => {
                        const index = parseInt(e.currentTarget.dataset.index, 10);
                        showLightbox(imageGalleryUrls, index);
                    });
                });
            }
        });
    }

    // --- DATA FETCHING (UNCHANGED) ---
    fetch('boat_ramps.geojson').then(res => res.json()).then(data => L.geoJSON(data, { onEachFeature }).addTo(map));

    // ... (Your existing weather and tide fetching code remains here, unchanged)
    const TIDE_API_URL = 'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=today&station=8771450&product=predictions&datum=STND&time_zone=lst&interval=hilo&units=english&format=json';
    async function fetchAndDisplayTides() {
        try {
            const response = await fetch(TIDE_API_URL);
            if (!response.ok) throw new Error('Tide fetch failed');
            const tideJson = await response.json();
            const predictions = tideJson.predictions;
            if (!predictions) return;
            const now = new Date();
            let nextTideIndex = -1;
            for (let i = 0; i < predictions.length; i++) { if (new Date(predictions[i].t) > now) { nextTideIndex = i; break; } }
            const tideWidgetContainer = document.getElementById('tide-widget');
            const titleDate = now.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
            let widgetHTML = `<div id="tide-widget-title">Tides for ${titleDate}:</div>`;
            predictions.forEach((tide, index) => {
                const timeString = new Date(tide.t).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
                const tideTypeText = (tide.type === 'H') ? 'High' : 'Low';
                let pillClasses = 'tide-pill ' + ((tide.type === 'H') ? 'high-tide' : 'low-tide');
                if (index === nextTideIndex) { pillClasses += ' next-tide'; }
                widgetHTML += `<div class="${pillClasses}"><span class="tide-pill-time">${timeString}</span><span class="tide-pill-level">${tideTypeText}</span><span class="tide-tooltip">${parseFloat(tide.v).toFixed(2)} ft</span></div>`;
            });
            tideWidgetContainer.innerHTML = widgetHTML;
        } catch (error) { console.error("Failed to display tides:", error); }
    }

    var weatherControl = L.control({ position: 'topleft' });
    weatherControl.onAdd = function (map) { this._div = L.DomUtil.create('div', 'weather-panel'); this._div.innerHTML = '<h4>Loading Data...</h4>'; return this._div; };
    weatherControl.addTo(map);

    const weatherWaterUrl = 'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=latest&station=8771450&product=water_temperature&datum=STND&time_zone=lst&units=english&format=json';
    fetch(`https://api.weather.gov/points/29.3013,-94.7977`)
        .then(res => res.json()).then(pointData => fetch(pointData.properties.forecastHourly))
        .then(res => res.json()).then(hourlyData => {
            fetch(weatherWaterUrl).then(res => res.json()).then(waterData => {
                const p = hourlyData.properties.periods[0];
                let wt = 'N/A';
                if (waterData.data && waterData.data.length > 0) { wt = `${waterData.data[0].v}°F`; }
                weatherControl._div.innerHTML = `<div class="temp-large">${p.temperature}°F</div><div class="description">${p.shortForecast}</div><div class="details">Wind: ${p.windSpeed} ${p.windDirection}</div><div class="details">Humidity: ${p.relativeHumidity ? p.relativeHumidity.value : 'N/A'}%</div><div class="water-temp">Water Temp: ${wt}</div>`;
            }).catch(e => console.error("Water temp error:", e));
        }).catch(e => console.error("Weather error:", e));

    fetchAndDisplayTides();
});
