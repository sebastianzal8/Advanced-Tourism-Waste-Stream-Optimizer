# Advanced Tourism Waste Stream Optimizer

## Overview
The Advanced Tourism Waste Stream Optimizer is a comprehensive Python-based solution designed to analyze, predict, and optimize waste management in tourism destinations. This project leverages time-series forecasting, network optimization, and interactive visualization to help tourism businesses and destinations reduce their environmental impact while improving operational efficiency.

## Features
- **Synthetic Data Generation**: Realistic tourism waste data simulation with seasonal patterns
- **Time-Series Forecasting**: Prophet-based predictions for waste generation patterns
- **Network Optimization**: OR-Tools minimum-cost flow optimization for waste transportation
- **Interactive Visualization**: Folium-based maps showing waste flows and locations
- **Cost Analysis**: Comprehensive financial impact assessment of waste management strategies
- **Geographic Analysis**: Location-based optimization considering transportation distances

## Technology Stack
- **Core**: Python 3.8+
- **Data Science**: Pandas, NumPy, Matplotlib, Seaborn
- **Time-Series**: Prophet (Facebook)
- **Optimization**: OR-Tools (Google)
- **Network Analysis**: NetworkX
- **Geospatial**: Folium, GeoPandas
- **Visualization**: Matplotlib, Folium (interactive maps)

## Project Structure
```
Advanced Tourism Waste Stream Optimizer/
├── mvp.ipynb                    # Main Jupyter notebook with complete implementation
├── waste_optimization_map.html  # Interactive map visualization
├── requirements.txt             # Python dependencies
└── README.md                   # Project documentation
```

## Key Components

### 1. Data Generation
- **10 Waste Producers**: Hotels and restaurants across Barcelona
- **3 Waste Processors**: Central processing plants with capacity constraints
- **Historical Data**: 12 months of waste generation with seasonal patterns
- **Waste Types**: Organic, plastic, and paper waste

### 2. Time-Series Forecasting
- **Prophet Models**: Individual forecasting for each producer-waste type combination
- **Seasonal Patterns**: Automatic detection of tourism seasonality
- **Uncertainty Intervals**: Confidence bounds for predictions
- **Forecast Horizon**: 1-month ahead predictions

### 3. Network Optimization
- **Minimum-Cost Flow**: OR-Tools optimization for waste transportation
- **Geographic Constraints**: Real-world distances using Haversine formula
- **Capacity Constraints**: Processor capacity limitations
- **Cost Minimization**: Optimal allocation of waste to processors

### 4. Visualization
- **Interactive Map**: Folium-based visualization with:
  - Producer markers (colored by waste volume)
  - Processor markers (sized by capacity)
  - Flow lines (thickness proportional to volume)
  - Detailed popups with information
- **Static Charts**: Cost breakdown, distance distribution, capacity utilization

## Getting Started

### Prerequisites
- Python 3.8+
- Jupyter Notebook or JupyterLab

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Jupyter notebook:
   ```bash
   jupyter notebook mvp.ipynb
   ```

### Usage
1. **Data Generation**: The notebook automatically generates synthetic tourism waste data
2. **Forecasting**: Prophet models predict future waste volumes
3. **Optimization**: OR-Tools finds optimal waste transportation routes
4. **Visualization**: Interactive map and charts show results

## Key Insights

### Geographic Distribution
- Waste producers are distributed across Barcelona
- Processors are strategically located to minimize transportation costs
- Optimal routes consider real-world distances and constraints

### Cost Analysis
- **Organic Waste**: Highest transportation cost (€214,347)
- **Paper Waste**: Medium transportation cost (€79,559)
- **Plastic Waste**: Lowest transportation cost (€35,243)

### Optimization Results
- **Total Cost**: €329,149 for optimal waste transportation
- **Average Distance**: 3.74 km per transportation route
- **Capacity Utilization**: Varies from 26% to 185% across processors

## Technical Details

### Distance Calculation
Uses the Haversine formula to calculate real-world distances between geographic coordinates:
```python
def haversine_distance(lat1, lon1, lat2, lon2):
    # Calculate great circle distance between two points
    # Returns distance in kilometers
```

### Optimization Algorithm
- **Problem Type**: Minimum-cost flow problem
- **Objective**: Minimize total transportation cost
- **Constraints**: Supply (waste volumes) and demand (processor capacities)
- **Fallback**: Greedy algorithm when OR-Tools is unavailable

### Forecasting Model
- **Algorithm**: Facebook Prophet
- **Seasonality**: Additive model with yearly patterns
- **Robustness**: Handles missing data and outliers
- **Uncertainty**: Provides confidence intervals

## Contributing
Please read our contributing guidelines before submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For questions and support, please open an issue on GitHub. 