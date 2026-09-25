#!/usr/bin/env python3

# This script creates a set of GFS 0.25x0.25 850mb Temperature Forecast [°C] across CONUS and Southern Canada
# This script processes and plots the GFS0P25 850mb Temperature Forecast data downloaded using the WxData CLI in the shell script automate_gfs.sh
# The shell script automate_gfs.sh executes this Python script gfs_graphics.py in our environment created in that shell script after the download completes

# This script was written by Eric J. Drewitz

###############
### IMPORTS ###
###############

import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import pandas as pd
import metpy.calc as mpcalc

from wxdata import gfs_post_processing
from datetime import datetime, timedelta, UTC

# Extract the current time in UTC
now = datetime.now(UTC)

# Set all of our text to bold using matplotlib rcParams
mpl.rcParams['font.weight'] = 'bold'

# Create our graphics directory
os.makedirs(f"GFS 850mb Temperature Forecast", exist_ok=True)

# Defines our directory where the data is stored
path_to_data = f"GFS0P25/Temperature"

# Ingest our data
# This set of graphics will focus on CONUS and southern Canada (I'm based in CONUS)
# Western Bound = -130 (130°W)
# Eastern Bound = -65 (65°W)
# Southern Bound = 20 (20°N)
# Northern Bound = 60 (60°N)

western_bound = -130
eastern_bound = -65
southern_bound = 20
northern_bound = 60

ds = gfs_post_processing.primary_gfs_post_processing(path_to_data,
                                                        western_bound,
                                                        eastern_bound,
                                                        southern_bound,
                                                        northern_bound)

# Create our figure
for i in range(0, len(ds['step']), 1):
    fig = plt.figure(figsize=(12,12))
    
    # Create our subplot with a PlateCarree (lat/lon) projection
    ax = fig.add_subplot(1,1,1, projection=ccrs.PlateCarree())
    
    # Set our boundaries in a latlon format of [western_bound, eastern_bound, southern_bound, northern_bound] followed by our PlateCarree projection
    ax.set_extent([-130, -65, 20, 60], ccrs.PlateCarree())
    
    # Add our features to the map 
    # Add our coastlines
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=3)
    
    # Add the oceans, land, states, lakes and Canadian provinces and color them light cyan
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAND, color='navajowhite', zorder=1)
    ax.add_feature(cfeature.STATES, edgecolor='black', linewidth=0.5, zorder=5)
    province_boundaries = cfeature.NaturalEarthFeature(
        category="cultural",
        name="admin_1_states_provinces_lines",
        scale="50m",
        facecolor="none",
        edgecolor="black",
    )
    ax.add_feature(province_boundaries, linewidth=0.5, zorder=5)
    
    # Add our 850mb temperature contours converted to Celsius from Kelvin
    # Let's also apply smooth_gaussian() from metpy.calc to smooth our contour lines
    c = ax.contour(ds['longitude'], 
                   ds['latitude'], 
                   (mpcalc.smooth_gaussian(ds['temperature'][i, :, :] - 273.15, n=8)), 
                   levels=np.arange(-10, 35, 5), 
                   transform=ccrs.PlateCarree(), 
                   colors='black', 
                   linewidths=0.75)
    
    ax.clabel(c, fontsize=6, inline=True)
    # Add our filled contours for 850mb temperature converted to Celsius from Kelvin
    cs = ax.contourf(ds['longitude'], 
                   ds['latitude'], 
                   (ds['temperature'][i, :, :] - 273.15), 
                   levels=np.arange(-10, 31, 1), 
                   transform=ccrs.PlateCarree(),
                   alpha=0.25,
                   cmap='jet',
                   extend='both')
    
    # Create our colorbar for our filled contours
    fig.colorbar(cs, 
                 shrink=0.5, 
                 pad=0.01,
                 ticks=np.arange(-10, 35, 5))
    

    # Plot title
    plt.title(f"GFS0P25 850 MB TEMPERATURE [°C]", 
                   fontsize=10, 
                   fontweight='bold',
                   bbox=dict(boxstyle='round', 
                                facecolor='bisque'),
                   loc='left')
    
    # Extract our valid time as a datetime object
    valid_time = pd.to_datetime(ds['valid_time'].values)
    
    # Gets our new forecast hour (eventhough we are plotting the initial frame)
    times = ds['step'].values
    forecast_time = valid_time + timedelta(hours=int(times[i]))
    
    # Secondary title for our model runtime
    plt.title(f"Forecast Valid: {forecast_time.strftime('%m/%d/%Y %H:00')} (t+{int(times[i])} HR)\nModel Initialization: {valid_time.strftime('%m/%d/%Y %H:00')} UTC", 
                    fontsize=7, 
                    fontweight='bold',
                    bbox=dict(boxstyle='round', 
                                facecolor='bisque'),
                    loc='right')
    
    # Adding my signature on the plot
    ax.text(0, 
            -0.001, 
            f"Plot Created by Eric J. Drewitz at {now.strftime('%m/%d %H:%M')} UTC - Powered by WxData", 
            transform=ax.transAxes, 
            fontsize=6, 
            fontweight='bold', 
            bbox=dict(boxstyle='round', 
                    facecolor='bisque'))
    
    # Names our file for the forecast hour frame
    filename = f"{forecast_time.strftime('%m%d%Y%H')}.png"
    
    # Saves our frame to our graphics directory
    fig.savefig(f"GFS 850mb Temperature Forecast/{filename}", bbox_inches='tight')
    
print("GFS0P25 850MB Temperature Forecast Graphics Saved To: f:GFS 850mb Temperature Forecast/")




