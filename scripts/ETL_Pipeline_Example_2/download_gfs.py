#!/usr/bin/env python3

# This script uses WxData to download the GFS0P25 850mb Temperature Forecast Data from NCEP/NOMADS

# This script is written by Eric J. Drewitz

import os
from wxdata import gfs_0p25

# Get the absolute directory where this python script lives
# This is necessary for automating Python scripts via Windows Powershell
script_dir = os.path.dirname(os.path.abspath(__file__))

gfs_0p25(process_data=False,
         variables=['temperature'],
         levels=[850],
         custom_directory=f"{script_dir}/GFS0P25/Temperature/850")