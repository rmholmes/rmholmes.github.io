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
  // Simple approach: load and display timestamp
  function updateTimestamp() {
    console.log('updateTimestamp called');
    
    fetch('/files/forecast_timestamp.txt?v=' + Math.random())
      .then(r => {
        console.log('Fetch response status:', r.status);
        return r.text();
      })
      .then(text => {
        console.log('Raw text received:', JSON.stringify(text));
        console.log('Text length:', text.length);
        console.log('Text trimmed:', JSON.stringify(text.trim()));
        
        const trimmed = text.trim();
        console.log('Attempting to parse as date:', trimmed);
        
        const date = new Date(trimmed);
        console.log('Parsed date:', date);
        console.log('Date is valid:', !isNaN(date.getTime()));
        
        if (!isNaN(date.getTime())) {
          const formatted = date.toLocaleString();
          console.log('Formatted date:', formatted);
          document.getElementById('last-updated').textContent = formatted;
        } else {
          console.log('Date invalid, showing fallback');
          document.getElementById('last-updated').textContent = 'Recently updated';
        }
      })
      .catch(e => {
        console.error('Caught error:', e);
        document.getElementById('last-updated').textContent = 'Recently updated';
      });
  }
  
  console.log('Script loaded, calling updateTimestamp in 1 second');
  setTimeout(updateTimestamp, 1000);
  
  // Cache bust images
  setTimeout(() => {
    const t = '?t=' + new Date().getTime();
    const k = document.getElementById('forecast-plot-katoomba');
    const n = document.getElementById('forecast-plot-nowra');
    if (k && !k.src.includes('?')) k.src += t;
    if (n && !n.src.includes('?')) n.src += t;
  }, 2000);
</script>

## About these forecasts

These are detailed 3-hourly forecasts for popular climbing locations in NSW, scraped directly from the [Bureau of Meteorology](https://bom.gov.au) forecast pages. The forecasts update automatically several times per day as new data becomes available.

### What you're seeing:

- **Temperature & Dew Point**: Red line shows air temperature, blue line shows dew point (when these converge, expect fog or cloud formation)
- **Wind Speed & Direction**: Arrow symbols show wind direction, colored by speed (red = light winds, orange = moderate, green = strong)
- **Chance of Rain**: Bar chart shows probability of any rain at each 3-hour interval

The shaded gray areas indicate the typical afternoon thermal window (12pm-6pm) when climbing conditions are often best.
