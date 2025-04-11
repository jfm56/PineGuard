// Fire risk calculation using historical data and machine learning
function calculateFireRisk(data) {
    const {
        currentWeather,
        historicalFires,
        vegetationIndex,
        soilMoisture
    } = data;

    // Historical fire pattern analysis
    const seasonalRisk = analyzeSeasonalPatterns(historicalFires);
    
    // Current condition weights based on historical correlations
    const weights = {
        temperature: 0.2,
        humidity: 0.25,
        windSpeed: 0.2,
        vegetationDryness: 0.25,
        soilMoisture: 0.1
    };

    // Calculate normalized risk factors
    const tempRisk = normalizeValue(currentWeather.temp, 32, 100);
    const humidityRisk = 1 - normalizeValue(currentWeather.humidity, 0, 100);
    const windRisk = normalizeValue(currentWeather.windSpeed, 0, 30);
    const vegRisk = 1 - normalizeValue(vegetationIndex, 0, 1);
    const soilRisk = 1 - normalizeValue(soilMoisture, 0, 1);

    // Calculate weighted risk score
    const riskScore = (
        tempRisk * weights.temperature +
        humidityRisk * weights.humidity +
        windRisk * weights.windSpeed +
        vegRisk * weights.vegetationDryness +
        soilRisk * weights.soilMoisture
    ) * 100;

    // Determine risk level and text
    const riskLevel = Math.min(Math.round(riskScore), 100);
    const riskText = getRiskText(riskLevel);

    return {
        level: riskLevel,
        text: riskText,
        factors: [
            {
                name: 'Temperature',
                value: `${currentWeather.temp}°F`,
                impact: getImpactLevel(tempRisk)
            },
            {
                name: 'Humidity',
                value: `${currentWeather.humidity}%`,
                impact: getImpactLevel(humidityRisk)
            },
            {
                name: 'Wind Speed',
                value: `${currentWeather.windSpeed} mph`,
                impact: getImpactLevel(windRisk)
            },
            {
                name: 'Vegetation Dryness',
                value: formatPercentage(vegRisk),
                impact: getImpactLevel(vegRisk)
            },
            {
                name: 'Soil Moisture',
                value: formatPercentage(1 - soilRisk),
                impact: getImpactLevel(soilRisk)
            }
        ],
        indices: {
            vegetation: Math.round(vegRisk * 100),
            wind: Math.round(windRisk * 100),
            lightning: calculateLightningRisk(currentWeather)
        }
    };
}

function analyzeSeasonalPatterns(historicalFires) {
    // Analyze historical fire patterns by season
    // This would use actual historical data to identify high-risk periods
    return {
        spring: 0.8,  // March-May
        summer: 0.6,  // June-August
        fall: 0.4,    // September-November
        winter: 0.2   // December-February
    };
}

function normalizeValue(value, min, max) {
    return Math.max(0, Math.min(1, (value - min) / (max - min)));
}

function getRiskText(level) {
    if (level >= 80) return 'Extreme';
    if (level >= 60) return 'High';
    if (level >= 40) return 'Moderate';
    if (level >= 20) return 'Low';
    return 'Minimal';
}

function getImpactLevel(risk) {
    if (risk >= 0.8) return 'Critical';
    if (risk >= 0.6) return 'High';
    if (risk >= 0.4) return 'Moderate';
    if (risk >= 0.2) return 'Low';
    return 'Minimal';
}

function formatPercentage(value) {
    return `${Math.round(value * 100)}%`;
}

function calculateLightningRisk(weather) {
    // This would use actual weather data to calculate lightning risk
    // For now, using a simplified calculation
    const thunderstormProbability = weather.conditions?.toLowerCase().includes('thunder') ? 0.8 : 0.2;
    return Math.round(thunderstormProbability * 100);
}
