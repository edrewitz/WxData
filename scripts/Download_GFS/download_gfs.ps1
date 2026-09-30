# Stop execution on any error (equivalent to set -e)
$ErrorActionPreference = "Stop"

# Define environment name
$ENV_NAME = "wx_env"

Write-Output "========================================="
Write-Output "Creating new Conda environment: $ENV_NAME"
Write-Output "========================================="

# 1. Initialize Conda for this script session
$condaPath = Get-Command conda -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
if ($condaPath) {
    # Dynamically find the profiles script folder relative to the conda executable
    $condaDir = Split-Path (Split-Path $condaPath -Parent) -Parent
    $profileScript = Join-Path $condaDir "shell\condabin\conda-hook.ps1"
    if (Test-Path $profileScript) {
        & $profileScript
    }
} else {
    # Fallback to standard home directory paths if not in system environment variables
    $homeDir = $HOME
    $possiblePaths = @(
        "$homeDir\miniconda3\shell\condabin\conda-hook.ps1",
        "$homeDir\anaconda3\shell\condabin\conda-hook.ps1"
    )
    $initialized = $false
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            & $path
            $initialized = $true
            break
        }
    }
    if (-not $initialized) {
        Write-Error "Error: Conda installation not found."
        Exit 1
    }
}

# 2. Create the Conda environment
conda create -n $ENV_NAME python=3.12 -y

# 3. Activate the new environment
conda activate $ENV_NAME

# Suppress errors if pip uninstall fails because the package isn't there yet
try {
    pip uninstall wxdata -y
} catch {
    # Package wasn't installed, safe to ignore
}

# 4. Install the wxdata package
Write-Output "========================================="
Write-Output "Installing wxdata package..."
Write-Output "========================================="
pip install git+"https://github.com/edrewitz/WxData.git@development"

Write-Output "========================================="
Write-Output "Setup complete! Environment '$ENV_NAME' is ready."
Write-Output "To use it in your terminal, run: conda activate $ENV_NAME"
Write-Output "========================================="

wxdata-gfs 0p25 latest -v geopotential_height -v temperature -v relative_humidity -v u-component_of_wind -v v-component_of_wind -l 1000 -l 850 -l 700 -l 500 -l 250
wxdata-gfs 0p25 latest -c secondary -v geopotential_height -v temperature -v relative_humidity -v u-component_of_wind -v v-component_of_wind -l 875 -l 775 -l 675 -l 575 -l 475 -s google
wxdata-gfs 0p50 latest -v temperature -v relative_humidity -l 2 -lt height_above_ground -s aws 

Write-Output "All downloads completed successfully."