"""
This file hosts the regression tests for the archived NOAA CFS URL scanners.

The archived CFS client downloads two different products from the NOAA CFS
archive on AWS:

    - CFS Flux     -> the 'flxf' objects
    - CFS Pressure -> the 'pgbf' objects

The URL scanner returns the local file name that the downloaded GRIB2 file is
saved as. That local file name must match the name of the object that is
actually downloaded, otherwise the Flux and Pressure products cannot be told
apart on disk and they overwrite each other when they share a directory.

(C) Eric J. Drewitz 2025-2026
"""

import importlib.util
from pathlib import Path
from urllib.parse import urlparse

import pytest

MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "wxdata"
    / "archived_data"
    / "model_data"
    / "noaa"
    / "cfs"
    / "url_scanner.py"
)


def _load_url_scanner():
    """
    Loads the archived CFS URL scanner module.

    The module is loaded directly from its file so that these tests do not
    require the full WxData dependency stack (xarray, cartopy, cfgrib, ...).
    The URL scanner itself only depends on 'requests'.
    """

    spec = importlib.util.spec_from_file_location(
        "wxdata_archived_cfs_url_scanner",
        MODULE_PATH
    )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


url_scanner = _load_url_scanner()


class _FakeResponse:
    """
    A stand-in for a requests response that reports a successful download.
    """

    status_code = 200

    def close(self):
        pass


@pytest.fixture
def fake_server(monkeypatch):
    """
    Serves a successful response for every request so that the scanners do
    not exit the process when they look for the data.
    """

    def _fake_get(url, *args, **kwargs):
        return _FakeResponse()

    monkeypatch.setattr(url_scanner.requests, "get", _fake_get)

    return _fake_get


def _basename(url):
    """
    Returns the file name of the object that the URL points to.
    """

    return urlparse(url).path.rsplit("/", 1)[-1]


@pytest.mark.parametrize("run", [0, 6, 12, 18])
def test_pressure_scanner_saves_files_under_the_downloaded_name(fake_server, run):
    """
    The CFS Pressure files must be saved under the same name that is
    downloaded from the NOAA CFS archive.
    """

    urls, files, idx_urls = url_scanner.cfs_pressure_url_scanner(
        date="2024-01-01",
        run=run,
        final_forecast_hour=24,
        proxies=None
    )

    assert len(urls) == len(files) == len(idx_urls)

    for url, idx_url, filename in zip(urls, idx_urls, files):
        assert filename == _basename(url)
        assert filename == _basename(idx_url).removesuffix(".idx")


def test_pressure_scanner_uses_the_pressure_product_prefix(fake_server):
    """
    The CFS Pressure product is the 'pgbf' object on the NOAA CFS archive.
    """

    urls, files, idx_urls = url_scanner.cfs_pressure_url_scanner(
        date="2024-01-01",
        run=0,
        final_forecast_hour=24,
        proxies=None
    )

    for url, idx_url, filename in zip(urls, idx_urls, files):
        assert filename.startswith("pgbf")
        assert "/pgbf" in url
        assert "/pgbf" in idx_url


@pytest.mark.parametrize("run", [0, 6, 12, 18])
def test_flux_scanner_saves_files_under_the_downloaded_name(fake_server, run):
    """
    The CFS Flux files must be saved under the same name that is downloaded
    from the NOAA CFS archive.
    """

    urls, files, idx_urls = url_scanner.cfs_flux_url_scanner(
        date="2024-01-01",
        run=run,
        final_forecast_hour=24,
        proxies=None
    )

    assert len(urls) == len(files) == len(idx_urls)

    for url, idx_url, filename in zip(urls, idx_urls, files):
        assert filename == _basename(url)
        assert filename == _basename(idx_url).removesuffix(".idx")
        assert filename.startswith("flxf")


def test_flux_and_pressure_files_do_not_collide(fake_server):
    """
    The Flux and Pressure products must not be saved under the same file
    name, otherwise one product overwrites the other when they are
    downloaded into the same directory.
    """

    _, flux_files, _ = url_scanner.cfs_flux_url_scanner(
        date="2024-01-01",
        run=0,
        final_forecast_hour=24,
        proxies=None
    )

    _, pressure_files, _ = url_scanner.cfs_pressure_url_scanner(
        date="2024-01-01",
        run=0,
        final_forecast_hour=24,
        proxies=None
    )

    assert set(flux_files).isdisjoint(set(pressure_files))
