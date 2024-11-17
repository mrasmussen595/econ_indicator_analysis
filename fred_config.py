# config.py
import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('FRED_API_KEY')
BASE_URL = 'https://api.stlouisfed.org/fred'
START_DATE = '1976-01-01'

# Economic indicators with their FRED codes and descriptions
INDICATORS = {
   'yield_spread': {
       'id': 'T10Y2Y',
       'name': 'Treasury Yield Spread (10Y-2Y)',
       'description': 'Difference between 10-Year and 2-Year Treasury Constant Maturity Rates'
   },
   'gdp': {
       'id': 'GDPC1', 
       'name': 'Real GDP',
       'description': 'Real Gross Domestic Product'
   },
   'fed_funds': {
       'id': 'DFF',
       'name': 'Federal Funds Rate',
       'description': 'Federal Funds Effective Rate'
   },
   'unemployment': {
       'id': 'UNRATE',
       'name': 'Unemployment Rate',
       'description': 'Civilian Unemployment Rate'
   },
   'option_adjusted_spread': {
       'id': 'BAMLH0A0HYM2',
       'name': 'High Yield Bond Spread',
       'description': 'ICE BofA US High Yield Index Option-Adjusted Spread'
   },
   'delinquency_rate_credit_cards': {
       'id': 'DRCCLACBS',
       'name': 'Credit Card Delinquency Rate',
       'description': 'Delinquency Rate on Credit Card Loans'
   },
   
   'delinquency_rate_loans': {
       'id': 'DRBLACBS',
       'name': 'Business Loan Delinquency Rate',
       'description': 'Delinquency Rate on Business Loans'
   },
    'cpi': {
       'id': 'CPIAUCSL',
       'name': 'Consumer Price Index',
       'description': 'Measures average change in prices paid by consumers. Main inflation indicator.'
   },
        'pce': {
       'id': 'PCEPI',
       'name': 'PCE Price Index',
       'description': 'Federal Reserve\'s preferred inflation measure. Tracks personal consumption costs.'
   }
   
}

# Important economic periods to highlight
PERIODS = {
    'Pre-GFC (1996-2007)': ('1996-12-31', '2007-10-01'),
    'Great Recession (2008-2010)': ('2007-10-01', '2009-06-30'),
    'Post-Crisis (2010-2020)': ('2009-06-30', '2020-01-01'),
    'Covid to Present (2020-2024)': ('2020-01-01', None)
}

# Colors for visualizations
COLORS = {
   'Pre-GFC (1996-2007)': '#0081AF',    # Blue
   'Great Recession (2008-2010)': '#2D936C',  # Green
   'Post-Crisis (2010-2020)': '#764B8E', # Purple
   'Covid to Present (2020-2024)': '#9E2A2B'      # Red
}