# 1. Check if the script is already running in PowerShell 7+
if ($PSVersionTable.PSVersion.Major -lt 7) {
    Write-Host "Running in legacy PowerShell $($PSVersionTable.PSVersion.Major). Checking for PowerShell 7..." -ForegroundColor Yellow

    # 2. Check if PowerShell 7 is already installed but not being used
    $pwshPath = Get-Command pwsh.exe -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
    if (-not $pwshPath) {
        # Search common default installation paths if it's not in the PATH environment variable yet
        $defaultPath = "$env:ProgramFiles\PowerShell\7\pwsh.exe"
        if (Test-Path $defaultPath) { $pwshPath = $defaultPath }
    }

    # 3. If PowerShell 7 is not found, install it silently via Winget (or Microsoft's web installer)
    if (-not $pwshPath) {
        Write-Host "PowerShell 7 not found. Starting silent installation..." -ForegroundColor Cyan
        
        # Using winget (Recommended for Windows 10/11)
        winget install --id Microsoft.PowerShell --source winget --silent --accept-source-agreements --accept-package-agreements
        
        # Fallback if winget is unavailable (e.g., Windows Server without Desktop Experience)
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Winget failed or unavailable. Falling back to MSI web installer..." -ForegroundColor Yellow
            Invoke-Expression "& { $(Invoke-RestMethod https://aka.ms) } -UseMSI -Quiet"
        }

        # Refresh path environment variable to find the newly installed pwsh.exe
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        $pwshPath = "$env:ProgramFiles\PowerShell\7\pwsh.exe"
    }

    # 4. Relaunch this exact script inside PowerShell 7 and exit the current PS5 session
    if (Test-Path $pwshPath) {
        Write-Host "Relaunching script inside PowerShell 7..." -ForegroundColor Green
        & $pwshPath -File $PSCommandPath $args
        Exit $LASTEXITCODE
    } else {
        Write-Error "Failed to install or locate PowerShell 7."
        Exit 1
    }
}

# ==============================================================================
# YOUR ACTUAL POWERSHELL 7+ CODE GOES HERE
# ==============================================================================
Write-Host "Success! The script is now running inside PowerShell v$($PSVersionTable.PSVersion.Major)." -ForegroundColor Green

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

# Gets our current directory
$CURRENT_DIR = Get-Location

# Sets our working directory
$WORKING_DIR = "$CURRENT_DIR/scripts/Download_GFS"

wxdata-gfs 0p25 latest -v geopotential_height -v temperature -v relative_humidity -v u-component_of_wind -v v-component_of_wind -l 1000 -l 850 -l 700 -l 500 -l 250 -cdir $WORKING_DIR/GFS0P25/Primary
wxdata-gfs 0p25 latest -c secondary -v geopotential_height -v temperature -v relative_humidity -v u-component_of_wind -v v-component_of_wind -l 875 -l 775 -l 675 -l 575 -l 475 -s google -cdir $WORKING_DIR/GFS0P25/Secondary
wxdata-gfs 0p50 latest -v temperature -v relative_humidity -l 2 -lt height_above_ground -s aws -cdir $WORKING_DIR/GFS0P50

Write-Output "All downloads completed successfully."