"""
This file hosts the functions associated with exceptions when retrieving Wyoming Sounding Data.

(C) Eric J. Drewitz 2025-2026
"""

def station_id_exception(station_id):
    
    """
    This function returns an error message to the user for an invalid station ID
    
    Required Arguments:
    
    1) station_id (String) - The station ID.
    
    Returns
    -------
    
    An error message saying something went wrong and is likely an invalid station ID.    
    """
    
    print(f"""
          
          Error: Data retrival unsuccessful.
          
          Most likely due to {station_id.upper()} being an invalid station ID.
          
          If {station_id.upper()} is valid, there could be no data available at this time.
          """)
    
    
def date_format_exception(date):
    
    """
    This function returns an error message for a date format exception.
    
    Required Arguments:
    
    1) date (String) - The date/time in string format.
    
    Returns
    -------
    
    An error message stating there is an issue with the format and reminding the user of the correct format.    
    """
    
    print(f"""
          
          Error: User submitted an invalid date. 
          
          {date} is not properly formatted.
          
          Please format date as 'YYYY-mm-dd:HH' and try again.
          
          YYYY - Four digit year.
          
          mm - Two digit month.
          
          dd - Two digit day.
          
          HH - Two digit hour (24-Hour Clock)
          
          """)