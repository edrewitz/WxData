#!/usr/bin/env python3

"""
This is a Python wrapper script that will be executed by the shell script to perform the following:

1) Download the latest GFS0P25 data
2) Create a set of forecast graphics for the GFS0P25 850mb Temperature Forecast

This script is written by Eric J. Drewitz
"""
import os
from wxdata import run_external_scripts

# Get the absolute directory where this python script lives
# This is necessary for automating Python scripts via Windows Powershell
script_dir = os.path.dirname(os.path.abspath(__file__))

# Runs our two processes to (1) Download the data & (2) Plot the data in the order they are listed
run_external_scripts([f"{script_dir}/download_gfs.py",
                      f"{script_dir}/gfs_graphics.py"])