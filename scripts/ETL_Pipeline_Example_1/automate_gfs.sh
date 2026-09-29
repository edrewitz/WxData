#!/bin/bash

# This script uses the CLI found in the WxData Python package to download the GFS 0.25x0.25 850mb Temperature Forecast from Amazon Web Services.
# As soon as the GFS download completes, a Python script gfs_graphics.py will run and ingest our data and create a series of forecast graphics.

# This script was written by Eric J. Drewitz

# Exit immediately if a command exits with a non-zero status
set -e

# Define environment name
ENV_NAME="wx_env"

echo "========================================="
echo "Creating new Conda environment: $ENV_NAME"
echo "========================================="

# 1. Initialize Conda for this script session
# This replicates how conda init injects conda commands into your shell
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/anaconda3/etc/profile.d/conda.sh"
else
    echo "Error: Conda installation not found in your home directory."
    exit 1
fi

# 2. Create the Conda environment
conda create -n "$ENV_NAME" python=3.12 -y

# 3. Activate the new environment
conda activate "$ENV_NAME"

pip uninstall wxdata

# 4. Install the wxdata package
echo "========================================="
echo "Installing wxdata package..."
echo "========================================="
pip install git+"https://github.com/edrewitz/WxData.git@development"

echo "========================================="
echo "Setup complete! Environment '$ENV_NAME' is ready."
echo "To use it in your terminal, run: conda activate $ENV_NAME"
echo "========================================="

# The following processes include

# 1 - Downloading the latest GFS 0.25x0.25 Degree 850mb Temperature Forecast to GFS0P25/Temperature
wxdata-gfs 0p25 latest -v temperature -l 850 -s aws -cdir GFS0P25/Temperature

# 2 - Executing a Python script that ingests the data and creates a set of forecast graphics
python gfs_graphics.py