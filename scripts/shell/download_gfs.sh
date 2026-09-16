#!/bin/bash

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

# Downloads the following datasets concurrently
# - GFS 0.25x0.25 Degree Primary Variables & Levels: 500mb Geopotential Height
# - GFS 0.25x0.25 Degree Secondary Variables & Levels: 875mb Temperature
# - GFS 0.50x0.50 Degree 2-Meter Temperature
#
# **IMPORTANT**
# To prevent server rate limiting we are pulling from the different servers for each dataset
# - GFS 0.25x0.25 Degree Primary Variables & Levels: NCEP/NOMADS
# - GFS 0.25x0.25 Degree Secondary Variables & Levels: Google Cloud
# - GFS 0.50x0.50 Degree 2-Meter Temperature: Amazon Web Services (AWS)
gfs 0p25 latest -v geopotential_height -l 500 & \
gfs 0p25 latest -c secondary -v temperature -l 875 -s google & \
gfs 0p50 latest -v temperature -l 2 -lt height_above_ground -s aws
