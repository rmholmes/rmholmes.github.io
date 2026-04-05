---
title: "Weather Forecasts for Climbing Areas"
permalink: /weather-forecasts/
author_profile: true
---

{% include base_path %}

7-day detailed weather forecasts for climbing locations in NSW with temperature, wind, and rainfall predictions.

<div style="text-align: center; margin-bottom: 20px;">
  <p style="font-size: 12px; color: #666;">
    Last updated: <span id="last-updated">loading</span>
  </p>
</div>

<h2>Katoomba</h2>
<p style="font-size: 12px; color: #666;">
  <a href="https://www.bom.gov.au/places/nsw/katoomba/forecast/detailed/" target="_blank">View on BOM website</a>
</p>
<div style="text-align: center;">
  <img id="forecast-plot-katoomba" src="/images/bom_forecast_katoomba.png" alt="BOM Forecast for Katoomba" style="width: 100%; max-width: 900px; height: auto;">
</div>

<h2>Nowra</h2>
<p style="font-size: 12px; color: #666;">
  <a href="https://www.bom.gov.au/places/nsw/nowra/forecast/detailed/" target="_blank">View on BOM website</a>
</p>
<div style="text-align: center;">
  <img id="forecast-plot-nowra" src="/images/bom_forecast_nowra.png" alt="BOM Forecast for Nowra" style="width: 100%; max-width: 900px; height: auto;">
</div>

<script src="/assets/js/forecast.js" defer></script>

## About these forecasts

These are detailed 3-hourly forecasts for popular climbing locations in NSW, scraped directly from the detailed forecast pages from the old [Bureau of Meteorology](https://reg.bom.gov.au) website. The plots are simply a graphical representation of the underlying tabular forecast data.

### Update schedule

Forecasts are updated automatically 30 minutes after each BOM forecast issue time:
- **05:30 UTC** (4:30 PM AEDT / 3:30 PM AEST)
- **11:30 UTC** (10:30 PM AEDT / 9:30 PM AEST)
- **17:30 UTC** (4:30 AM AEDT / 3:30 AM AEST)
- **23:30 UTC** (10:30 AM AEDT / 9:30 AM AEST)

### What you're seeing:

- **Temperature & Dew Point**: Red line shows air temperature, blue line shows dew point. Low dew point temperatures indicate low humidity. Dew point temperature is generally a more robust metric to look at than relative humidity (in percentage) because the relative humidity is strongly dependent on air temperature. I.e. the relative humidity generally decreases in the afternoon when the air temperature increases, but this does not actually indicate that there is less water in the air.

- **Wind Speed & Direction**: Arrow symbols show wind direction, with colors indicating speed (red = very light winds less than 5 knots, orange = light winds between 5 and 10 knots, green = moderate winds greater than 10 knots). Higher wind speeds generally lead to better climbing conditions, but this depends on the relative exposure of the cliff you're climbing at compared to the wind direction.

- **Chance of Rain**: Bar chart shows probability of any rain within each 3-hour interval.

The gray shaded areas indicate the typical afternoon climbing period between midday and 6pm.
