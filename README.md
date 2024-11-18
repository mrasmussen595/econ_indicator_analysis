# Economic Indicator Analysis
A Python-based tool for fetching, transforming, and analyzing economic indicators from the Federal Reserve Economic Data (FRED) database.
📋 Project Overview
This project provides a suite of tools for working with FRED economic data, including data loading, transformation, and visualization capabilities. It enables users to perform sophisticated analysis on economic indicators through a modular Python framework.
🚀 Features

Automated FRED data fetching
Data transformation and preprocessing
Statistical analysis tools
Visualization capabilities
Jupyter notebook integration for interactive analysis

🛠️ Installation

Clone the repository:

bashCopygit clone https://github.com/yourusername/econ_indicator_analysis.git
cd econ_indicator_analysis

Create and activate a virtual environment:

bashCopypython -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate

Install dependencies:

bashCopypip install -r requirements.txt

Create a .env file with your FRED API key:

envCopyFRED_API_KEY=your_api_key_here
📦 Project Structure
Copyecon_indicator_analysis/
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

💻 Usage

Configure your FRED API settings in fred_config.py
Basic usage example:

pythonCopyfrom fred_loader import FREDLoader
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

For interactive analysis, open analysis.ipynb in Jupyter Notebook:

bashCopyjupyter notebook analysis.ipynb
📊 Example Outputs
The project can generate various analyses and visualizations, which are saved in:

stats.xlsx for statistical summaries
fred_analysis.pdf for detailed analysis reports

🤝 Contributing

Fork the repository
Create a feature branch: git checkout -b feature/YourFeature
Commit changes: git commit -m 'Add YourFeature'
Push to branch: git push origin feature/YourFeature
Submit a Pull Request

📝 License
This project is licensed under the terms included in the LICENSE file.
⚠️ Prerequisites

Python 3.8+
FRED API Key (obtain from FRED's API page)
Required Python packages (see requirements.txt)