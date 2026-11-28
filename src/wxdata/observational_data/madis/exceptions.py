"""
This file has the function that returns errors for requesting MADIS data to the user.

(C) Eric J. Drewitz 2025-2026
"""

import sys

def request_error(response):
    
    """
    This function returns an error based on the response code so users can troubleshoot their request errors.
    
    Required Arguments:
    
    1) response (HTTP Response) - The HTTP response for the request.
    
    Optional Arguments: None    
    """
    
    status = response.status_code
    
    if status == 200:
        pass
    elif status == 441:
        print(f"Error Response Code {status}: URL is too long for the server to process.")
        print(f"This is most likely attributed to having too many variables selected.")
        print(f"Try selecting less variables in a single request and try again.")
        print(f"System Exit")
        sys.exit(1)
    elif status == 429:
        print(f"Error Response Code {status}: User has submitted too many requests in a too short period of time.")
        print(f"This is from submitting too many requests in a too short period of time exceeding the server rate-limit.")
        print(f"Wait a few minutes and then try again.")
        print(f"System Exit")
        sys.exit(1)
    elif status == 500:
        print(f"Error Response Code {status}: Internal Server Error.")
        print(f"This is likely an issue on the server end and not user-error.")
        print(f"Wait a couple of minutes and try re-submitting.")
        sys.exit(1)
    else:
        print(f"Error Response Code {status}. An error occurred.")
        print(f"System Exit")
        sys.exit(1)