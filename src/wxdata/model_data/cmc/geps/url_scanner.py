"""
This file hosts the URL Scanner for the GEPS

(C) Eric J. Drewitz 2025-2026
"""
import requests
import sys
import time
import wxdata.model_data.cmc.utils._exceptions as _exceptions

from wxdata.model_data.cmc.utils.filenames import get_filenames
# Exception handling for Python >= 3.13 and Python < 3.13
try:
    from datetime import datetime, timedelta, UTC
except Exception as e:
    from datetime import datetime, timedelta

# Gets current time in UTC
try:
    now = datetime.now(UTC)
except Exception as e:
    now = datetime.utcnow()

# Gets local time
local = datetime.now()

# Gets yesterday's date
yd = now - timedelta(days=1)

