#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status

# Define environment name
ENV_NAME="testwxx"
SCRIPT_PATH="/c/Users/drewi/WxData/test/run_wxdata.py"

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
conda create -n "$ENV_NAME" python=3.14 -y

# 3. Activate the new environment
conda activate "$ENV_NAME"

# 3. Install the package into your environment (e.g., 'myenv')
conda install -y -n testwxx wxdata

# Execute the Python script directly inside the environment
conda run -n "$ENV_NAME" python "$SCRIPT_PATH"