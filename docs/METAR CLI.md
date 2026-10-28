---
title: METAR CLI
---

# METAR Observations Command Line Interface

METAR Observations Soundings Client

***Valid Commands***

-cr = Clear Recycle Bin (Default=False).

For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
Setting -cr True clears your recycle bin with each run of the script. 
This ensures if any old files are moved to the recycle bin are deleted if they are not already.

--proxy = Proxy Server (Default=None).

Client assumes user is not trying to download data through a proxy server.

If you are using a proxy server you can define it by using `--proxy https://proxy-server-address:proxy-server-port`

**Example** 

`wxdata-metars fetch latest --proxy https://proxy-server-address:proxy-server-port`
