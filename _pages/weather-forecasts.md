---
title: "Weather Forecasts"
permalink: /weather-forecasts/
author_profile: true
---

{% include base_path %}

7-day detailed weather forecasts for climbing locations in NSW with temperature, wind, and rainfall predictions.

<div style="text-align: center; margin-bottom: 20px;">
  <button onclick="location.reload();" style="padding: 10px 20px; font-size: 16px; background-color: #008cba; color: white; border: none; border-radius: 4px; cursor: pointer;">
    🔄 Refresh Data
  </button>
  <p style="font-size: 12px; color: #666;">
    Last updated: <span id="last-updated">—</span>
  </p>
</div>

<h2>Katoomba</h2>
<div style="text-align: center;">
  <img id="forecast-plot-katoomba" src="/images/bom_forecast_katoomba.png" alt="BOM Forecast for Katoomba" style="width: 100%; max-width: 900px; height: auto;">
</div>

<h2>Nowra</h2>
<div style="text-align: center;">
  <img id="forecast-plot-nowra" src="/images/bom_forecast_nowra.png" alt="BOM Forecast for Nowra" style="width: 100%; max-width: 900px; height: auto;">
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  // Load timestamp from JSON file
  fetch('/files/forecast_metadata.json')
    .then(response => response.json())
    .then(data => {
      if (data && data.timestamp) {
        const date = new Date(data.timestamp);
        if (isFinite(date)) {
          document.getElementById('last-updated').textContent = date.toLocaleString();
        }
      }
    })
    .catch(err => {
      console.error('Error loading timestamp:', err);
    });
  
  // Force refresh images with cache buster
  const now = new Date().getTime();
  const img1 = document.getElementById('forecast-plot-katoomba');
  const img2 = document.getElementById('forecast-plot-nowra');
  if (img1) img1.src = img1.src.split('?')[0] + '?t=' + now;
  if (img2) img2.src = img2.src.split('?')[0] + '?t=' + now;
});
</script>

## About these forecasts

These are detailed 3-hourly forecasts for popular climbing locations in NSW, scraped directly from the [Bureau of Meteorology](https://bom.gov.au) forecast pages. The forecasts update automatically several times per day as new data becomes available.

### What you're seeing:

- **Temperature & Dew Point**: Red line shows air temperature, blue line shows dew point (when these converge, expect fog or cloud formation)
- **Wind Speed & Direction**: Arrow symbols show wind direction, colored by speed (red = light winds, orange = moderate, green = strong)
- **Chance of Rain**: Bar chart shows probability of any rain at each 3-hour interval

The shaded gray areas indicate the typical afternoon thermal window (12pm-6pm) when climbing conditions are often best.
