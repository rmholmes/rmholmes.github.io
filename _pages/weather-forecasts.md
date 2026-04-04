---
title: "Weather Forecasts"
permalink: /weather-forecasts/
author_profile: true
---

{% include base_path %}

7-day detailed weather forecast for Katoomba, NSW with temperature, wind, and rainfall predictions.

<div style="text-align: center; margin-bottom: 20px;">
  <button onclick="location.reload();" style="padding: 10px 20px; font-size: 16px; background-color: #008cba; color: white; border: none; border-radius: 4px; cursor: pointer;">
    🔄 Refresh Data
  </button>
  <p style="font-size: 12px; color: #666;">
    Last updated: <span id="last-updated">Loading...</span>
  </p>
</div>

<div style="text-align: center;">
  <img id="forecast-plot" src="/images/bom_forecast_katoomba.png" alt="BOM Forecast for Katoomba" style="width: 100%; max-width: 900px; height: auto;">
</div>

<script>
  // Try to get the last commit time for this image
  fetch('https://api.github.com/repos/rmholmes/rmholmes.github.io/commits?path=images/bom_forecast_katoomba.png&per_page=1')
    .then(response => response.json())
    .then(data => {
      if (data.length > 0) {
        const timestamp = new Date(data[0].commit.committer.date);
        document.getElementById('last-updated').textContent = timestamp.toLocaleString();
      }
    })
    .catch(error => {
      document.getElementById('last-updated').textContent = 'Unable to fetch update time';
    });
  
  // Add a cache-busting query parameter to force browser to reload the image
  document.getElementById('forecast-plot').src += '?t=' + new Date().getTime();
</script>

## About this forecast

This is a detailed 3-hourly forecast for **Katoomba, NSW** scraped directly from the [Bureau of Meteorology](https://bom.gov.au) forecast page. The forecast updates automatically several times per day as new data becomes available.

### What you're seeing:

- **Temperature & Dew Point**: Red line shows air temperature, blue line shows dew point (when these converge, expect fog or cloud formation)
- **Wind Speed & Direction**: Arrow symbols show wind direction, colored by speed (red = light winds, orange = moderate, green = strong)
- **Chance of Rain**: Bar chart shows probability of any rain at each 3-hour interval

The shaded gray areas indicate the typical afternoon thermal window (12pm-6pm) when climbing conditions are often best.
