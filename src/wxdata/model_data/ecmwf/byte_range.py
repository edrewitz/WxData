"""
This file has the core client for the European Centre for Medium-Range Weather Forecasts (ECMWF) Data.

(C) Eric J. Drewitz 2025-2026
"""
from __future__ import annotations

import json
import requests
import sys
import os

from time import sleep
from tqdm.auto import tqdm
from wxdata.model_data.ecmwf.validate import validate_file


def byte_range(record):
    """
    Convert ECMWF offset/length into HTTP range.
    """

    start = record["_offset"]
    end = start + record["_length"] - 1

    return start, end

def create_download_progress_bar(
    records,
    desc="Downloading",
):
    """
    Create a byte-based download progress bar.

    Required Arguments:
    1) records : list[dict]
        ECMWF index records containing '_length'.
        
    Optional Arguments:
    1) desc : str
        Progress bar label.
        
    Returns
    -------
    
    A tqdm progress bar. 
    """

    total_bytes = sum(
        rec["_length"]
        for rec in records
    )

    return tqdm(
        total=total_bytes,
        desc=desc,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        dynamic_ncols=True,
        leave=False,
    )
    
    
def aifs_load_index(
                     index_url,
                     proxies
                     ):
    
    """
    This function loads JSON Index File.
    
    Required Arguments:
    
    1) index_url (String) - The URL of the index file.
    
    2) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    Optional Arguments: None
    
    Returns
    -------
    
    All records in the JSON Index File.     
    """
    if proxies == None:
        response = requests.get(index_url, 
                                timeout=60)
    else:
        response = requests.get(index_url, 
                                timeout=60,
                                proxies=proxies)

    text = response.text.lstrip("\ufeff").strip()

    if not text:
        raise RuntimeError(
            f"ECMWF returned an empty index response: {index_url}"
        )

    if not text.startswith("{"):
        raise RuntimeError(
            "ECMWF index response is not JSON Lines.\n"
            f"Content-Type: {response.headers.get('Content-Type')!r}\n"
            f"First 200 characters: {text[:200]!r}"
        )

    records = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        line = line.strip()

        if not line:
            continue

        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Invalid index record on line {line_number}: "
                f"{line[:200]!r}"
            ) from exc

    return records


def load_index(
               index_url,
               proxies
               ):
    """
    This function loads JSON Index File.
    
    Required Arguments:
    
    1) index_url (String) - The URL of the index file.
    
    2) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    Optional Arguments: None
    
    Returns
    -------
    
    All records in the JSON Index File.     
    """

    if proxies == None:
        try:
            r = requests.get(index_url, 
                             timeout=60)
        except Exception as e:
            for i in range(0, 10, 1):
                print(f"Error: Connection Disrupted.\nWaiting 30 seconds and trying again...")
                sleep(30)
                try:
                    r = requests.get(index_url, 
                                        timeout=60)
                    break
                except Exception as e:
                    i = i
                    if i >= 9:
                        print(f"Error: Client unable to reconnect. - System Exit.")
                        sys.exit(1)
    else:
        try:
            r = requests.get(index_url, 
                             timeout=60,
                             proxies=proxies)
        except Exception as e:
            for i in range(0, 10, 1):
                print(f"Error: Connection Disrupted.\nWaiting 30 seconds and trying again...")
                sleep(30)
                try:
                    r = requests.get(index_url, 
                                        timeout=60,
                                        proxies=proxies)
                    break
                except Exception as e:
                    i = i
                    if i >= 9:
                        print(f"Error: Client unable to reconnect. - System Exit.")
                        sys.exit(1)

    records = []
    for line in r.text.splitlines():
        line = line.strip()
        if line:
            records.append(json.loads(line))
            
    return records


def select_records(
    records,
    levtype=None,
    levels=None,
    params=None,
    members=None,
):
    
    """
    This function queries the records to extract the various byte-ranges.
    
    Required Arguments: 
    
    1) records (List) - All records in the JSON Index File.
    
    Optional Arguments:
    
    1) levtype (String) - The level type.
    
        ***Level Types***
    
        i) pl - pressure
        
        ii) sfc - surface
        
        iii) soil - depth below ground
    
    2) levels (Integer List) - The list of levels in a level type. 
    
    3) params (String List) - The list of parameters.
    
    4) members (Integer List) - [For ensembles only]: The list of ensemble members. 
    
    Returns
    -------
    
    The byte-ranges for the requested data. 
    """
    selected = records

    if levtype is not None:
        selected = [
            r for r in selected
            if r.get("levtype") == levtype
        ]

    if levels is not None:
        levels = {str(l) for l in levels}

        selected = [
            r for r in selected
            if str(r.get("levelist")) in levels
        ]

    if params is not None:
        params = set(params)

        selected = [
            r for r in selected
            if r.get("param") in params
        ]

    if members is not None:
        members = {str(m) for m in members}

        selected = [
            r for r in selected
            if str(r.get("number")) in members
        ]

    return selected

