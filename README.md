# Economic Indicator Analysis

A Python-based tool for fetching, transforming, and analyzing economic indicators from the Federal Reserve Economic Data (FRED) database.

## 📋 Project Overview

This project provides a suite of tools for working with FRED economic data, including data loading, transformation, and visualization capabilities. It enables users to perform sophisticated analysis on economic indicators through a modular Python framework.

## 🚀 Features

- Automated FRED data fetching
- Data transformation and preprocessing
- Statistical analysis tools
- Visualization capabilities
- Jupyter notebook integration for interactive analysis

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/econ_indicator_analysis.git
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

1. Configure your FRED API settings in `fred_config.py`

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
stats_table, current_plot, predictive_plot, time_series_plot = fred_visualize(df)

# Display all visualizations
stats_table.show()
current_plot.show()
predictive_plot.show()
time_series_plot.show()

# Export to PDF
fred_export(stats_table, current_plot, predictive_plot, time_series_plot)
```

## 📊 Example Outputs

The project generates various analyses and visualizations:
- `stats.xlsx`: Excel file containing transformed data and statistical summaries
- `fred_analysis.pdf`: PDF report containing:
  - Statistical summary table
  - Current economic indicators plot
  - Predictive analysis plot
  - Time series analysis plot

## 📝 License

This project is licensed under the terms included in the LICENSE file.

## ⚠️ Prerequisites

- Python 3.8+
- FRED API Key (obtain from [FRED's API page](https://fred.stlouisfed.org/docs/api/api_key.html))
- Required Python packages (see requirements.txt)