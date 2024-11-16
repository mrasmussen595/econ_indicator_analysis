# visualizations.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import COLORS


def prepare_viz_data(df, start_date='1996-12-31'):
    """
    Prepare data for visualization
    """
    # Convert start_date to datetime
    start_date = pd.to_datetime(start_date)
    # Since date is the index, filter using the index directly
    df_viz = df[df.index >= start_date].copy()
    df_viz['year'] = df_viz.index.year
    # Filter for necessary columns

    """df_viz = df_viz[[
        'quarter',
        'year',
        'period',
        'quarterly_spread',
        'next_quarter_delinquency',
        'delinquency_rate_loans'
    ]].drop_duplicates()"""

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
    time_series_plot = plot_time_series(df_viz)

    return current_plot, predictive_plot, time_series_plot

def plot_current_relationship(current_df):
    """Create current analysis plot"""
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

    apply_standard_formatting(fig, "Corporate Loan Risk Analysis", f"Delinquency Rate vs Option-Adjusted Spread (Correlation: {correlation:.3f})")
    return fig

def plot_predictive_relationship(prediction_df):
    """Create scatter plot of predictive relationship"""
    correlation = prediction_df['quarterly_spread'].corr(prediction_df['loan_delinq_3m_forward'])

    fig = px.scatter(
        prediction_df,
        x='quarterly_spread',
        y='loan_delinq_3m_forward',
        trendline="ols",
        title=f'Predictive Analysis (Correlation: {correlation:.3f})',
        labels={
            'quarterly_Spread': 'Current Quarter Spread (basis points)',
            'loan_delinq_3m_forward': 'Next Quarter Delinquency Rate (%)'
        }
    )

    apply_standard_formatting(fig, "Predictive Risk Analysis", f"Next Quarter's Delinquency Rate vs Current Option-Adjusted Spread (Correlation: {correlation:.3f})")
    return fig

def plot_time_series(df):
   """Create time series plot with clean styling and axis labels"""
   # Calculate annual averages
   df_annual = df.groupby('year').agg({
       'quarterly_spread': 'mean',
       'delinquency_rate_loans': 'mean',
       'period': 'first'
   }).reset_index()

   fig = make_subplots(specs=[[{"secondary_y": True}]])

   # Add spread line
   fig.add_trace(
       go.Scatter(
           x=df_annual['year'],
           y=df_annual['quarterly_spread'],
           name="Option-Adjusted Spread",
           mode='lines+markers',  # Keep markers, remove text
           line=dict(color=COLORS['Expansion'])
       ),
       secondary_y=False
   )

   # Add delinquency line
   fig.add_trace(
       go.Scatter(
           x=df_annual['year'],
           y=df_annual['delinquency_rate_loans'],
           name="Delinquency Rate",
           mode='lines+markers',  # Keep markers, remove text
           line=dict(color=COLORS['Great Recession'])
       ),
       secondary_y=True
   )

   # Update layout with axis titles
   fig.update_layout(
       xaxis_title="Year",
       yaxis_title="Option-Adjusted Spread (basis points)",
       yaxis2_title="Delinquency Rate (%)"
   )

   # Apply formatting
   fig = apply_standard_formatting(
       fig,
       "Long-Term Credit Risk Trends",
       "Annual Average Spread vs Delinquency Rate"
   )

   return fig

def apply_standard_formatting(fig, title, subtitle=None):
    """Apply consistent, enhanced formatting to plots"""
    # Set main title and subtitle
    full_title = title
    if subtitle:
        full_title += f'<br><span style="font-size: 14px">{subtitle}</span>'
    
    fig.update_layout(
        # Title configuration
        title=dict(
            text=full_title,
            font=dict(size=24),
            x=0.5,  # Center the title
            y=0.95
        ),
        # Basic layout
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12),
        width=1000,
        height=600,
        margin=dict(t=100, l=80, r=40, b=80),
        
        # Legend configuration
        legend=dict(
            title="Economic Period",
            borderwidth=1,
            bordercolor='#E5E5E5',
            bgcolor='rgba(255, 255, 255, 0.9)',
            x=0.02,
            y=0.98
        )
    )
    
    # Enhance axes styling
    for axis in [fig.update_xaxes, fig.update_yaxes]:
        axis(
            showgrid=True,
            gridwidth=1,
            gridcolor='#E5E5E5',
            mirror=True,
            showline=True,
            linewidth=2,
            linecolor='#2C3E50'
        )
    
    # Style markers and trendline
    fig.update_traces(
        marker=dict(size=12, line=dict(width=1, color='white')),
        selector=dict(mode='markers')
    )
    fig.update_traces(
        line=dict(width=2, dash='dot'),
        selector=dict(mode='lines')
    )
    
    # Add source citation
    fig.add_annotation(
        text="Source: Federal Reserve Economic Data (FRED)",
        xref="paper", yref="paper",
        x=0.0000001, y=-0.15,
        showarrow=False,
        font=dict(size=9, color='gray')
    )
    
    return fig

