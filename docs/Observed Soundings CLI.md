---
title: Observed Soundings CLI
---

# Observed Soundings Command Line Interface

***Globally Valid Commands***

-stid = Station ID. The station ID for the observed sounding site.

-cdir = Custom Directory (Default=None).

If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.
The default path is f:Observed Sounding/{STATION_ID_datetime.csv}. 

-cr = Clear Recycle Bin (Default=False).

For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
Setting -cr True clears your recycle bin with each run of the script. 
This ensures if any old files are moved to the recycle bin are deleted if they are not already.

--proxy = Proxy Server (Default=None).

Client assumes user is not trying to download data through a proxy server.

If you are using a proxy server you can define it by using `--proxy https://proxy-server-address:proxy-server-port`

Example: 

`wxdata-soundings fetch latest -stid okx --proxy https://proxy-server-address:proxy-server-port`

***Extra Commands For Downloading Archived Data***

-d = Datetime. The date and time of the observed sounding in the format 'YYYY-mm-dd:HH'

Example: Let's use the WxData CLI to download the observed upper-air sounding for the El Reno Tornado

*No Proxy*

`wxdata-soundings fetch archived -stid oun -d 2013-05-31:18`

*Proxy*

`wxdata-soundings fetch archived -stid oun -d 2013-05-31:18 --proxy https://proxy-server-address:proxy-server-port`
