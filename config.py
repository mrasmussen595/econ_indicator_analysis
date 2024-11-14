# config.py
from dotenv import load_dotenv
import os

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
   }
}

# Important economic periods to highlight
PERIODS = {
   'Dot Com Crisis': ('2001-01-01', '2001-12-31'),
   'Great Recession': ('2007-10-01', '2009-06-30'),
   'COVID-19': ('2020-01-01', '2020-06-30')
}

# Colors for visualizations
COLORS = {
   'Expansion': '#2E86C1',    # Blue
   'Dot Com Crisis': '#E74C3C',  # Red
   'Great Recession': '#8E44AD', # Purple
   'COVID-19': '#F39C12'      # Orange
}