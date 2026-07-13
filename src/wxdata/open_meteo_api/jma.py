"""
This file hosts the interface for the Open-Meteo API for JMA data.

(C) Eric J. Drewitz 2025-2026
"""
import requests as _requests
from wxdata.open_meteo_api.utils import(
    json_to_pandas as _json_to_pandas,
    server_response as _server_response,
    df_to_csv as _df_to_csv
)