def fred_export(df, output_path='fred_analysis.pdf'):
    """
    Export FRED analysis plots to a single PDF while maintaining exact styling
    and separate legends for each plot.
    """
    # Get the individual plots
    current_plot, predictive_plot, time_series_plot = fred_visualize(df)
    
    # Create a single figure with subplots
    fig = make_subplots(
        rows=3, 
        cols=1,
        subplot_titles=[
            'Corporate Loan Risk Analysis<br>' +
            '<span style="font-size: 14px">' +
            f'Delinquency Rate vs Option-Adjusted Spread (Correlation: {df["quarterly_spread"].corr(df["delinquency_rate_loans"]):.3f})</span>',
            
            'Predictive Risk Analysis<br>' +
            '<span style="font-size: 14px">' +
            f'Next Quarter\'s Delinquency Rate vs Current Option-Adjusted Spread (Correlation: {df["quarterly_spread"].corr(df["loan_delinq_3m_forward"]):.3f})</span>',
            
            'Long-Term Credit Risk Trends<br>' +
            '<span style="font-size: 14px">Annual Average Spread vs Delinquency Rate</span>'
        ],
        vertical_spacing=0.2,
        specs=[[{"secondary_y": False}],
               [{"secondary_y": False}],
               [{"secondary_y": True}]]
    )
    
    # Add traces with modified properties
    # Current relationship plot (with period legend)
    for trace in current_plot.data:
        new_trace = go.Scatter(
            x=trace.x,
            y=trace.y,
            mode=trace.mode,
            name=trace.name,
            legendgroup="period",
            legendgrouptitle=dict(text="Economic Period"),
            marker=trace.marker,
            line=trace.line if hasattr(trace, 'line') else None,
            legend="legend"
        )
        fig.add_trace(new_trace, row=1, col=1)
    
    # Predictive relationship plot (no legend needed)
    for trace in predictive_plot.data:
        new_trace = go.Scatter(
            x=trace.x,
            y=trace.y,
            mode=trace.mode,
            name=trace.name,
            showlegend=False,
            marker=trace.marker,
            line=trace.line if hasattr(trace, 'line') else None
        )
        fig.add_trace(new_trace, row=2, col=1)
    
    # Time series plot (with metrics legend)
    for i, trace in enumerate(time_series_plot.data):
        new_trace = go.Scatter(
            x=trace.x,
            y=trace.y,
            mode=trace.mode,
            name=trace.name,
            legendgroup="metrics",
            legendgrouptitle=dict(text="Metrics"),
            marker=trace.marker,
            line=trace.line if hasattr(trace, 'line') else None,
            legend="legend2"
        )
        fig.add_trace(
            new_trace,
            row=3,
            col=1,
            secondary_y=trace.name == "Delinquency Rate"
        )
    
    # Update layout for the combined figure
    fig.update_layout(
        # Overall figure settings
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12),
        width=1000,
        height=1800,
        margin=dict(t=100, l=80, r=40, b=80),
        
        # Update legend settings
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",     # Changed to "top"
            y=0.98,            # Near top (values from 0 to 1)
            xanchor="left",    # Changed to "left"
            x=0.02            # Slightly inset from left edge
        ),
        legend2=dict(
            orientation="h",
            yanchor="bottom",  # Keep as "bottom"
            y=0.15,           # Near bottom (lower values are further down)
            xanchor="left",
            x=0.02            # Slightly inset from left edge
        )
    )
    # Update axes styling for all subplots
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#E5E5E5',
        mirror=True,
        showline=True,
        linewidth=2,
        linecolor='#2C3E50'
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#E5E5E5',
        mirror=True,
        showline=True,
        linewidth=2,
        linecolor='#2C3E50'
    )
    
    # Update specific axis labels
    fig.update_xaxes(title_text="Current Option-Adjusted Spread", row=1, col=1)
    fig.update_yaxes(title_text="Current Loan Delinquency Rate (%)", row=1, col=1)
    
    fig.update_xaxes(title_text="Current Quarter Spread (basis points)", row=2, col=1)
    fig.update_yaxes(title_text="Next Quarter Delinquency Rate (%)", row=2, col=1)
    
    fig.update_xaxes(title_text="Year", row=3, col=1)
    fig.update_yaxes(title_text="Option-Adjusted Spread (basis points)", row=3, col=1, secondary_y=False)
    fig.update_yaxes(title_text="Delinquency Rate (%)", row=3, col=1, secondary_y=True)
    
    # Add source citation at the bottom
    fig.add_annotation(
        text="Source: Federal Reserve Economic Data (FRED)",
        xref="paper", yref="paper",
        x=0.0000001, y=-0.05,
        showarrow=False,
        font=dict(size=9, color='gray')
    )
    
    # Export to PDF
    fig.write_image(output_path, format='pdf')
    
    return fig