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

***Additional Required Field For Archived Data***

-st = Start Time. The time in 'YYYY-mm-dd:HH' of the last scan in the set.
    
Example: start_time='2025-08-01:18' & hours = 3 = Radar scans from 2025-08-01:15 - 2025-08-01:18.

