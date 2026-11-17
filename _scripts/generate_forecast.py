#!/usr/bin/env python
"""
Generate BOM forecast plots for multiple locations.

Usage:
    python _scripts/generate_forecast.py

Generates:
    - images/bom_forecast_katoomba.png
    - images/bom_forecast_nowra.png
    - images/bom_forecast_campbelltown.png
    - files/forecast_metadata.json (timestamp)
"""

import sys
import json
import argparse
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Add _scripts to path so we can import bom_scraper
sys.path.insert(0, str(Path(__file__).parent))

from bom_scraper import (
    scrape_bom_forecast,
    extract_forecast_data,
    prepare_forecast_data,
    get_arrow_for_direction,
    get_arrow_color,
    scrape_bom_observations,
    prepare_bom_observations
)

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerTuple
from datetime import timedelta


# BOM observation stations used alongside each forecast location
OBSERVATION_STATIONS = {
    'katoomba': {'id': '94743', 'name': 'Mount Boyce'},
    'nowra': {'id': '94750', 'name': 'Nowra'},
    'campbelltown': {'id': '94757', 'name': 'Campbelltown'},
}


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

    observations = pd.DataFrame()
    station = OBSERVATION_STATIONS.get(location)
    if station:
        observations = prepare_bom_observations(scrape_bom_observations(station['id']))
        if observations.empty:
            print(f"Warning: no complete {station['name']} observation bins are available")
    
    print("Generating plot...")
    # Create figure with 3 subplots
    fig, axes = plt.subplots(3, 1, figsize=(8.5, 8))
    title = f'7-Day Forecast for {location_name}'
    if not observations.empty:
        title = f'7-Day Forecast + 2-Day Observations for {location_name}'
    fig.suptitle(title, fontsize=16, fontweight='bold')
    
    df_valid = df.dropna(subset=['DateTime', 'Temperature_C'])
    
    # Plot 1: Temperature and Dew Point
    ax1 = axes[0]
    ax1.set_title('Temperature & Dew Point')
    ax1.set_ylabel('Temperature (°C)')
    
    df_temp_dew = df_valid.dropna(subset=['Dew_Point_C'])
    line1 = ax1.plot(df_temp_dew['DateTime'], df_temp_dew['Temperature_C'],
                     color='tab:red', marker='o', linewidth=2, label='Air temperature', markersize=5)
    line2 = ax1.plot(df_temp_dew['DateTime'], df_temp_dew['Dew_Point_C'],
                     color='tab:blue', marker='s', linewidth=2, label='Dew point', markersize=5, alpha=0.8)
    if not observations.empty:
        observed_temperature = observations.dropna(subset=['Air_Temperature_C'])
        observed_dew_point = observations.dropna(subset=['Dew_Point_C'])
        ax1.plot(observed_temperature['DateTime'], observed_temperature['Air_Temperature_C'],
                 color='tab:red', marker='.', linestyle='--', linewidth=1.5,
                 markersize=5)
        ax1.plot(observed_dew_point['DateTime'], observed_dew_point['Dew_Point_C'],
                 color='tab:blue', marker='s', linestyle='--', linewidth=1.5,
                 markersize=2.5, alpha=0.8)
    ax1.grid(True, alpha=0.3)
    
    ax1.legend(handles=line1 + line2, loc='lower right', fontsize='small')
    
    # Plot 2: Wind Speed and Direction
    ax2 = axes[1]
    ax2.set_title('Wind Speed & Direction')
    
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

    if not observations.empty:
        observed_wind = observations.dropna(subset=['Wind_Speed_kt'])
        if not observed_wind.empty:
            ax2.set_ylim(0, max(ax2.get_ylim()[1], observed_wind['Wind_Speed_kt'].max() * 1.2))
            for _, row in observed_wind.dropna(subset=['Wind_Direction']).iterrows():
                ax2.text(mdates.date2num(row['DateTime']), row['Wind_Speed_kt'],
                         get_arrow_for_direction(row['Wind_Direction']), fontsize=13,
                         ha='center', va='center', color=get_arrow_color(row['Wind_Speed_kt']),
                         weight='bold', zorder=3)
    
    # Plot 3: Rain Chance
    ax3 = axes[2]
    ax3.set_title('Rainfall')
    df_rain = df_valid.dropna(subset=['Rain_Chance_Percent'])
    if len(df_rain) > 0:
        ax3.bar(df_rain['DateTime'], df_rain['Rain_Chance_Percent'],
               width=0.08, color='steelblue', alpha=0.7, edgecolor='navy',
               label='Forecast probability')
        ax3.set_ylabel('Rain Probability (%)')
        ax3.set_ylim(0, 100)
        ax3.grid(True, alpha=0.3, axis='y')
    else:
        ax3.text(0.5, 0.5, 'No rain data', ha='center', va='center',
                transform=ax3.transAxes)

    if not observations.empty:
        observed_rain = observations.dropna(subset=['Rainfall_3h_mm'])
        amount_cols = ['Rain_50pc_mm', 'Rain_25pc_mm', 'Rain_10pc_mm']
        forecast_amounts = pd.DataFrame()
        amount_slots = pd.DataFrame()
        if all(col in df_valid.columns for col in amount_cols):
            amount_slots = df_valid.dropna(subset=amount_cols)
            forecast_amounts = amount_slots[amount_slots['Rain_10pc_mm'] > 0]
        if not amount_slots.empty:
            # Mark the 3-hour slots for which BOM provides rainfall exceedance
            # amounts (including zeros), so their absence isn't read as "no rain"
            for k, slot_time in enumerate(amount_slots['DateTime']):
                start = mdates.date2num(slot_time - timedelta(hours=1.5))
                end = mdates.date2num(slot_time + timedelta(hours=1.5))
                ax3.plot([start, end], [0.975, 0.975], transform=ax3.get_xaxis_transform(),
                         color='darkgreen', linewidth=4, solid_capstyle='butt', zorder=6)
        if not observed_rain.empty or not amount_slots.empty:
            rain_axis = ax3.twinx()
            y_max = 1.0
            if not observed_rain.empty:
                rain_axis.bar(observed_rain['DateTime'], observed_rain['Rainfall_3h_mm'],
                              width=0.08, color='tab:green', alpha=0.45,
                              label='Observed')
                y_max = max(y_max, observed_rain['Rainfall_3h_mm'].max() * 1.05)
            if not forecast_amounts.empty:
                # Line from the 50% exceedance level up to the 10% exceedance level
                x_forecast = forecast_amounts['DateTime']
                rain_axis.vlines(x_forecast, forecast_amounts['Rain_50pc_mm'],
                                 forecast_amounts['Rain_10pc_mm'],
                                 color='darkgreen', linewidth=1.2, zorder=5)
                # Cross lines at the 50% (wide) and 25% (narrow) levels; the line
                # itself simply ends at the 10% level
                for col, cap in zip(('Rain_50pc_mm', 'Rain_25pc_mm'), (7, 4)):
                    rain_axis.plot(x_forecast, forecast_amounts[col], linestyle='None',
                                   marker='_', markersize=cap, markeredgewidth=1.4,
                                   color='darkgreen', zorder=5)
                y_max = max(y_max, forecast_amounts['Rain_10pc_mm'].max() * 1.1)
            rain_axis.set_ylabel('Rainfall (mm / 3 hours)')
            rain_axis.set_ylim(0, y_max)
            forecast_handles, forecast_labels = ax3.get_legend_handles_labels()
            rain_handles, rain_labels = rain_axis.get_legend_handles_labels()
            if not amount_slots.empty:
                # One entry for both the availability bar and the exceedance glyph
                exceedance_handle = (
                    Line2D([], [], color='darkgreen', linewidth=4, solid_capstyle='butt'),
                    Line2D([], [], color='darkgreen', linewidth=1.2, marker='_',
                           markersize=8, markeredgewidth=1.4),
                )
                forecast_handles.append(exceedance_handle)
                forecast_labels.append('Forecast 50/25/10% exceedance')
            ax3.legend(forecast_handles + rain_handles, forecast_labels + rain_labels,
                       loc='upper right', fontsize='small',
                       handler_map={tuple: HandlerTuple(ndivide=None, pad=0)})

    # Add afternoon shading and format axes
    def date_formatter(x, pos=None):
        dt = mdates.num2date(x)
        if dt.hour != 12:
            return ''
        return f"{dt.strftime('%A')}\n{dt.day}/{dt.month}"
    
    date_range = df['DateTime'].dropna()
    if not observations.empty:
        date_range = pd.concat([date_range, observations['DateTime']]).dropna()
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
    
    if len(date_range) > 0:
        x_limits = (mdates.date2num(date_range.min()) - 0.1, mdates.date2num(date_range.max()) + 0.1)
        for ax in axes:
            ax.set_xlim(x_limits)

    for i, ax in enumerate(axes):
        ax.xaxis.set_major_locator(mdates.HourLocator(byhour=[12]))
        ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=[0]))
        ax.grid(True, which='minor', axis='x', alpha=0.15, linestyle='-', linewidth=0.5)
        
        if i == len(axes) - 1:
            ax.xaxis.set_major_formatter(FuncFormatter(date_formatter))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=0, ha='center')
            ax.set_xlabel('')
        else:
            ax.xaxis.set_ticklabels([])
            ax.set_xlabel('')
    
    if not observations.empty:
        # Current time marks the transition from observations to forecast
        now_local = datetime.now(ZoneInfo('Australia/Sydney')).replace(tzinfo=None)
        for ax in axes:
            ax.axvline(mdates.date2num(now_local), color='black', linestyle=':',
                       linewidth=1.5, zorder=4)
        axes[0].annotate('◄ observed', xy=(mdates.date2num(now_local), 0.94),
                         xycoords=('data', 'axes fraction'), xytext=(-4, 0),
                         textcoords='offset points', ha='right', va='top', fontsize=9, style='italic')
        axes[0].annotate('forecast ►', xy=(mdates.date2num(now_local), 0.94),
                         xycoords=('data', 'axes fraction'), xytext=(4, 0),
                         textcoords='offset points', ha='left', va='top', fontsize=9, style='italic')

    if station and not observations.empty:
        fig.text(0.5, 0.005,
                 f"Observations: BOM {station['name']} AWS (station {station['id']})",
                 ha='center', fontsize=7)
    plt.tight_layout(rect=(0, 0.025, 1, 0.96))
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    plt.close(fig)
    print(f"✓ Forecast plot saved to {output_path}")


def generate_all_forecasts():
    """
    Generate forecast plots for all configured locations.
    Also saves metadata with timestamp.
    """
    locations = [
        {'slug': 'katoomba', 'name': 'Katoomba', 'output': 'images/bom_forecast_katoomba.png'},
        {'slug': 'nowra', 'name': 'Nowra', 'output': 'images/bom_forecast_nowra.png'},
        {'slug': 'campbelltown', 'name': 'Campbelltown (Sydney)', 'output': 'images/bom_forecast_campbelltown.png'},
    ]
    
    metadata = {
        'timestamp': datetime.now(ZoneInfo('Australia/Sydney')).isoformat(),
        'timezone': 'Australia/Sydney',
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
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--katoomba-preview',
            action='store_true',
            help='Generate only the local Katoomba observations and forecast preview'
        )
        args = parser.parse_args()
        if args.katoomba_preview:
            generate_forecast_plot(output_path='_site/katoomba_observations_preview.png')
            sys.exit(0)
        success = generate_all_forecasts()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"✗ Fatal error: {e}")
        sys.exit(1)
