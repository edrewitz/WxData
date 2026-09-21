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
# - GFS 0.25x0.25 Degree Geopotential Height at 1000mb, 850mb, 700mb, 500mb and 250mb - Source = NOMADS
# - GFS 0.25x0.25 Degree Temperature at 1000mb, 850mb, 700mb, 500mb and 250mb - Source = AWS
# - GFS 0.25x0.25 Degree Relative Humidity at 1000mb, 850mb, 700mb, 500mb and 250mb - Source = Google
#
# In this example we will sort each set of files into their own directory based on variable.
#
# **IMPORTANT**
# To prevent server rate limiting we are pulling from the different servers for each dataset.
# This is a good practice as it prevents overloading a single server with too many requests. 

wxdata-gfs 0p25 latest -v geopotential_height -l 1000 -l 850 -l 700 -l 500 -l 250 -cdir GFS0P25/Geopotential_Height & \
wxdata-gfs 0p25 latest -v temperature -l 1000 -l 850 -l 700 -l 500 -l 250 -s aws -cdir GFS0P25/Temperature & \
wxdata-gfs 0p25 latest -v relative_humidity -l 1000 -l 850 -l 700 -l 500 -l 250 -s google -cdir GFS0P25/Relative_Humidity
