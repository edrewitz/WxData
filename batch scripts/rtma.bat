@echo off
:: Replace this with the directory your miniconda3 activate.bat file lives in
SET CONDA_PATH=C:\Users\drewi\miniconda3\Scripts

:: Initialize Conda for this script execution
call %CONDA_PATH%\activate.bat %CONDA_PATH%

:: Create the environment
call conda create -n wxdtest python=3.12 -y

:: Activate the environment
call conda activate wxdtest

::pip uninstall wxdata -y
:: Install and run WxData
pip install git+"https://github.com/edrewitz/WxData.git@development"

model rtma fetch --region conus --cat analysis