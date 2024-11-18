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
├── fred_config.py        # FRED-specific configurations
├── analysis.ipynb       # Example Jupyter notebook
│
├── resources/           # Additional resource files
├── requirements.txt     # Python dependencies
└── fred_analysis.pdf   # PDF Export
```

## 💻 Usage

1. Configure your FRED API settings in `fred_config.py`

2. Basic usage example:
```python
from fred_loader import FREDLoader
from fred_transformer import FREDTransformer
from fred_visualizer import FREDVisualizer

# Initialize components
loader = FREDLoader()
transformer = FREDTransformer()
visualizer = FREDVisualizer()

# Load and process data
data = loader.get_series('GDP')
processed_data = transformer.transform(data)
visualizer.plot_series(processed_data)
```

3. For interactive analysis, open `analysis.ipynb` in Jupyter Notebook:
```bash
jupyter notebook analysis.ipynb
```

## 📊 Example Outputs

The project can generate various analyses and visualizations, which are saved in:
- `stats.xlsx` for statistical summaries
- `fred_analysis.pdf` for detailed analysis reports

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Commit changes: `git commit -m 'Add YourFeature'`
4. Push to branch: `git push origin feature/YourFeature`
5. Submit a Pull Request

## 📝 License

This project is licensed under the terms included in the LICENSE file.

## ⚠️ Prerequisites

- Python 3.8+
- FRED API Key (obtain from [FRED's API page](https://fred.stlouisfed.org/docs/api/api_key.html))
- Required Python packages (see requirements.txt)