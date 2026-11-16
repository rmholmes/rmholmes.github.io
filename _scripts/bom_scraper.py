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
from zoneinfo import ZoneInfo


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

OBSERVATION_URL = 'https://www.bom.gov.au/fwo/IDN60801/IDN60801.94743.json'
OBSERVATION_TIMEZONE = 'Australia/Sydney'
WIND_DIRECTIONS = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                   'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
WIND_BEARINGS = {direction: index * 22.5 for index, direction in enumerate(WIND_DIRECTIONS)}


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


def scrape_bom_observations():
    """Fetch the latest Mt Boyce observation records from the BOM JSON feed."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; forecast-observations/1.0)'
    }

    try:
        response = requests.get(OBSERVATION_URL, headers=headers, timeout=15)
        response.raise_for_status()
        records = response.json()['observations']['data']
        if not isinstance(records, list):
            raise ValueError('BOM observation data is not a list')
        return records
    except Exception as e:
        print(f"Error fetching Mt Boyce observations: {e}")
        return []


def prepare_bom_observations(records, now=None):
    """Aggregate Mt Boyce observations into Sydney-local 3-hour bins.

    Bins are right-closed and labeled at their end time, matching forecast
    valid-time labels. Bins with fewer than three observations are omitted.
    """
    columns = [
        'DateTime', 'Air_Temperature_C', 'Dew_Point_C', 'Humidity_Percent',
        'Wind_Speed_kt', 'Wind_Gust_kt', 'Wind_Direction', 'Rainfall_3h_mm',
        'Observation_Count'
    ]
    if not records:
        return pd.DataFrame(columns=columns)

    observations = pd.DataFrame(records)
    if 'aifstime_utc' not in observations:
        return pd.DataFrame(columns=columns)

    timestamps = pd.to_datetime(
        observations['aifstime_utc'],
        format='%Y%m%d%H%M%S',
        errors='coerce',
        utc=True
    )
    observations['DateTime'] = timestamps.dt.tz_convert(OBSERVATION_TIMEZONE)
    observations = observations.dropna(subset=['DateTime'])
    observations = observations.sort_values('DateTime').drop_duplicates(
        'DateTime', keep='last'
    )
    observations['DateTime'] = observations['DateTime'].dt.tz_localize(None)

    source_columns = {
        'air_temp': 'Air_Temperature_C',
        'dewpt': 'Dew_Point_C',
        'rel_hum': 'Humidity_Percent',
        'wind_spd_kt': 'Wind_Speed_kt',
        'gust_kt': 'Wind_Gust_kt',
        'rain_trace': 'Rain_Trace_mm'
    }
    for source, target in source_columns.items():
        observations[target] = pd.to_numeric(observations.get(source), errors='coerce')

    direction_bearing = observations.get('wind_dir', pd.Series(index=observations.index))
    direction_radians = np.deg2rad(direction_bearing.map(WIND_BEARINGS))
    wind_speed = observations['Wind_Speed_kt']
    observations['Wind_Eastward'] = -np.sin(direction_radians) * wind_speed
    observations['Wind_Northward'] = -np.cos(direction_radians) * wind_speed
    observations['Observation_Count'] = 1

    rain_trace = observations['Rain_Trace_mm']
    previous_rain = rain_trace.ffill().shift(1)
    rainfall_change = rain_trace - previous_rain
    rainfall_change = rainfall_change.where(rainfall_change >= 0, rain_trace)
    observations['Rainfall_Increment_mm'] = rainfall_change.fillna(0).clip(lower=0)

    indexed = observations.set_index('DateTime')
    bins = indexed.resample('3h', closed='right', label='right', origin='start_day')
    aggregate_columns = [
        'Air_Temperature_C', 'Dew_Point_C', 'Humidity_Percent', 'Wind_Speed_kt',
        'Wind_Eastward', 'Wind_Northward'
    ]
    aggregated = bins[aggregate_columns].mean()
    aggregated['Wind_Gust_kt'] = bins['Wind_Gust_kt'].max()
    aggregated['Rainfall_3h_mm'] = bins['Rainfall_Increment_mm'].sum()
    aggregated['Observation_Count'] = bins['Observation_Count'].sum()

    bearing = np.degrees(np.arctan2(
        -aggregated['Wind_Eastward'], -aggregated['Wind_Northward']
    )) % 360

    def compass_direction(value):
        if pd.isna(value):
            return np.nan
        index = int(np.floor((value + 11.25) / 22.5)) % len(WIND_DIRECTIONS)
        return WIND_DIRECTIONS[index]

    aggregated['Wind_Direction'] = bearing.map(compass_direction)
    incomplete = aggregated['Observation_Count'] < 3
    result_columns = [
        'Air_Temperature_C', 'Dew_Point_C', 'Humidity_Percent', 'Wind_Speed_kt',
        'Wind_Gust_kt', 'Rainfall_3h_mm', 'Wind_Direction'
    ]
    aggregated.loc[incomplete, result_columns] = np.nan

    timezone = ZoneInfo(OBSERVATION_TIMEZONE)
    if now is None:
        now = pd.Timestamp.now(tz=timezone).tz_localize(None)
    else:
        now = pd.Timestamp(now)
        if now.tzinfo is not None:
            now = now.tz_convert(timezone).tz_localize(None)

    last_complete_bin = now.floor('3h')
    first_bin = last_complete_bin - pd.Timedelta(hours=48)
    aggregated = aggregated.loc[
        (aggregated.index > first_bin) & (aggregated.index <= last_complete_bin)
    ].copy()
    aggregated['DateTime'] = aggregated.index
    return aggregated.reset_index(drop=True)[columns]


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
        
        # Extract day name and date from previous sibling elements
        # The date appears as a sibling text node like "Monday 6 April"
        # (not in the table summary which only says "3 Hourly Rainfall Forecast for Monday")
        date_string = ''
        day_name = 'Unknown'
        
        # Look for previous text siblings to find the date (format: "Day Date Month")
        for prev_elem in rainfall_table.find_previous_siblings():
            text = prev_elem.get_text(strip=True) if hasattr(prev_elem, 'get_text') else str(prev_elem).strip()
            # Check if this looks like a date (starts with day name and contains month name)
            if any(day in text for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']):
                if any(month in text for month in ['January', 'February', 'March', 'April', 'May', 'June', 
                                                     'July', 'August', 'September', 'October', 'November', 'December']):
                    date_string = text
                    day_name = text.split()[0] if ' ' in text else text
                    break
        
        # Fallback: extract day name from table summary if we couldn't find the date string
        if not date_string:
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
                'Date_String': date_string,
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
        base_date (datetime): Start date for forecast (default: today) - IGNORED if Date_String is available
    
    Returns:
        pd.DataFrame: Prepared DataFrame with numeric columns, DateTime index, sorted by time
    """
    if df.empty:
        return df
    
    df = df.copy()
    
    # Convert numeric columns
    for col in ['Temperature_C', 'Dew_Point_C', 'Wind_Speed_kmh', 'Humidity_Percent', 'Rain_Chance_Percent']:
        df[col] = df[col].apply(to_numeric)
    
    # Create DateTime index combining Date_String (if available) or Day, and Time columns
    if 'Date_String' not in df.columns:
        # Fallback to old behavior if Date_String not present
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
    else:
        # Use Date_String to extract actual calendar dates
        # Date_String format: e.g., "Friday 4 April 2025" or "Friday 4 April"
        date_to_date = {}
        for date_string in df['Date_String'].unique():
            try:
                # Try parsing with year first
                date_obj = datetime.strptime(date_string.strip(), '%A %d %B %Y').date()
                date_to_date[date_string] = date_obj
            except ValueError:
                try:
                    # Try parsing without year (add current year)
                    date_string_with_year = f"{date_string.strip()} {datetime.now().year}"
                    date_obj = datetime.strptime(date_string_with_year, '%A %d %B %Y').date()
                    date_to_date[date_string] = date_obj
                except ValueError:
                    # If parsing fails, fall back to None
                    date_to_date[date_string] = None
        
        def create_datetime(row):
            day_date = date_to_date.get(row['Date_String'])
            if day_date is None:
                return None
            try:
                time_obj = datetime.strptime(row['Time'], '%I:%M %p')
                return datetime.combine(day_date, time_obj.time())
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
