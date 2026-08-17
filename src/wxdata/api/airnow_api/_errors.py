"""
File hosting common types of error messages for the Air Now API

(C) Eric J. Drewitz 2025-2026
"""

def missing_api_key():
    
    """
    Error message for missing API Key
    """
    
    print("Error: User has not passed in an API Key nor defined a path to a .txt file that contains an existing API Key.")
    print("Visit: https://docs.airnowapi.org/ to create a free API Key if you don't already have one.")

    
def rate_limit_error_message():
    
    """
    Returns an error message when rate limited    
    """
    
    print(f"Error: Too Many Requests")
    print(f"The Air-Now API allows for up to 500 calls per hour.")
    print(f"Please try again later.")