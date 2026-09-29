# This script uses the CLI found in the WxData Python package to download the GFS 0.25x0.25 850mb Temperature Forecast from Amazon Web Services.
# As soon as the GFS download completes, a Python script gfs_graphics.py will run and ingest our data and create a series of forecast graphics.

# This script was written by Eric J. Drewitz

# Define our conda environment name & Python version for our conda environment
$EnvName = "wx_test"
$PythonVersion = "3.12"

# Dynamically construct the path to the environment's Python executable
$CondaHome = "$env:USERPROFILE\miniconda3" # Change to "anaconda3" if using full Anaconda
$CondaExe = "$CondaHome\Scripts\conda.exe"
if (-not (Test-Path $CondaHome)) {
    # Fallback/Check if Conda is in the standard ProgramData location
    $CondaHome = "$env:ALLUSERSPROFILE\miniconda3"
}

# Define our Python environment path for when we run Python scripts
$TargetPython = "$CondaHome\envs\$EnvName\python.exe"

Write-Host "--- Initializing Environment Pipeline ---" -ForegroundColor Cyan

# Create the Conda environment (if it doesn't already exist)
Write-Host "--- Initializing Environment Pipeline ---" -ForegroundColor Cyan

# Create the Conda environment using the absolute path to conda.exe
if (-not (Test-Path $TargetPython)) {
    Write-Host "Creating conda environment '$EnvName' with Python $PythonVersion..." -ForegroundColor Yellow
    
    # Use the call operator (&) with the full path to conda.exe
    & $CondaExe create --name $EnvName python=$PythonVersion -y
} else {
    Write-Host "Conda environment '$EnvName' already exists." -ForegroundColor Green
}


# Pip install the package using the targeted environment's Python/pip
Write-Host "Installing wxdata via pip..." -ForegroundColor Yellow
& $TargetPython -m pip install git+"https://github.com/edrewitz/WxData.git@development"

# Downloading the latest GFS 0.25x0.25 Degree for 850mb temperature to the folder: GFS0P25/Temperature
wxdata-gfs 0p25 latest -v temperature -l 850 -s aws -cdir GFS0P25/Temperature

# Run your Python scripts explicitly targeting the environment's binary
Write-Host "Running Python scripts..." -ForegroundColor Green

# Example 1: Running our script to create our GFS 850mb forecast graphics
& $TargetPython "C:\Users\drewi\WxData\scripts\ETL_Pipeline_Example_1\gfs_graphics.py"

Write-Host "--- Pipeline Execution Completed ---" -ForegroundColor Cyan