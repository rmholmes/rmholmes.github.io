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
    Last updated: <span id="last-updated">Checking...</span>
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
  // Simple approach: try to load timestamp, show file mod time as fallback
  function updateTimestamp() {
    // Try fetching the timestamp file
    fetch('/files/forecast_timestamp.txt?v=' + Math.random())
      .then(r => r.text())
      .then(text => {
        console.log('Parsed timestamp text:', text);
        try {
          const date = new Date(text.trim());
          if (!isNaN(date)) {
            document.getElementById('last-updated').textContent = date.toLocaleString();
            return;
          }
        } catch (e) {
          console.error('Date parse error:', e);
        }
        // Fallback
        document.getElementById('last-updated').textContent = 'Just now';
      })
      .catch(e => {
        console.error('Fetch failed:', e);
        document.getElementById('last-updated').textContent = 'Just now';
      });
  }
  
  // Wait a moment for page to fully load
  setTimeout(updateTimestamp, 500);
  
  // Cache bust images
  setTimeout(() => {
    const t = '?t=' + new Date().getTime();
    const k = document.getElementById('forecast-plot-katoomba');
    const n = document.getElementById('forecast-plot-nowra');
    if (k && !k.src.includes('?')) k.src += t;
    if (n && !n.src.includes('?')) n.src += t;
  }, 1000);
</script>

## About these forecasts

These are detailed 3-hourly forecasts for popular climbing locations in NSW, scraped directly from the [Bureau of Meteorology](https://bom.gov.au) forecast pages. The forecasts update automatically several times per day as new data becomes available.

### What you're seeing:

- **Temperature & Dew Point**: Red line shows air temperature, blue line shows dew point (when these converge, expect fog or cloud formation)
- **Wind Speed & Direction**: Arrow symbols show wind direction, colored by speed (red = light winds, orange = moderate, green = strong)
- **Chance of Rain**: Bar chart shows probability of any rain at each 3-hour interval

The shaded gray areas indicate the typical afternoon thermal window (12pm-6pm) when climbing conditions are often best.
