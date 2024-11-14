# File specifically for data extraction 

import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment
API_KEY = os.getenv('FRED_API_KEY')
BASE_URL = 'https://api.stlouisfed.org/fred'

def get_fred_series(series_id, observation_start=None):
    """
    Fetch data series from FRED API
    
    Parameters:
    series_id (str): FRED series identifier
    observation_start (str): Start date in YYYY-MM-DD format
    
    Returns:
    pandas.DataFrame: Time series data
    """
    # Build API URL
    url = f"{BASE_URL}/series/observations"
    
    params = {
        'series_id': series_id,
        'api_key': API_KEY,
        'file_type': 'json',
        'observation_start': observation_start if observation_start else '1976-01-01'
    }
    
    # Make API request
    response = requests.get(url, params=params)
    data = response.json()
    
    # Convert to DataFrame
    df = pd.DataFrame(data['observations'])
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    
    return df.set_index('date')['value'] #set date index so pandas automatically knows the date (i.e. resampling)

# Get various indicators 
yield_spread = get_fred_series('T10Y2Y')
gdp = get_fred_series('GDPC1')
fed_funds = get_fred_series('DFF')
unemployment = get_fred_series('UNRATE')
option_adjusted_spread = get_fred_series('BAMLH0A0HYM2')
delinquency_rate_credit = get_fred_series('DRCCLACBS')
delinquency_rate_loans = get_fred_series('DRBLACBS')
# Create main dataframe
df = pd.DataFrame({
    'yield_spread': yield_spread,
    'gdp': gdp,
    'fed_funds':fed_funds, 
    'unemployment': unemployment,
    'option_adjusted_spread': option_adjusted_spread,
    'delinquency_rate_credit_cards': delinquency_rate_credit,
    'delinquency_rate_loans': delinquency_rate_loans
})