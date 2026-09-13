# Set the path to your Miniconda installation
$CondaPath = "C:\Users\drewi\miniconda3"

# Initialize Conda for this PowerShell session
& "$CondaPath\shell\condabin\conda-hook.ps1"

# Create the environment (Python 3.12)
conda create -n wxtest python=3.12 -y

# Activate the new environment
conda activate wxtest

# Install WxData from GitHub
pip install git+https://github.com/edrewitz/WxData.git

# Run the WxData command
wxdata rtma rtma --model rtma --cat analysis