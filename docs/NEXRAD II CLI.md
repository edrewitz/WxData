---
title: NEXRAD II CLI
---

# NEXRAD II Radar Data Command Line Interface

NEXRAD II Radar Data Client

***Globally Valid Commands***

-sid = Site ID. The ID for the NEXRAD II Radar site.

-hr = Hours. Default=3. The amount of hours to query (hours=3 --> current to current -3 hours).

-m = Mode. Default='precipitation'. 

When in 'precipitation' mode, data querying is based on 10 scans per hour.
    
When in 'clear air' mode, data querying is based on 7 scans per hour.
           
-cdir = Custom Directory. If you want to save the files in a custom directory - enter the full path here.

-cr = Clear Recycle Bin. To clear your recycle bin with each run of the script set to True. (Default=False)

--proxy = Proxy Server (Default=None).

Client assumes user is not trying to download data through a proxy server.

If you are using a proxy server you can define it by using `--proxy https://proxy-server-address:proxy-server-port`

***Additional Required Field For Archived Data***

-st = Start Time. The time in 'YYYY-mm-dd:HH' of the last scan in the set.
    
Example: start_time='2025-08-01:18' & hours = 3 = Radar scans from 2025-08-01:15 - 2025-08-01:18.

***Example***

1) Download the latest NEXRAD II data from Upton, NY (OKX) for the past 4 hours and creates and saves the radar data in a directory called "NEXRAD_2/KOKX/Current" which is within the current working directory. 

*Linux Shell*
```shell
# Gets current Directory
current_dir=$(pwd)

# Retrieves radar data
wxdata-nexrad2 fetch latest -sid kokx -hr 4 -cdir=$current_dir/NEXRAD_2/KOKX/Current
```

*Windows Powershell*
```powershell
# Gets current Directory
$CURRENT_DIR = (Get-Location).Path

# Retrieves radar data
wxdata-nexrad2 fetch latest -sid kokx -hr 4 -cdir=$CURRENT_DIR\NEXRAD_2\KOKX\Current
```
2) Download archived NEXRAD II data from Upton, NY (OKX) for the past 4 hours starting at 2025-12-25:18 (UTC) and creates and saves the radar data in a directory called "NEXRAD_2/KOKX/Archived" which is within the current working directory. 

*Linux Shell*
```shell
# Gets current Directory
current_dir=$(pwd)

# Retrieves radar data
wxdata-nexrad2 fetch archived -st 2025-12-25:18 -sid kokx -hr 4 -cdir=$current_dir/NEXRAD_2/KOKX/Archived
```

*Windows Powershell*
```powershell
# Gets current Directory
$CURRENT_DIR = (Get-Location).Path

# Retrieves radar data
wxdata-nexrad2 fetch archived -st 2025-12-25:18 -sid kokx -hr 4 -cdir=$CURRENT_DIR\NEXRAD_2\KOKX\Archived
```

