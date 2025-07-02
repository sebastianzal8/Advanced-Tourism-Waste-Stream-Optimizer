"""
Configuration file for Advanced Tourism Waste Stream Optimizer

This file contains all the configuration parameters and settings
used by the waste optimization system.
"""

# Random seed for reproducibility
RANDOM_SEED = 42

# Barcelona city boundaries (approximate)
BARCELONA_BOUNDS = {
    'lat_min': 41.35, 'lat_max': 41.45,
    'lon_min': 2.10, 'lon_max': 2.25
}

# Waste producer names
PRODUCER_NAMES = [
    "Hotel Barcelona Palace",
    "Restaurant La Rambla", 
    "Hotel Gothic Quarter",
    "Cafe Central",
    "Hotel Beachfront",
    "Restaurant Port Vell",
    "Hotel Eixample",
    "Cafe Gracia",
    "Hotel Montjuic",
    "Restaurant Born"
]

# Waste processor names
PROCESSOR_NAMES = [
    "Central Waste Processing Plant",
    "Recycling Center North",
    "Organic Waste Facility"
]

# Waste types
WASTE_TYPES = ['organic', 'plastic', 'paper']

# Transportation cost per kilometer (in euros)
COST_PER_KM = 2.0

# Prophet model parameters
PROPHET_CONFIG = {
    'yearly_seasonality': True,
    'weekly_seasonality': False,
    'daily_seasonality': False,
    'seasonality_mode': 'additive'
}

# Map visualization settings
MAP_CONFIG = {
    'center': [41.3851, 2.1734],  # Barcelona center
    'zoom_start': 12,
    'tiles': 'OpenStreetMap'
}

# Chart colors
CHART_COLORS = {
    'organic': 'green',
    'plastic': 'blue', 
    'paper': 'orange'
}

# File paths
OUTPUT_FILES = {
    'interactive_map': 'waste_optimization_map.html',
    'cost_analysis': 'cost_analysis.png',
    'distance_analysis': 'distance_analysis.png',
    'utilization_analysis': 'capacity_utilization.png'
} 