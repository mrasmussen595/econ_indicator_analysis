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
    # Enhanced metrics list with more descriptive names
    metrics = [
        {'name': 'Credit Spread Analysis', 'is_header': True},
        {'name': 'Average Option-Adjusted Spread', 'column': 'quarterly_spread', 'func': 'mean', 'format': '{:.0f} bps'},
        {'name': 'Spread Volatility (Std Dev)', 'column': 'quarterly_spread', 'func': 'std', 'format': '{:.0f} bps'},
        
        {'name': 'Loan Performance Metrics', 'is_header': True},
        {'name': 'Average Delinquency Rate', 'column': 'delinquency_rate_loans', 'func': 'mean', 'format': '{:.2f}%'},
        {'name': 'Delinquency Volatility', 'column': 'delinquency_rate_loans', 'func': 'std', 'format': '{:.2f}%'},
        
        {'name': 'Predictive Relationships', 'is_header': True}
    ]
    
    # Add simplified correlation metrics
    for months in [3, 6, 12]:
        period = 'Quarter' if months == 3 else 'Half-Year' if months == 6 else 'Year'
        metrics.extend([
            {'name': f'{period} Forward Correlation', 'column': f'loan_delinq_{months}m_forward', 
             'func': 'corr', 'base_column': 'quarterly_spread', 'format': '{:.2f}'},
            {'name': f'{period} Forward R²', 'column': f'loan_delinq_{months}m_forward', 
             'func': 'corr_squared', 'base_column': 'quarterly_spread', 'format': '{:.2f}'}
        ])

    # Calculate statistics
    results = []
    regimes = df['market_regime'].unique()

    for metric in metrics:
        if metric.get('is_header'):
            row = {'Metric': f'<b>{metric["name"]}</b>', **{regime: '' for regime in regimes}}
        else:
            row = {'Metric': f'  {metric["name"]}'}
            
            for regime in regimes:
                regime_data = df[df['market_regime'] == regime]
                try:
                    if metric.get('func') == 'corr':
                        value = regime_data[metric['base_column']].corr(regime_data[metric['column']])
                        # Color coding for correlations
                        if abs(value) > 0.7:
                            formatted_value = f'<span style="color: #2ecc71">{metric["format"].format(value)}</span>'
                        elif abs(value) < 0.3 or value < 0:
                            formatted_value = f'<span style="color: #e74c3c">{metric["format"].format(value)}</span>'
                        else:
                            formatted_value = metric['format'].format(value)
                    elif metric.get('func') == 'corr_squared':
                        value = regime_data[metric['base_column']].corr(regime_data[metric['column']]) ** 2
                        # Color coding for R-squared
                        if value > 0.5:
                            formatted_value = f'<span style="color: #2ecc71">{metric["format"].format(value)}</span>'
                        elif value < 0.1:
                            formatted_value = f'<span style="color: #e74c3c">{metric["format"].format(value)}</span>'
                        else:
                            formatted_value = metric['format'].format(value)
                    else:
                        value = getattr(regime_data[metric['column']], metric['func'])()
                        formatted_value = metric['format'].format(value)
                    
                    row[regime] = formatted_value
                except:
                    row[regime] = 'N/A'
        
        results.append(row)

    # Create table with enhanced formatting
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['<b>Metric</b>'] + [f'<b>{regime}</b>' for regime in regimes],
            font=dict(size=15, color='white', family='Arial'),
            fill_color='#2c3e50',
            align=['left'] + ['center'] * len(regimes),
            height=40,
            line_color='#34495e'
        ),
        cells=dict(
            values=[[row['Metric'] for row in results]] + 
                  [[row[regime] for row in results] for regime in regimes],
            font=dict(size=14, family='Arial'),
            align=['left'] + ['center'] * len(regimes),
            height=30,
            fill_color=[['#f8f9fa', '#ffffff'] * (len(results)//2 + 1)],
            line_color='#ecf0f1'
        )
    )])

    # Update layout with improved spacing
    fig.update_layout(
        title=dict(
            text='Credit Market Risk Analysis by Regime<br>' + 
                 '<span style="font-size: 15px; color: #34495e">Relationship between the US High Yield Index Option-Adjusted Spread and Corporate Loan Delinquency Rate has weakened over time </span>',
            font=dict(size=26, family='Arial', color='#2c3e50'),
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top'
        ),
        width=1300,
        height=600,
        margin=dict(t=80, l=40, r=40, b=40),
        paper_bgcolor='white',
        showlegend=False
    )
    
    # Add enhanced footer with improved positioning
    fig.add_annotation(
        text="<b>Source:</b> Federal Reserve Economic Data (FRED) | " +
             "<b>Color Coding:</b> Green indicates strong predictive relationships, Red indicates weak or negative relationships",
        xref="paper", yref="paper",
        x=0.0, y=-0.05,
        showarrow=False,
        font=dict(size=13, color='#2c3e50'),
        align='left'
    )
    
    return fig

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
    Export FRED analysis plots to a single PDF with clean, executive-ready formatting.
    Includes stats table and all visualizations with properly positioned legends.
    """
    # Get all plots
    stats_table, current_plot, predictive_plot, time_series_plot = fred_visualize(df)
    
    # Create figure with subplots - including space for stats table
    fig = make_subplots(
        rows=4, 
        cols=1,
        row_heights=[0.25, 0.25, 0.25, 0.25],
        vertical_spacing=0.08,
        specs=[[{"type": "table"}],
               [{"secondary_y": False}],
               [{"secondary_y": False}],
               [{"secondary_y": True}]],
        subplot_titles=["", "Current Relationship Analysis", 
                       "Predictive Relationship Analysis", "Historical Trends"]
    )
    
    # Add stats table with full formatting
    table_colors = ['rgb(244, 248, 251)', 'white']  # Alternating row colors
    fig.add_trace(
        go.Table(
            header=dict(
                values=[[col] for col in stats_table.data[0].header.values],
                font=dict(size=14, family='Arial', color='#2c3e50'),
                fill_color='rgb(232, 241, 248)',
                align='left',
                height=30
            ),
            cells=dict(
                values=[[val] for val in stats_table.data[0].cells.values],
                font=dict(size=12, family='Arial', color='#2c3e50'),
                fill_color=[table_colors*(len(stats_table.data[0].cells.values[0])//2 + 1)],
                align='left',
                height=25
            ),
            columnwidth=[2, 1]  # Adjust column widths
        ),
        row=1,
        col=1
    )
    
    # Helper function to extract scatter plot data
    def add_scatter_traces(source_fig, target_fig, row, show_legend=True):
        for trace in source_fig.data:
            if isinstance(trace, go.Scatter):
                new_trace = trace
            else:
                # Convert px trace to go.Scatter
                new_trace = go.Scatter(
                    x=trace['x'],
                    y=trace['y'],
                    mode='markers' if trace.mode == 'markers' else 'lines+markers',
                    name=trace.name,
                    marker=dict(
                        color=trace.marker.color if hasattr(trace.marker, 'color') else None,
                        size=12,
                        line=dict(width=1, color='white')
                    ),
                    line=dict(color=trace.line.color, width=2) if hasattr(trace, 'line') else None,
                    showlegend=show_legend
                )
            target_fig.add_trace(new_trace, row=row, col=1)

    # Add current relationship plot
    add_scatter_traces(current_plot, fig, 2)
    
    # Add predictive relationship plot (no legend needed)
    add_scatter_traces(predictive_plot, fig, 3, False)
    
    # Add time series plot with dual y-axis
    for trace in time_series_plot.data:
        is_delinquency = trace.name == "Delinquency Rate"
        fig.add_trace(
            go.Scatter(
                x=trace.x,
                y=trace.y,
                mode='lines+markers',
                name=trace.name,
                line=trace.line,
                marker=dict(size=8),
                showlegend=True
            ),
            row=4,
            col=1,
            secondary_y=is_delinquency
        )
    
    # Update layout with executive-ready formatting
    fig.update_layout(
        # Overall figure settings
        title=dict(
            text='Credit Market Risk Analysis Overview',
            font=dict(size=28, family='Arial', color='#2c3e50'),
            x=0.5,
            y=0.98,
            xanchor='center',
            yanchor='top'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12),
        width=1200,
        height=2400,
        margin=dict(t=100, l=80, r=40, b=60),
        
        # Two separate legends for different plot types
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.18,  # Position between time series and other plots
            xanchor="center",
            x=0.5,
            bgcolor='rgba(255, 255, 255, 0.9)',
            borderwidth=1,
            bordercolor='#E5E5E5',
            title=dict(text="Economic Period")
        ),
        legend2=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.02,  # Position at bottom
            xanchor="center",
            x=0.5,
            bgcolor='rgba(255, 255, 255, 0.9)',
            borderwidth=1,
            bordercolor='#E5E5E5',
            title=dict(text="Metrics")
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
    fig.update_xaxes(title_text="Current Option-Adjusted Spread", row=2, col=1)
    fig.update_yaxes(title_text="Current Loan Delinquency Rate (%)", row=2, col=1)
    
    fig.update_xaxes(title_text="Current Quarter Spread (basis points)", row=3, col=1)
    fig.update_yaxes(title_text="Next Quarter Delinquency Rate (%)", row=3, col=1)
    
    fig.update_xaxes(title_text="Year", row=4, col=1)
    fig.update_yaxes(title_text="Option-Adjusted Spread (basis points)", row=4, col=1, secondary_y=False)
    fig.update_yaxes(title_text="Delinquency Rate (%)", row=4, col=1, secondary_y=True)
    
    # Add source citation
    fig.add_annotation(
        text="Source: Federal Reserve Economic Data (FRED)",
        xref="paper",
        yref="paper",
        x=0.0,
        y=-0.05,
        showarrow=False,
        font=dict(size=11, color='#666666'),
        align='left'
    )
    
    # Export to PDF
    fig.write_image(output_path, format='pdf')
    
    return fig