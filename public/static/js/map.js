// Initialize map centered on Pine Barrens
const map = L.map('map').setView([39.8, -74.5], 9);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Layer groups
const layers = {
    fireRisk: L.layerGroup().addTo(map),
    evacuationRoutes: L.layerGroup(),
    fireStations: L.layerGroup(),
    waterSources: L.layerGroup()
};

// Icons
const icons = {
    fireStation: L.icon({
        iconUrl: '/static/icons/fire-station.png',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    }),
    waterSource: L.icon({
        iconUrl: '/static/icons/water-source.png',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    })
};

// Initialize map data
let mapData = {
    fireStations: [],
    waterSources: [],
    evacuationRoutes: [],
    riskAreas: []
};

// Load map data
async function loadMapData() {
    try {
        const response = await fetch('/api/map-data');
        mapData = await response.json();
        
        // Add fire stations
        mapData.fireStations.forEach(station => {
            L.marker(station.coords, {icon: icons.fireStation})
                .bindPopup(`<b>${station.name}</b>`)
                .addTo(layers.fireStations);
        });

        // Add water sources
        mapData.waterSources.forEach(source => {
            L.marker(source.coords, {icon: icons.waterSource})
                .bindPopup(`<b>${source.name}</b>`)
                .addTo(layers.waterSources);
        });

        // Add evacuation routes
        mapData.evacuationRoutes.forEach(route => {
            L.polyline(route.path, {
                color: 'blue',
                weight: 3,
                opacity: 0.7
            })
            .bindPopup(`<b>${route.name}</b>`)
            .addTo(layers.evacuationRoutes);
        });

        // Initial risk areas update
        updateRiskAreas();
    } catch (error) {
        console.error('Error loading map data:', error);
    }
}

// Update risk areas based on selected time range
async function updateRiskAreas() {
    try {
        const timeRange = document.getElementById('timeRange').value;
        layers.fireRisk.clearLayers();

        const response = await fetch(`/api/fire-risk?timeRange=${timeRange}`);
        const riskData = await response.json();

        riskData.riskAreas.forEach(area => {
            const color = getRiskColor(area.riskLevel);
            const radius = area.severity * 1000; // Convert to meters

            L.circle(area.coords, {
                color: color,
                fillColor: color,
                fillOpacity: 0.4,
                radius: radius
            })
            .bindPopup(`
                <b>Risk Level: ${area.riskLevel}</b><br>
                Factors:<br>
                ${area.factors.map(f => `• ${f.name}: ${f.value}`).join('<br>')}
            `)
            .addTo(layers.fireRisk);
        });
    } catch (error) {
        console.error('Error updating risk areas:', error);
    }
}

// Get color based on risk level
function getRiskColor(riskLevel) {
    switch (riskLevel.toLowerCase()) {
        case 'extreme': return '#ff0000';
        case 'high': return '#ff6600';
        case 'moderate': return '#ffcc00';
        case 'low': return '#00cc00';
        default: return '#00ff00';
    }
}

// Layer control event listeners
document.getElementById('fireRiskLayer').addEventListener('change', function(e) {
    if (e.target.checked) {
        map.addLayer(layers.fireRisk);
    } else {
        map.removeLayer(layers.fireRisk);
    }
});

document.getElementById('evacuationRoutes').addEventListener('change', function(e) {
    if (e.target.checked) {
        map.addLayer(layers.evacuationRoutes);
    } else {
        map.removeLayer(layers.evacuationRoutes);
    }
});

document.getElementById('fireStations').addEventListener('change', function(e) {
    if (e.target.checked) {
        map.addLayer(layers.fireStations);
    } else {
        map.removeLayer(layers.fireStations);
    }
});

document.getElementById('waterSources').addEventListener('change', function(e) {
    if (e.target.checked) {
        map.addLayer(layers.waterSources);
    } else {
        map.removeLayer(layers.waterSources);
    }
});

// Initialize map data on load
loadMapData();
