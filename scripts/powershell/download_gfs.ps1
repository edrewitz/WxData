# Set the path to your Miniconda installation
$CondaPath = "C:\Users\drewi\miniconda3"

# Initialize Conda for this PowerShell session
& "$CondaPath\shell\condabin\conda-hook.ps1"

# Create the environment (Python 3.12)
conda create -n wxtest python=3.12 -y

# Activate the new environment
conda activate wxtest

# Install WxData from GitHub
pip install git+https://github.com/edrewitz/WxData.git@development

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
Start-Job -WorkingDirectory $CurrentDir -ScriptBlock { gfs 0p25 latest -v geopotential_height -l 500 }
Start-Job -WorkingDirectory $CurrentDir -ScriptBlock { gfs 0p25 latest -c secondary -v temperature -l 875 -s google }
Start-Job -WorkingDirectory $CurrentDir -ScriptBlock { gfs 0p50 latest -v temperature -l 2 -lt height_above_ground -s aws }