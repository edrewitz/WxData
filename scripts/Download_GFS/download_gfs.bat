@echo off
setlocal enabledelayedexpansion

:: Define environment name
set "ENV_NAME=wx_env"

echo =========================================
echo Creating new Conda environment: %ENV_NAME%
echo =========================================

:: 1. Initialize Conda for this script session
:: Check standard Miniconda paths in the user profile or root directory
if exist "%USERPROFILE%\miniconda3\Scripts\activate.bat" (
    set "CONDA_ACTIVATE=%USERPROFILE%\miniconda3\Scripts\activate.bat"
) else if exist "C:\miniconda3\Scripts\activate.bat" (
    set "CONDA_ACTIVATE=C:\miniconda3\Scripts\activate.bat"
) else if exist "%USERPROFILE%\anaconda3\Scripts\activate.bat" (
    set "CONDA_ACTIVATE=%USERPROFILE%\anaconda3\Scripts\activate.bat"
) else (
    echo Error: Conda installation not found.
    exit /b 1
)

:: Initialize Conda by calling its activation script
call "%CONDA_ACTIVATE%"
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to initialize Conda.
    exit /b 1
)

:: 2. Create the Conda environment
call conda create -n "%ENV_NAME%" python=3.12 -y
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to create environment %ENV_NAME%.
    exit /b 1
)

:: 3. Activate the new environment
call conda activate "%ENV_NAME%"
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to activate environment %ENV_NAME%.
    exit /b 1
)

:: Remove existing package version if present
call pip uninstall wxdata -y

:: 4. Install the wxdata package
echo =========================================
echo Installing wxdata package...
echo =========================================
call pip install git+"https://github.com/edrewitz/WxData.git@development"
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to install wxdata package.
    exit /b 1
)

echo =========================================
echo Setup complete! Environment '%ENV_NAME%' is ready.
echo To use it in your terminal, run: conda activate %ENV_NAME%
echo =========================================

:: Downloads the following datasets concurrently (in parallel)
:: In Windows Batch, the 'start' command runs tasks in a separate background window.
:: '/b' forces them to run in the background within the same console session.

start "" /b wxdata-gfs 0p25 latest -v geopotential_height -v temperature -v relative_humidity -v u-component_of_wind -v v-component_of_wind -l 1000 -l 850 -l 700 -l 500 -l 250

start "" /b wxdata-gfs 0p25 latest -c secondary -v geopotential_height -v temperature -v relative_humidity -v u-component_of_wind -v v-component_of_wind -l 875 -l 775 -l 675 -l 575 -l 475 -s google

start "" /b wxdata-gfs 0p50 latest -v temperature -v relative_humidity -l 2 -lt height_above_ground -s aws

echo Concurrent GFS downloads initiated in the background...