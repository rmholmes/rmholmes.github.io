#!/usr/bin/env python
"""
Generate BOM forecast plots for multiple locations.

Usage:
    python _scripts/generate_forecast.py

Generates:
    - images/bom_forecast_katoomba.png
    - images/bom_forecast_nowra.png
    - _data/forecast_metadata.json (timestamp)
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add _scripts to path so we can import bom_scraper
sys.path.insert(0, str(Path(__file__).parent))

from bom_scraper import (
    scrape_bom_forecast,
    extract_forecast_data,
    prepare_forecast_data,
    get_arrow_for_direction,
    get_arrow_color
)

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from datetime import timedelta


def generate_forecast_plot(location='katoomba', location_name='Katoomba', output_path='images/bom_forecast_katoomba.png'):
    """
    Generate and save a 3-panel BOM forecast plot.
    
    Args:
        location (str): BOM location slug
        location_name (str): Friendly name for display
        output_path (str): Where to save the plot
    """
    print(f"Fetching BOM forecast for {location_name}...")
    soup = scrape_bom_forecast(location)
    
    if not soup:
        raise Exception('Failed to fetch BOM forecast from website')
    
    print("Extracting forecast data...")
    df_raw = extract_forecast_data(soup)
    
    if df_raw.empty:
        raise Exception('No forecast data extracted')
    
    print(f"Preparing data ({len(df_raw)} records)...")
    df = prepare_forecast_data(df_raw)
    
    print("Generating plot...")
    # Create figure with 3 subplots
    fig, axes = plt.subplots(3, 1, figsize=(11, 8))
    fig.suptitle(f'7-Day Forecast for {location_name}', fontsize=16, fontweight='bold')
    
    df_valid = df.dropna(subset=['DateTime', 'Temperature_C'])
    
    # Plot 1: Temperature and Dew Point
    ax1 = axes[0]
    ax1.set_title('Temperature & Dew Point Forecast')
    ax1.set_ylabel('Temperature (°C)')
    
    df_temp_dew = df_valid.dropna(subset=['Dew_Point_C'])
    line1 = ax1.plot(df_temp_dew['DateTime'], df_temp_dew['Temperature_C'],
                     color='tab:red', marker='o', linewidth=2, label='Air Temperature', markersize=5)
    line2 = ax1.plot(df_temp_dew['DateTime'], df_temp_dew['Dew_Point_C'],
                     color='tab:blue', marker='s', linewidth=2, label='Dew Point', markersize=5, alpha=0.8)
    ax1.grid(True, alpha=0.3)
    
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='best')
    
    # Plot 2: Wind Speed and Direction
    ax2 = axes[1]
    ax2.set_title('Wind Speed & Direction Forecast')
    
    df_wind = df_valid[df_valid['Wind_Direction'] != '–'].copy()
    df_wind = df_wind.dropna(subset=['Wind_Speed_kmh'])
    df_wind['Wind_Speed_Knots'] = df_wind['Wind_Speed_kmh'].astype(float) / 1.852
    
    if len(df_wind) > 0:
        df_wind['Arrow'] = df_wind['Wind_Direction'].apply(get_arrow_for_direction)
        
        x_numeric = mdates.date2num(df_wind['DateTime'])
        y_values = df_wind['Wind_Speed_Knots'].values
        
        ax2.scatter(x_numeric, y_values, s=0, alpha=0)
        
        for idx, row in df_wind.iterrows():
            wind_speed = row['Wind_Speed_Knots']
            arrow_color = get_arrow_color(wind_speed)
            ax2.text(mdates.date2num(row['DateTime']), row['Wind_Speed_Knots'],
                    row['Arrow'], fontsize=18, ha='center', va='center',
                    color=arrow_color, weight='bold', zorder=3)
        
        ax2.set_ylabel('Wind Speed (knots)')
        ax2.set_ylim(0, df_wind['Wind_Speed_Knots'].max() * 1.2)
        ax2.grid(True, alpha=0.3)
    else:
        ax2.text(0.5, 0.5, 'No wind data', ha='center', va='center',
                transform=ax2.transAxes)
    
    # Plot 3: Rain Chance
    ax3 = axes[2]
    ax3.set_title('Chance of Rain Forecast')
    df_rain = df_valid.dropna(subset=['Rain_Chance_Percent'])
    if len(df_rain) > 0:
        ax3.bar(df_rain['DateTime'], df_rain['Rain_Chance_Percent'],
               width=0.08, color='steelblue', alpha=0.7, edgecolor='navy')
        ax3.set_ylabel('Rain Probability (%)')
        ax3.set_ylim(0, 100)
        ax3.grid(True, alpha=0.3, axis='y')
    else:
        ax3.text(0.5, 0.5, 'No rain data', ha='center', va='center',
                transform=ax3.transAxes)
    
    # Add afternoon shading and format axes
    def date_formatter(x, pos=None):
        dt = mdates.num2date(x)
        if dt.hour != 12:
            return ''
        return f"{dt.strftime('%A')} {dt.month}/{dt.day}\n12pm"
    
    date_range = df['DateTime'].dropna()
    if len(date_range) > 0:
        start_date = date_range.min().date()
        end_date = date_range.max().date()
        current_date = start_date
        
        while current_date <= end_date:
            noon = datetime(current_date.year, current_date.month, current_date.day, 12, 0)
            six_pm = datetime(current_date.year, current_date.month, current_date.day, 18, 0)
            
            for ax in axes:
                ax.axvspan(mdates.date2num(noon), mdates.date2num(six_pm),
                           alpha=0.15, color='gray', zorder=0)
            
            current_date += timedelta(days=1)
    
    for i, ax in enumerate(axes):
        ax.xaxis.set_major_locator(mdates.HourLocator(byhour=[12]))
        ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=[0]))
        ax.grid(True, which='minor', axis='x', alpha=0.15, linestyle='-', linewidth=0.5)
        
        if i == len(axes) - 1:
            ax.xaxis.set_major_formatter(FuncFormatter(date_formatter))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=0, ha='center')
            ax.set_xlabel('Date')
        else:
            ax.xaxis.set_ticklabels([])
            ax.set_xlabel('')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    print(f"✓ Forecast plot saved to {output_path}")


def generate_all_forecasts():
    """
    Generate forecast plots for all configured locations.
    Also saves metadata with timestamp.
    """
    locations = [
        {'slug': 'katoomba', 'name': 'Katoomba', 'output': 'images/bom_forecast_katoomba.png'},
        {'slug': 'nowra', 'name': 'Nowra', 'output': 'images/bom_forecast_nowra.png'},
    ]
    
    metadata = {
        'timestamp': datetime.now().isoformat(),
        'locations': {}
    }
    
    for loc in locations:
        try:
            print(f"\n{'='*60}")
            print(f"Generating forecast for {loc['name']}...")
            print('='*60)
            generate_forecast_plot(loc['slug'], loc['name'], loc['output'])
            metadata['locations'][loc['slug']] = {
                'name': loc['name'],
                'image': loc['output'],
                'status': 'success'
            }
        except Exception as e:
            print(f"✗ Error generating {loc['name']}: {e}")
            metadata['locations'][loc['slug']] = {
                'name': loc['name'],
                'image': loc['output'],
                'status': 'error',
                'error': str(e)
            }
    
    # Save metadata to files/ directory so it's accessible via /files/
    metadata_dir = Path('files')
    metadata_dir.mkdir(exist_ok=True)
    metadata_file = metadata_dir / 'forecast_metadata.json'
    
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n✓ Metadata saved to {metadata_file}")
    print(f"  Timestamp: {metadata['timestamp']}")
    
    # Check if all succeeded
    statuses = [loc['status'] for loc in metadata['locations'].values()]
    if 'error' in statuses:
        print("\n⚠ Some forecasts failed to generate")
        return False
    
    print("\n✓ All forecasts generated successfully!")
    return True


if __name__ == '__main__':
    try:
        success = generate_all_forecasts()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"✗ Fatal error: {e}")
        sys.exit(1)
