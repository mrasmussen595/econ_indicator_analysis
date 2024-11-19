# Economic Indicator Analysis

A Python-based tool for fetching, transforming, and analyzing economic indicators from the Federal Reserve Economic Data (FRED) database.

## 📋 Project Overview

This project provides a suite of tools for working with FRED economic data, including data loading, transformation, and visualization capabilities. It enables users to perform sophisticated analysis on economic indicators through a modular Python framework.

## 🔑 Getting Started with FRED API

Before using this tool, you'll need a FRED API key:

1. Visit the [FRED API Documentation](https://fred.stlouisfed.org/docs/api/api_key.html)
2. Log in or create a FRED account if you don't have one
3. Navigate to [FRED API Keys](https://fredaccount.stlouisfed.org/apikeys)
4. Click "Request API Key"
5. Save your API key for use in the next steps

> **Important**: 
> - Each developer should request a distinct API key for each application they build
> - Never share your API key or commit it to version control
> - You cannot request or view API keys without first logging into your fredaccount.stlouisfed.org user account
> - All web service requests require an API key to identify requests

## 🔐 Setting Up Your API Key

Create a `.env` file in the project root:
```
FRED_API_KEY=your_api_key_here
```

## 🚀 Features

- Automated FRED data fetching
- Data transformation and preprocessing
- Statistical analysis tools
- Visualization capabilities
- Jupyter notebook integration for interactive analysis

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/mrasmussen595/econ_indicator_analysis.git
cd econ_indicator_analysis
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your FRED API key:
```
FRED_API_KEY=your_api_key_here
```

## 📦 Project Structure

```
econ_indicator_analysis/
│
├── fred_loader.py        # Data loading from FRED API
├── fred_transformer.py   # Data transformation utilities
├── fred_visualizer.py    # Visualization tools
├── fred_config.py        # Environment considerations and parameters
├── analysis.ipynb       # Example Jupyter notebook
│
├── resources/           # Additional resource files
├── requirements.txt     # Python dependencies
└── fred_analysis.pdf   # PDF Export
```

## 💻 Usage

1. Configure economic indicators desired and observation start date in `fred_config.py`

2. For interactive analysis, open `analysis.ipynb` in Jupyter Notebook:
```bash
jupyter notebook analysis.ipynb
```

3. The notebook contains four main sections:

### Data Loading
```python
# Import required libraries
%load_ext autoreload
%autoreload 2

from IPython.display import display
from fred_loader import fred_load
from fred_transformer import fred_transform
from fred_visualizer import fred_export, fred_visualize

# Load FRED data
df = fred_load()
print("Data loaded successfully!")
display(df)
```

### Data Transformation
```python
# Transform data with specified start date
df = fred_transform(df, start_date='1996-12-31')
print("Transformation complete!")
display(df)

# Export to Excel
df.to_excel('stats.xlsx')
```

### Visualization and Export
```python
# Generate visualizations
stats_table, covid_plot, pregfc_plot, time_series_plot = fred_visualize(df)

# Display all visualizations
stats_table.show() # Summary stats table
covid_plot.show() # Built-in analysis of OAS vs Loan Delinquency indicators for covid to present (2020-2024)
pregfc_plot.show() # Built-in analysis of OAS vs Loan Delinquency indicators for Pre-GFC (1996-2007)
time_series_plot.show() # Time Series plot comparing two indicators

# Export to PDF
fred_export(stats_table, covid_plot, pregfc_plot, time_series_plot)
```

## 📊 Example Outputs

The project generates various analyses and visualizations:
- `stats.xlsx`: Excel file containing transformed data and statistical summaries
- `fred_analysis.pdf`: PDF report containing:
  - Statistical summary table
  - Scatterplot of OAS vs Loan Delinquency indicators for covid to present (2020-2024)
  - Scatterplot of OAS vs Loan Delinquency indicators for Pre-GFC (1996-2007)
  - Time series analysis plot

## 📝 License

This project is licensed under the terms included in the LICENSE file.

## ⚠️ Prerequisites

- Python 3.8+
- FRED API Key (obtain from [FRED's API page](https://fred.stlouisfed.org/docs/api/api_key.html))
- Required Python packages (see requirements.txt)