def download_messages(
    grib_url,
    records,
    output_path,
    output_filename,
    proxies
):
    
    """
    This function downloads the GRIB messages for the queried records.
    
    Required Arguments:
    
    1) grib_url (String) - The URL of the GRIB file that will be downloaded.
    
    2) records (List) - The list of valid byte-ranges. 
    
    3) output_path (String) - The local directory for the ECMWF data files.
    
    4) output_filename (String) - The filename of the output file.
    
    5) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    Optional Arguments: None
    
    Returns
    -------
    
    Queried files downloaded to directory {output_path}
    """

    os.makedirs(output_path, exist_ok=True)

    MAX_RETRIES = 20
    RETRY_WAIT = 90
    CHUNK_SIZE = 1024 * 1024

    with open(f"{output_path}/{output_filename}", "wb") as fout:

        with create_download_progress_bar(
            records,
            desc=output_filename
        ) as pbar:

            for rec in records:

                start = rec["_offset"]
                expected_bytes = rec["_length"]
                end = start + expected_bytes - 1

                headers = {
                    "Range": f"bytes={start}-{end}"
                }

                success = False

                for attempt in range(1, MAX_RETRIES + 1):

                    try:

                        if proxies == None:
                            r = requests.get(
                                grib_url,
                                headers=headers,
                                stream=True,
                                timeout=500
                            )
                        else:
                            r = requests.get(
                                grib_url,
                                headers=headers,
                                stream=True,
                                timeout=500,
                                proxies=proxies
                            )

                        r.raise_for_status()

                        data = bytearray()

                        for chunk in r.iter_content(
                            chunk_size=CHUNK_SIZE
                        ):

                            if chunk:
                                data.extend(chunk)

                        bytes_received = len(data)

                        if bytes_received != expected_bytes:
                            raise IOError(
                                f"Incomplete byte range "
                                f"({bytes_received:,}/{expected_bytes:,} bytes)"
                            )

                        fout.write(data)
                        pbar.update(bytes_received)

                        success = True
                        break

                    except Exception as e:

                        if attempt < MAX_RETRIES:

                            sleep(RETRY_WAIT)

                        else:

                            print(
                                f"\nERROR: Unable to download "
                                f"range {start}-{end} after "
                                f"{MAX_RETRIES} attempts."
                            )

                            sys.exit(1)

                if not success:
                    sys.exit(1)
                                                
                        
def download_ecmwf_data(grib_url,
                        index_url,
                        level_type,
                        levels,
                        variables,
                        members,
                        proxies,
                        output_path,
                        output_filename):
    
    """
    This function is the core of the client that downloads the ECMWF data.
    
    Required Arguments:
    
    1) grib_url (String) - The URL of the GRIB file that will be downloaded.
    
    2) records (List) - The list of valid byte-ranges. 
    
    3) level_type (String) - The type of level the variable is on.
    
    4) levels (Integer List or None) - The list of valid levels for a specific level_type.
    
    5) variables (String List) - The list of variables.
    
    6) members (Integer List or None) - List of ensemble members for ensemble data.
    
    7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    8) output_path (String) - The local directory for the ECMWF data files.
    
    9) output_filename (String) - The filename of the output file.
    
    Optional Arguments: None
    
    Returns
    -------
    
    Queried file downloaded to {output_path}    
    """
    
    records = load_index(
                        index_url,
                        proxies
                        )

    
    selected = select_records(
            records,
            levtype=level_type,
            levels=levels,
            params=variables,
            members=members,
        )
    
    try:
        download_messages(
            grib_url,
            selected,
            output_path,
            output_filename,
            proxies
        )
    except Exception as e:
        for i in range(0, 10, 1):
            sleep(30)
            try:
                download_messages(
                            grib_url,
                            selected,
                            output_path,
                            output_filename,
                            proxies
                        )
                break
            except Exception as e:
                i = i
                if i >= 9:
                    print(f"Error: Client unable to reconnect. - System Exit.")
                    sys.exit(1)
                    
    validate_file(output_path,
                  output_filename)