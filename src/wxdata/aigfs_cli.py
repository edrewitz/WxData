"""
This file hosts the WxData Command Line Interface for retrieving AI Global Forecast System (AIGFS) Data.

Command Line Use: `wxdata-aigfs **args`

(C) Eric J. Drewitz 2025-2026
"""
import click as _click
import sys as _sys
import platform as _platform
current_os = _platform.system()