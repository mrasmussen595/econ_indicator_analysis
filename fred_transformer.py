# Third Cell - Data Transformation
import pandas as pd
import numpy as np

def fred_transform(df):
    # GDP calculation
    df['gdp_growth'] = df['gdp'].pct_change(periods=4) * 100

    # Option - Adjusted Spread Calc: Average over each quarter 
    """
    SQL Equivalent: 
    with cte AS (
        SELECT
            date, 
            AVERAGE(option_adjusted_spread) OVER PARTITION BY QUARTER(DATE)) as quarterly_spread
        FROM fred_data) 
    """
    df['quarterly_spread'] = df.groupby(df.index.to_period('Q'))['option_adjusted_spread'].transform('mean')
    # Add next quarter's delinquency rate for predictive modeling
    """
    SQL Equivalent:
    SELECT 
        date,
        delinquency_rate_loans,
        LEAD(delinquency_rate_loans, 1) OVER (
            ORDER BY date
        ) as next_quarter_delinquency
    FROM fred_data
    """
    df['next_quarter_delinquency'] =  df['delinquency_rate_loans'].shift(-90)

    # Call fill missing value function below
    df = fill_missing_values(df)
    # Date processing
    df = df.reset_index()
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    df['quarter'] = df.index.quarter.astype(str) + "Q" + df.index.year.astype(str).str[-2:]

    # Add period classifications
    df['period'] = classify_periods(df)
    
    return df

def classify_periods(df):
    """
    SQL Equivalent: 
    SELECT *,
        CASE 
            WHEN date BETWEEN '2001-01-01' AND '2001-12-31' THEN 'Dot Com' 
            WHEN date BETWEEN '2007-10-01' AND '2009-06-30' THEN 'Great Recession'
            WHEN date BETWEEN '2020-01-01' AND '2020-06-30' THEN 'COVID'
            ELSE 'Expansion' 
        END AS period
    FROM fred_data 
    """
    periods = []
    for date in df.index:
        if '2001-01-01' <= str(date) <= '2001-12-31':
            periods.append('Dot Com')
        elif '2007-10-01' <= str(date) <= '2009-06-30':
            periods.append('Great Recession')
        elif '2020-01-01' <= str(date) <= '2020-06-30':
            periods.append('COVID')
        else:
            periods.append('Expansion')
            
    return periods

def fill_missing_values(df):
        # Fill down credit card delinquency data + loan delinquency data (only available quarterly) and spreads (averaging)
    """
    SQL Equivalent: 
    with cte AS (
        SELECT
            date,
            COALESCE(
                delinquency_rate_loans,
                LAG(delinquency_rate_loans) OVER (ORDER BY date)
            ) AS delinquency_rate_loans,
            COALESCE(
                delinquency_rate_credit_cards,
                LAG(delinquency_rate_credit_cards) OVER (ORDER BY date)
            ) AS delinquency_rate_credit_cards, 
            COALESCE(
                quarterly_spreads,
                LAG(quarterly_spreads) OVER (ORDER BY date)
            ) AS quarterly_spreads, 
        FROM fred_data ) 
    """
    columns_to_fill = [
        'delinquency_rate_credit_cards',
        'delinquency_rate_loans',
        'quarterly_spread' ]
    
    df[columns_to_fill] = df[columns_to_fill].ffill()
    
    return df