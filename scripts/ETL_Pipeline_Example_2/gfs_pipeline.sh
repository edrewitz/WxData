#!/bin/bash

# In this script we will perform the following tasks:
# 1) Create a conda environment called gfs_pipeline
# 2) Activate our conda environment called gfs_pipeline
# 3) Install the WxData Python package from conda-forge
# 4) Execute our Python wrapper script that holds our downstream processes

# Downstream Processes in Python Scripts
# 1) Download the GFS0P25 850mb Temperature Forecast from NCEP/NOMADS
# 2) Create a set of forecast graphics for the GFS0P25 850mb Temperature

# This script was written by Eric J. Drewitz

# Exit immediately if a command exits with a non-zero status
set -e

# Define environment name
ENV_NAME="gfs_pipeline"

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

# 4. Install the wxdata package from conda-forge
echo "========================================="
echo "Installing wxdata package..."
echo "========================================="
conda install -c conda-forge -n gfs_pipeline -y wxdata

echo "========================================="
echo "Setup complete! Environment '$ENV_NAME' is ready."
echo "To use it in your terminal, run: conda activate $ENV_NAME"
echo "========================================="

# Executing the Python wrapper to start the process
python wrapper.py