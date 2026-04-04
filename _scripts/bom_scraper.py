"""
BOM Weather Forecast Scraper and Data Processor

Extracts 7-day detailed forecast data from Bureau of Meteorology website
for Katoomba (3-hourly: temperature, wind, rain, dew point, humidity)
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# Constants
WIND_DIRECTION_ARROWS = {
    # Maps compass directions to Unicode arrows (meteorological convention: arrow points FROM origin)
    'N': '↓', 'NNE': '↙', 'NE': '↙', 'ENE': '←',
    'E': '←', 'ESE': '↖', 'SE': '↖', 'SSE': '↑',
    'S': '↑', 'SSW': '↗', 'SW': '↗', 'WSW': '→',
    'W': '→', 'WNW': '↘', 'NW': '↘', 'NNW': '↓'
}

WIND_SPEED_COLORS = {
    # Colors for wind speed visualization (green=fast/good for climbing, red=slow/bad)
    'red': {'threshold': 5, 'description': 'Light winds (< 5 knots)'},
    'orange': {'threshold': 10, 'description': 'Moderate (5-10 knots)'},
    'green': {'threshold': float('inf'), 'description': 'Strong (> 10 knots)'}
}


def scrape_bom_forecast(location='katoomba'):
    """
    Scrape BOM detailed forecast page for specified location.
    
    Args:
        location (str): Location slug from BOM URL (default: 'katoomba')
    
    Returns:
        BeautifulSoup: Parsed HTML content or None if fetch fails
    """
    url = f"https://reg.bom.gov.au/places/nsw/{location}/forecast/detailed/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_forecast_data(soup):
    """
    Extract forecast data from BOM HTML.
    
    Parses 35 HTML tables (7 days × 5 table types) to extract:
    - Temperature, Dew Point, Wind Speed, Wind Direction, Humidity, Rain Probability
    
    Args:
        soup (BeautifulSoup): Parsed HTML content
    
    Returns:
        pd.DataFrame: 56 rows (8 time slots/day × 7 days), 8 columns with forecast data
    """
    if not soup:
        return pd.DataFrame()
    
    tables = soup.find_all('table')
    consolidated_data = []
    
    # Process tables in groups of 5 (one group per day)
    for day_idx in range(0, len(tables), 5):
        if day_idx + 4 >= len(tables):
            break
        
        rainfall_table = tables[day_idx]
        temp_table = tables[day_idx + 1]
        wind_humidity_table = tables[day_idx + 4]
        
        # Extract day name from rainfall table summary
        rainfall_summary = rainfall_table.get('summary', '')
        day_name = rainfall_summary.split('for ')[-1] if 'for' in rainfall_summary else 'Unknown'
        
        # Get table rows
        temp_rows = temp_table.find_all('tr')
        wind_humidity_rows = wind_humidity_table.find_all('tr')
        rainfall_rows = rainfall_table.find_all('tr')
        
        # Extract time slots from temperature table headers
        time_headers = temp_rows[0].find_all(['th', 'td'])
        times = [th.get_text(strip=True) for th in time_headers[1:]]
        
        # Extract temperature (first data row)
        temp_cells = temp_rows[1].find_all(['td', 'th'])
        temps = [c.get_text(strip=True) for c in temp_cells[1:]]
        
        # Extract dew point (search for row with "dew" label)
        dew_points = []
        for row in temp_rows[1:]:
            label_cell = row.find(['th', 'td'])
            if label_cell and 'dew' in label_cell.get_text().lower():
                dew_cells = row.find_all(['td', 'th'])
                dew_points = [c.get_text(strip=True) for c in dew_cells[1:]]
                break
        
        # Extract wind speed, direction, humidity from wind/humidity table
        wind_speeds_kmh = []
        wind_dirs = []
        humidity = []
        
        for row in wind_humidity_rows:
            label_cell = row.find(['th', 'td'])
            if not label_cell:
                continue
            
            label = label_cell.get_text().lower()
            data_cells = row.find_all(['td', 'th'])[1:]
            
            if 'wind speed' in label:
                # Extract wind speed from data-kmh attribute (not from text which gets concatenated)
                for cell in data_cells:
                    kmh_val = cell.get('data-kmh', '')
                    wind_speeds_kmh.append(kmh_val)
            elif 'wind direction' in label and 'wind speed' not in label:
                for cell in data_cells:
                    wind_dirs.append(cell.get_text(strip=True))
            elif 'humidity' in label:
                for cell in data_cells:
                    humidity.append(cell.get_text(strip=True))
        
        # Extract rain chance (find "Chance of any rain" row, not precipitation rows)
        rain_chances = []
        for row in rainfall_rows:
            label_cell = row.find(['th', 'td'])
            if label_cell and 'chance of any rain' in label_cell.get_text().lower():
                rain_cells = row.find_all(['td', 'th'])[1:]
                rain_chances = [c.get_text(strip=True) for c in rain_cells]
                break
        
        # Create consolidated records (one per time slot)
        for i, time in enumerate(times):
            record = {
                'Day': day_name,
                'Time': time,
                'Temperature_C': temps[i] if i < len(temps) else '',
                'Wind_Speed_kmh': wind_speeds_kmh[i] if i < len(wind_speeds_kmh) else '',
                'Wind_Direction': wind_dirs[i] if i < len(wind_dirs) else '',
                'Humidity_Percent': humidity[i] if i < len(humidity) else '',
                'Dew_Point_C': dew_points[i] if i < len(dew_points) else '',
                'Rain_Chance_Percent': rain_chances[i] if i < len(rain_chances) else ''
            }
            consolidated_data.append(record)
    
    return pd.DataFrame(consolidated_data)


def to_numeric(val):
    """
    Convert string values to float, handling dashes and percentage symbols.
    
    Args:
        val: Value to convert (string or numeric)
    
    Returns:
        float: Numeric value or np.nan if conversion fails
    """
    if val == '–' or val == '' or pd.isna(val):
        return np.nan
    try:
        val_str = str(val).replace('%', '').strip()
        return float(val_str)
    except:
        return np.nan


def prepare_forecast_data(df, base_date=None):
    """
    Prepare forecast data: convert to numeric types and create DateTime index.
    
    Args:
        df (pd.DataFrame): Raw forecast DataFrame from extract_forecast_data()
        base_date (datetime): Start date for forecast (default: today)
    
    Returns:
        pd.DataFrame: Prepared DataFrame with numeric columns, DateTime index, sorted by time
    """
    if df.empty:
        return df
    
    df = df.copy()
    
    # Convert numeric columns
    for col in ['Temperature_C', 'Dew_Point_C', 'Wind_Speed_kmh', 'Humidity_Percent', 'Rain_Chance_Percent']:
        df[col] = df[col].apply(to_numeric)
    
    # Create DateTime index combining Day and Time columns
    if base_date is None:
        base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    days_list = df['Day'].unique()
    day_to_date = {day: base_date + timedelta(days=i) for i, day in enumerate(days_list)}
    
    def create_datetime(row):
        day_date = day_to_date.get(row['Day'], base_date)
        try:
            time_obj = datetime.strptime(row['Time'], '%I:%M %p')
            return day_date.replace(hour=time_obj.hour, minute=time_obj.minute)
        except:
            return None
    
    df['DateTime'] = df.apply(create_datetime, axis=1)
    df = df.sort_values('DateTime')
    
    return df


def get_arrow_for_direction(direction):
    """
    Get Unicode arrow symbol for wind direction.
    
    Args:
        direction (str): Compass direction (e.g., 'N', 'NE', 'ESE')
    
    Returns:
        str: Unicode arrow pointing FROM wind origin (meteorological convention)
    """
    return WIND_DIRECTION_ARROWS.get(direction, '→')


def get_arrow_color(wind_speed_knots):
    """
    Get color for wind arrow based on speed (good for climbing use case).
    
    Args:
        wind_speed_knots (float): Wind speed in knots
    
    Returns:
        str: Color name ('red'=slow/bad, 'orange'=moderate, 'green'=fast/good)
    """
    if wind_speed_knots < 5:
        return 'red'
    elif wind_speed_knots <= 10:
        return 'orange'
    else:
        return 'green'
