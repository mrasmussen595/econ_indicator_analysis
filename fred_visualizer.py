# visualizations.py
import pandas as pd
import plotly.express as px


def prepare_viz_data(df, start_date='1996-12-31'):
    """
    Prepare data for visualization
    """
    # Convert start_date to datetime
    start_date = pd.to_datetime(start_date)

    # Since date is the index, filter using the index directly
    df_viz = df[df.index >= start_date].copy()
    # Filter for necessary columns
    df_viz = df_viz[[
        'quarter',
        'period',
        'quarterly_spread',
        'next_quarter_delinquency',
        'delinquency_rate_loans'
    ]].drop_duplicates()

    return df_viz
def fred_visualize(df):
    # Prepare data
    df_viz = prepare_viz_data(df)

    print("Data prepared. Shape:", df_viz.shape)
    print("Columns after preparation:", df_viz.columns.tolist())

    # Print key statistics
    print("Credit Risk Analysis Results:")
    # Create visualizations
    current_plot = plot_current_relationship(df_viz)
    predictive_plot = plot_predictive_relationship(df_viz)

    return current_plot, predictive_plot

def plot_current_relationship(current_df):
    """Create enhanced predictive analysis plot"""
    correlation = current_df['quarterly_spread'].corr(current_df['delinquency_rate_loans'])

    fig = px.scatter(
        current_df,
        x='quarterly_spread',
        y='delinquency_rate_loans',
        color='period',
        trendline="ols",
        title='High Yield Spreads Predict Future Loan Delinquencies<br>' +
              f'<span style="font-size: 14px">Correlation: {correlation:.3f}</span>',
        labels={
            'quarterly_spread': 'Current Option-Adjusted Spread',
            'delinquency_rate_loans': 'Current Loan Delinquency Rate (%)',
            'period': 'Economic Period'
        }
    )

    apply_standard_formatting(fig)
    return fig

def plot_predictive_relationship(prediction_df):
    """Create scatter plot of predictive relationship"""
    correlation = prediction_df['quarterly_spread'].corr(prediction_df['next_quarter_delinquency'])

    fig = px.scatter(
        prediction_df,
        x='quarterly_spread',
        y='next_quarter_delinquency',
        trendline="ols",
        title=f'Predictive Analysis (Correlation: {correlation:.3f})',
        labels={
            'quarterly_Spread': 'Current Quarter Spread (basis points)',
            'next_quarter_delinquency': 'Next Quarter Delinquency Rate (%)'
        }
    )

    apply_standard_formatting(fig)
    return fig

def apply_standard_formatting(fig):
    """Apply consistent formatting to all plots"""
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12),
        width=1000,
        height=600,
        legend=dict(
            borderwidth=1,
            bordercolor='#E5E5E5',
            bgcolor='rgba(255, 255, 255, 0.9)'
        )
    )

    fig.update_traces(
        marker=dict(size=12, line=dict(width=1, color='white')),
        selector=dict(mode='markers')
    )

    # Add source citation
    fig.add_annotation(
        text="Source: Federal Reserve Economic Data (FRED)",
        xref="paper", yref="paper",
        x=0, y=-0.15,
        showarrow=False,
        font=dict(size=9, color='gray')
    )
