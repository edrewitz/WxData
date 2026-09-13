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

# 4. Install the wxdata package
echo "========================================="
echo "Installing wxdata package..."
echo "========================================="
pip install git+"https://github.com/edrewitz/WxData.git"

echo "========================================="
echo "Setup complete! Environment '$ENV_NAME' is ready."
echo "To use it in your terminal, run: conda activate $ENV_NAME"
echo "========================================="

wxdata rtma rtma --model rtma --cat analysis