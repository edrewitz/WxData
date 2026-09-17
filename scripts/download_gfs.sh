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

# Downloads the following datasets concurrently (in parallel)
# - GFS 0.25x0.25 Degree Primary Variables & Levels
# - GFS 0.25x0.25 Degree Secondary Variables & Levels
# - GFS 0.50x0.50 Degree
#
# **IMPORTANT**
# To prevent server rate limiting we are pulling from the different servers for each dataset.
# This is a good practice as it prevents overloading a single server with too many requests. 
# - GFS 0.25x0.25 Degree Primary Variables & Levels: NCEP/NOMADS.
# - GFS 0.25x0.25 Degree Secondary Variables & Levels: Google Cloud.
# - GFS 0.50x0.50 Degree: Amazon Web Services (AWS).
#
# We will download the following variables at the following levels for the GFS
# - GFS 0.25x0.25 Degree Primary: Geopotential Height, Temperature, u & v Wind Components, Relative Humidity at 1000mb, 850mb, 700mb, 500mb and 250mb.
# - GFS 0.25x0.25 Degree Secondary: Geopotential Height, Temperature, u & v Wind Components, Relative Humidity at 875mb, 775mb, 675mb, 575mb and 475mb.
# - GFS 0.50x0.50 Degree: Temperature, Relative Humidity at 2-meters above ground. 

gfs 0p25 latest -v geopotential_height -v temperature -v relative_humidity -v u-component_of_wind -v v-component_of_wind -l 1000 -l 850 -l 700 -l 500 -l 250 & \
gfs 0p25 latest -c secondary -v geopotential_height -v temperature -v relative_humidity -v u-component_of_wind -v v-component_of_wind \
 -l 875 -l 775 -l 675 -l 575 -l 475 -s google & \
gfs 0p50 latest -v temperature -v relative_humidity -l 2 -lt height_above_ground -s aws
