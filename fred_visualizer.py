# visualizations.py
import io
import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF, Template
from PIL import Image
from plotly.subplots import make_subplots

from fred_config import COLORS


def prepare_viz_data(df, start_date='1996-12-31'):
    """
    Prepare data for visualization
    """
    # Convert start_date to datetime
    start_date = pd.to_datetime(start_date)
    # Since date is the index, filter using the index directly
    df_viz = df[df.index >= start_date].copy()
    df_viz['year'] = df_viz.index.year
    return df_viz

def fred_visualize(df):
    # Prepare data
    df_viz = prepare_viz_data(df)
    # Print key statistics
    print("Credit Risk Analysis Results:")
    # Create visualizations
    stats_table = create_stats_table(df_viz) 
    current_plot = plot_current_relationship(df_viz)
    predictive_plot = plot_predictive_relationship(df_viz)
    time_series_plot = plot_time_series(df_viz)

    return stats_table,current_plot, predictive_plot, time_series_plot

def create_stats_table(df):
    """
    Create a visually enhanced statistical summary table by market regime with improved formatting.
    """
    def format_correlation(value, is_r_squared=False):
        """Helper function to format and color-code correlation values"""
        if is_r_squared:
            if value > 0.5:
                color = "#2ecc71"  # Strong R² (green)
            elif value < 0.1:
                color = "#e74c3c"  # Weak R² (red)
            else:
                return "{:.2f}".format(value)
        else:
            if abs(value) > 0.7:
                color = "#2ecc71"  # Strong correlation (green)
            elif abs(value) < 0.3 or value < 0:
                color = "#e74c3c"  # Weak/negative correlation (red)
            else:
                return "{:.2f}".format(value)
        return f'<span style="color: {color}">{value:.2f}</span>'

    # Enhanced metrics list with more descriptive names
    metrics = [
        {'name': 'Credit Spread Analysis', 'is_header': True},
        {'name': 'Average Option-Adjusted Spread', 'column': 'option_adjusted_spread', 'func': 'mean', 'format': '{:.0f} bps'},
        {'name': 'Spread Volatility (Std Dev)', 'column': 'option_adjusted_spread', 'func': 'std', 'format': '{:.0f} bps'},
        
        {'name': 'Loan Performance Metrics', 'is_header': True},
        {'name': 'Average Delinquency Rate', 'column': 'delinquency_rate_loans', 'func': 'mean', 'format': '{:.2f}%'},
        {'name': 'Delinquency Volatility (Std Dev)', 'column': 'delinquency_rate_loans', 'func': 'std', 'format': '{:.2f}%'},
        
        {'name': 'Predictive Relationships', 'is_header': True}
    ]
    
    # Add simplified correlation metrics
    for months in [3, 6, 12]:
        period = 'Quarter' if months == 3 else 'Half-Year' if months == 6 else 'Year'
        metrics.extend([
            {'name': f'{period} Forward Correlation', 'column': f'loan_delinq_{months}m_forward', 
             'func': 'corr', 'base_column': 'option_adjusted_spread', 'format': '{:.2f}'},
            {'name': f'{period} Forward R²', 'column': f'loan_delinq_{months}m_forward', 
             'func': 'corr_squared', 'base_column': 'option_adjusted_spread', 'format': '{:.2f}'}
        ])

    # Calculate statistics
    results = []
    regimes = df['economic_period'].unique()

    for metric in metrics:
        if metric.get('is_header'):
            row = {'Metric': f'<b>{metric["name"]}</b>', **{regime: '' for regime in regimes}}
        else:
            row = {'Metric': f'  {metric["name"]}'}
            
            for regime in regimes:
                regime_data = df[df['economic_period'] == regime]
                try:
                    if metric.get('func') == 'corr':
                        # Calculate correlation using the base column and target column
                        corr = regime_data[metric['base_column']].corr(regime_data[metric['column']])
                        row[regime] = format_correlation(corr, is_r_squared=False)
                        
                    elif metric.get('func') == 'corr_squared':
                        # Calculate R² as the square of the correlation
                        corr = regime_data[metric['base_column']].corr(regime_data[metric['column']])
                        r_squared = corr ** 2
                        row[regime] = format_correlation(r_squared, is_r_squared=True)
                        
                    else:
                        # Handle other statistics (mean, std, etc.)
                        value = getattr(regime_data[metric['column']], metric['func'])()
                        # Convert percentage points to basis points for spread metrics
                        if metric['column'] == 'option_adjusted_spread':
                            value = value * 100
                        row[regime] = metric['format'].format(value)
                    
                except Exception as e:
                    print(f"Error calculating {metric['name']} for {regime}: {str(e)}")
                    row[regime] = 'N/A'
        
        results.append(row)
    fig = go.Figure(data=[go.Table(
            header=dict(
                values=['<b>Metric</b>'] + [f'<b>{regime}</b>' for regime in regimes],
                font=dict(size=14, color='white', family='Arial'),
                fill_color='#0A5FB4',
                align=['left'] + ['center'] * len(regimes),
                height=30,  # Increased from 40
                line_color='#34495e'
            ),
            cells=dict(
                values=[[row['Metric'] for row in results]] + 
                    [[row[regime] for row in results] for regime in regimes],
                font=dict(size=13, family='Arial'),
                align=['left'] + ['center'] * len(regimes),
                height=30,  # Increased from 30
                fill_color=[['#f8f9fa', '#ffffff'] * (len(results)//2 + 1)],
                line_color='#ecf0f1'
            )
        )])

    # Add height to the entire figure
    fig.update_layout(
        height=500,  # Specify overall figure height
        margin=dict(t=20, b=20))
 # Add some margin at top and bottom
    

    fig.update_layout(

        margin=dict(t=80, b=20),
        width=1300,  # Reduced from 1000
        height=600,
        title=dict(
            text="Key Statistics Summary",
            font=dict(size=24),
            x=0.5,  # Center the title
            y=0.95  # Reduced from 600
    ))

    # Add subtitle - adjusted y position
    fig.add_annotation(
        text="Option-adjusted spreads vs corporate loan delinquency rate statistics by economic period",
        xref="paper",
        yref="paper", 
        x=0.5,
        y=1.05,  
        showarrow=False,
        font=dict(size=16),
        xanchor='center',
        yanchor='top',
    ), 

    fig.add_annotation(
        text="Option-Adjusted Spread: Measures spread between below-investment-grade bonds (BB and below) and Treasury curve",
        xref="paper",
        yref="paper", 
        x=0,
        y=0.11, 
        showarrow=False,
        font=dict(size=12),
        xanchor='left',
        yanchor='top',
    )

    fig.add_annotation(
        text="Delinquency Rate on Business Loans: Percentage of business loans that are 30+ days past due measured across all US commercial banks",
        xref="paper",
        yref="paper", 
        x=0,
        y=0.07,  
        showarrow=False,
        font=dict(size=12),
        xanchor='left',
        yanchor='top',
    )

    fig.add_annotation(
        text="Source: Federal Reserve Economic Data (FRED)",
        xref="paper",
        yref="paper", 
        x=0,
        y=0.0001,  
        showarrow=False,
        font=dict(size=12),
        xanchor='left',
        yanchor='top',
    )
    return fig

def plot_current_relationship(current_df):
    """Create current analysis plot"""
    correlation = current_df['option_adjusted_spread'].corr(current_df['delinquency_rate_loans'])

    fig = px.scatter(
        current_df,
        x='quarterly_spread',
        y='delinquency_rate_loans',
        color='economic_period',
        trendline="ols",
        title='High Yield Spreads Predict Future Loan Delinquencies<br>' +
              f'<span style="font-size: 14px">Correlation: {correlation:.3f}</span>',
        labels={
            'quarterly_spread': 'Average Quarterly Spread',
            'delinquency_rate_loans': 'Current Quarter Delinquency Rate (%)',
            'economic_period': 'Economic Period'
        }
    )

    fig.update_layout(
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

    apply_standard_formatting(fig, "Corporate Loan Risk Analysis", f"Delinquency Rate vs Option-Adjusted Spread (Correlation: {correlation:.3f})")
    return fig

def plot_predictive_relationship(prediction_df):
    """Create scatter plot of predictive relationship"""
    correlation = prediction_df['option_adjusted_spread'].corr(prediction_df['loan_delinq_3m_forward'])

    fig = px.scatter(
        prediction_df,
        x='quarterly_spread',
        y='loan_delinq_3m_forward',
        color='economic_period',
        trendline="ols",
        title=f'Predictive Analysis (Correlation: {correlation:.3f})',
        labels={
            'quarterly_spread': 'Average Quarterly Spread',
            'loan_delinq_3m_forward': 'Next Quarter Delinquency Rate (%)',
            'economic_period': 'Economic Period'
        }
    )

    fig.update_layout(
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

    apply_standard_formatting(fig, "Predictive Risk Analysis", f"Next Quarter's Delinquency Rate vs Current Option-Adjusted Spread (Correlation: {correlation:.3f})")
    return fig

def plot_time_series(df):
   """Create time series plot with clean styling and axis labels"""
   # Calculate annual averages
   df_annual = df.groupby('year').agg({
       'option_adjusted_spread': 'mean',
       'delinquency_rate_loans': 'mean',
       'economic_period': 'first'
   }).reset_index()

   fig = make_subplots(specs=[[{"secondary_y": True}]])

   # Add spread line
   fig.add_trace(
       go.Scatter(
           x=df_annual['year'],
           y=df_annual['option_adjusted_spread'],
           name="Option-Adjusted Spread",
           mode='lines+markers',  # Keep markers, remove text
           line=dict(color=COLORS['Pre-GFC (1996-2007)'])
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
           line=dict(color=COLORS['Post-Crisis (2010-2020)'])
       ),
       secondary_y=True
   )

   # Update layout with axis titles
   fig.update_layout(
       xaxis_title="Year",
       yaxis_title="Option-Adjusted Spread",
       yaxis2_title="Delinquency Rate (%)",
        legend=dict(
            title="Metric",
            borderwidth=1,
            bordercolor='#E5E5E5',
            bgcolor='rgba(255, 255, 255, 0.9)',
            x=0.02,
            y=0.98
        )
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

def create_title(pdf, title="FRED Economic Analysis"):
    # Add title
    pdf.set_font('Arial', '', 24)  
    pdf.ln(60)
    pdf.write(5, title)
    pdf.ln(10)
    pdf.set_font('Arial', '', 16)
    pdf.write(4, "Economic Analysis Report")
    pdf.ln(5)

def fred_export(stats_table, current_plot, predictive_plot, time_series_plot, filename="fred_analysis.pdf"):
    # Create tmp directory if it doesn't exist
    os.makedirs("./tmp", exist_ok=True)
    
    pdf = FPDF()  # A4 (210 by 297 mm)
    WIDTH = 210
    HEADER_PATH = r"./resources/report_header.png"
    ''' First Page '''
    pdf.add_page()
    pdf.image(HEADER_PATH, 0, 0, WIDTH)
    create_title(pdf)
    
    # Save plots as images
    stats_table.write_image("./tmp/stats_table.png") 
    time_series_plot.write_image("./tmp/time_series_plot.png")
    
    # Add plots to first page
    pdf.image("./tmp/stats_table.png", 5, 35, WIDTH)
    pdf.image("./tmp/time_series_plot.png", 5,140, WIDTH)

    ''' Second Page '''
    pdf.add_page()
    
    # Save plots as images
    current_plot.write_image("./tmp/current_plot.png")
    predictive_plot.write_image("./tmp/predictive_plot.png")
    
    # Add plots to second page
    pdf.image("./tmp/current_plot.png", 5,10, WIDTH-10)
    pdf.image("./tmp/predictive_plot.png", 5, 140, WIDTH-10)

    # Save the PDF
    pdf.output(filename)

    # Clean up temporary files
    for file in ["stats_table.png", "current_plot.png", "predictive_plot.png", "time_series_plot.png"]:
        try:
            os.remove(f"./tmp/{file}")
        except:
            pass
    
    # Try to remove tmp directory if empty
    try:
        os.rmdir("./tmp")
    except:
        pass