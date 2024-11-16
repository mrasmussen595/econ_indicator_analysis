# Third Cell - Data Transformation
import pandas as pd

from config import PERIODS


def fred_transform(df):
    # GDP calculation
    df['gdp_growth'] = df['gdp'].pct_change(periods=4) * 100
    
    # Option-Adjusted Spread Calc: Average over each quarter
    df['quarterly_spread'] = df.groupby(df.index.to_period('Q'))['option_adjusted_spread'].transform('mean')
    
    # Add forward-looking delinquency rates
    df = create_forward_metrics(
    df, 
    metric_column='delinquency_rate_loans', 
    prefix='loan_delinq'
    )
    
    # Call fill missing value function
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
    #Label economic periods from config.py file
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
    def get_period(date):
        date_str = date.strftime('%Y-%m-%d')
        for period_name, (start, end) in PERIODS.items():
            if start <= date_str <= end:
                return period_name
        return 'Expansion'

    return df.index.map(get_period)

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
    I'd join back on this cte by date in the main table.
    """
    result_df = df.copy()
    
    columns_to_fill = [
        'delinquency_rate_credit_cards',
        'delinquency_rate_loans',
        'quarterly_spread' ]

    # Add any columns containing 'm_forward'
    forward_columns = [col for col in df.columns if 'm_forward' in col]
    columns_to_fill.extend(forward_columns)
    
    # Remove any columns that don't exist in the dataframe
    columns_to_fill = [col for col in columns_to_fill if col in df.columns]
    
    # Forward fill the selected columns
    if columns_to_fill:
        result_df[columns_to_fill] = result_df[columns_to_fill].ffill()
    
    return result_df

def create_forward_metrics(df, metric_column, prefix, intervals=[3, 6, 9, 12, 18, 24]):
    """
    Create forward-looking values at specified monthly intervals for any metric
    """
    for months in intervals:
        # Calculate the number of quarters to shift
        quarters_shift = months // 3
        
        # Get the last value for each quarter and shift it
        forward_value = df.groupby(df.index.to_period('Q'))[metric_column].last().shift(-quarters_shift)
        
        # Add the column directly to the dataframe
        df[f'{prefix}_{months}m_forward'] = df.index.to_period('Q').map(forward_value)
    
    return df