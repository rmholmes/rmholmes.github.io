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
    Last updated: <span id="last-updated">Loading...</span>
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
  // Try multiple approaches to load the timestamp
  
  // Approach 1: Use plain text file for simpler access
  fetch('{{ site.baseurl }}/files/forecast_timestamp.txt')
    .then(response => {
      if (!response.ok) throw new Error('timestamp.txt not found');
      return response.text();
    })
    .then(timestamp => {
      const date = new Date(timestamp);
      document.getElementById('last-updated').textContent = date.toLocaleString();
    })
    .catch(err1 => {
      console.log('Timestamp fetch failed:', err1);
      // Fallback: try JSON
      return fetch('{{ site.baseurl }}/files/forecast_metadata.json')
        .then(response => response.json())
        .then(data => {
          const date = new Date(data.timestamp);
          document.getElementById('last-updated').textContent = date.toLocaleString();
        })
        .catch(err2 => {
          console.error('Both timestamp methods failed:', err1, err2);
          document.getElementById('last-updated').textContent = 'Unable to load update time';
        });
    });
  
  // Force browser to reload images (cache-busting)
  const cacheBuster = '?t=' + new Date().getTime();
  document.getElementById('forecast-plot-katoomba').src += cacheBuster;
  document.getElementById('forecast-plot-nowra').src += cacheBuster;
</script>

## About these forecasts

These are detailed 3-hourly forecasts for popular climbing locations in NSW, scraped directly from the [Bureau of Meteorology](https://bom.gov.au) forecast pages. The forecasts update automatically several times per day as new data becomes available.

### What you're seeing:

- **Temperature & Dew Point**: Red line shows air temperature, blue line shows dew point (when these converge, expect fog or cloud formation)
- **Wind Speed & Direction**: Arrow symbols show wind direction, colored by speed (red = light winds, orange = moderate, green = strong)
- **Chance of Rain**: Bar chart shows probability of any rain at each 3-hour interval

The shaded gray areas indicate the typical afternoon thermal window (12pm-6pm) when climbing conditions are often best.
