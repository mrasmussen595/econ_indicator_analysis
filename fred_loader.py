# File specifically for data extraction 
import requests
import pandas as pd
from config import API_KEY, BASE_URL, INDICATORS, START_DATE

def get_fred_data(series_id, start_date=START_DATE):
    """
    Get economic data from FRED API
    
    Example:
    >>> unemployment_data = get_fred_data('UNRATE', '2000-01-01')
    
    Args:
        series_id: FRED series code (like 'UNRATE' for unemployment)
        start_date: Start date for data (YYYY-MM-DD format)
    
    Returns:
        Time series of values with dates as index
    """
    # Set up API call
    url = f"{BASE_URL}/series/observations"
    params = {
        'series_id': series_id,
        'api_key': API_KEY,
        'file_type': 'json',
        'observation_start': start_date
    }
    
    try:
        # Get data from FRED
        response = requests.get(url, params=params)
        response.raise_for_status()  
        data = response.json()
        
        # Convert to pandas series with date index
        df = pd.DataFrame(data['observations'])
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        
        return df.set_index('date')['value']
    
    except requests.exceptions.RequestException as e:
        print(f"Couldn't get data for {series_id}. Error: {e}")
        return pd.Series()
    
def fred_load():
    """
    Get all economic indicators in one DataFrame
    """
    # Load each indicator using config
    data = {}
    for name, info in INDICATORS.items():
        data[name] = get_fred_data(info['id'])

    return pd.DataFrame(data)