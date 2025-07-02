#!/usr/bin/env python3
"""
Example Usage of Advanced Tourism Waste Stream Optimizer

This script demonstrates how to use the waste optimization system
to analyze and optimize waste management in tourism destinations.

Run this script to see the complete analysis in action.
"""

import pandas as pd
import numpy as np
from prophet import Prophet
import networkx as nx
import folium
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
import random
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

def main():
    """Run the complete waste optimization analysis."""
    print("🚀 Advanced Tourism Waste Stream Optimizer")
    print("=" * 50)
    
    # Set random seed for reproducibility
    random.seed(42)
    np.random.seed(42)
    
    # Barcelona city boundaries
    barcelona_bounds = {
        'lat_min': 41.35, 'lat_max': 41.45,
        'lon_min': 2.10, 'lon_max': 2.25
    }
    
    print("1. 🔧 Generating synthetic data...")
    
    # Create waste producers
    producer_names = [
        "Hotel Barcelona Palace", "Restaurant La Rambla", "Hotel Gothic Quarter",
        "Cafe Central", "Hotel Beachfront", "Restaurant Port Vell",
        "Hotel Eixample", "Cafe Gracia", "Hotel Montjuic", "Restaurant Born"
    ]
    
    producers = []
    for i, name in enumerate(producer_names):
        producer = {
            'id': f'P{i+1:02d}',
            'name': name,
            'latitude': random.uniform(barcelona_bounds['lat_min'], barcelona_bounds['lat_max']),
            'longitude': random.uniform(barcelona_bounds['lon_min'], barcelona_bounds['lon_max'])
        }
        producers.append(producer)
    
    producers_df = pd.DataFrame(producers)
    print(f"   ✓ Created {len(producers_df)} waste producers")
    
    # Create waste processors
    processor_names = [
        "Central Waste Processing Plant",
        "Recycling Center North", 
        "Organic Waste Facility"
    ]
    
    processors = []
    for i, name in enumerate(processor_names):
        processor = {
            'id': f'PR{i+1:02d}',
            'name': name,
            'latitude': random.uniform(barcelona_bounds['lat_min'], barcelona_bounds['lat_max']),
            'longitude': random.uniform(barcelona_bounds['lon_min'], barcelona_bounds['lon_max']),
            'capacity_kg_per_month': random.randint(5000, 15000)
        }
        processors.append(processor)
    
    processors_df = pd.DataFrame(processors)
    print(f"   ✓ Created {len(processors_df)} waste processors")
    
    # Generate historical waste data
    waste_types = ['organic', 'plastic', 'paper']
    months = pd.date_range(start='2023-01-01', end='2023-12-31', freq='ME')
    
    historical_waste = []
    for producer in producers:
        base_organic = random.randint(800, 2000)
        base_plastic = random.randint(200, 600)
        base_paper = random.randint(300, 800)
        
        for month in months:
            seasonal_factor = 1.0
            if month.month in [6, 7, 8]:  # Summer months
                seasonal_factor = 1.4
            elif month.month in [12, 1, 2]:  # Winter months
                seasonal_factor = 0.8
            
            random_factor = random.uniform(0.9, 1.1)
            
            for waste_type in waste_types:
                if waste_type == 'organic':
                    base_volume = base_organic
                elif waste_type == 'plastic':
                    base_volume = base_plastic
                else:  # paper
                    base_volume = base_paper
                
                volume = int(base_volume * seasonal_factor * random_factor)
                
                historical_waste.append({
                    'producer_id': producer['id'],
                    'date': month,
                    'waste_type': waste_type,
                    'volume_kg': volume
                })
    
    historical_waste_df = pd.DataFrame(historical_waste)
    print(f"   ✓ Generated {len(historical_waste_df)} historical waste records")
    
    print("\n2. 🔮 Forecasting waste volumes...")
    
    # Time-series forecasting with Prophet
    forecasts = []
    for producer_id in producers_df['id']:
        for waste_type in waste_types:
            data = historical_waste_df[
                (historical_waste_df['producer_id'] == producer_id) & 
                (historical_waste_df['waste_type'] == waste_type)
            ].copy()
            
            if len(data) == 0:
                continue
            
            prophet_data = data[['date', 'volume_kg']].rename(columns={
                'date': 'ds',
                'volume_kg': 'y'
            })
            
            model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=False,
                daily_seasonality=False,
                seasonality_mode='additive'
            )
            
            try:
                model.fit(prophet_data)
                
                future_dates = pd.DataFrame({
                    'ds': pd.date_range(
                        start=prophet_data['ds'].max() + pd.DateOffset(months=1),
                        periods=1,
                        freq='ME'
                    )
                })
                
                forecast = model.predict(future_dates)
                forecasted_volume = max(0, int(forecast['yhat'].iloc[0]))
                
                forecasts.append({
                    'producer_id': producer_id,
                    'waste_type': waste_type,
                    'forecasted_volume_kg': forecasted_volume
                })
                
            except Exception as e:
                # Use simple average as fallback
                avg_volume = int(data['volume_kg'].mean())
                forecasts.append({
                    'producer_id': producer_id,
                    'waste_type': waste_type,
                    'forecasted_volume_kg': avg_volume
                })
    
    forecasts_df = pd.DataFrame(forecasts)
    print(f"   ✓ Generated forecasts for {len(forecasts_df)} combinations")
    print(f"   ✓ Total forecasted waste: {forecasts_df['forecasted_volume_kg'].sum():,} kg")
    
    print("\n3. 🌐 Building transportation network...")
    
    # Haversine distance function
    def haversine_distance(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        return c * 6371  # Earth radius in km
    
    # Create network edges
    edges_data = []
    for _, producer in producers_df.iterrows():
        for _, processor in processors_df.iterrows():
            distance_km = haversine_distance(
                producer['latitude'], producer['longitude'],
                processor['latitude'], processor['longitude']
            )
            unit_cost_eur = distance_km * 2  # €2 per km
            
            edges_data.append({
                'producer_id': producer['id'],
                'processor_id': processor['id'],
                'distance_km': round(distance_km, 2),
                'unit_cost_eur': round(unit_cost_eur, 2)
            })
    
    edges_df = pd.DataFrame(edges_data)
    print(f"   ✓ Created {len(edges_df)} transportation connections")
    
    print("\n4. ⚡ Optimizing transportation...")
    
    # Simple greedy optimization
    optimization_results = []
    
    for waste_type in waste_types:
        waste_forecasts = forecasts_df[forecasts_df['waste_type'] == waste_type]
        
        # Sort producers by supply (largest first)
        supplies = []
        for _, forecast in waste_forecasts.iterrows():
            supplies.append({
                'node_id': forecast['producer_id'],
                'supply': int(forecast['forecasted_volume_kg'])
            })
        supplies.sort(key=lambda x: x['supply'], reverse=True)
        
        # Initialize processor capacities
        demands = []
        for _, processor in processors_df.iterrows():
            demands.append({
                'node_id': processor['id'],
                'demand': int(processor['capacity_kg_per_month'])
            })
        
        # Allocate waste using greedy algorithm
        for supply in supplies:
            producer_id = supply['node_id']
            remaining_supply = supply['supply']
            
            # Get connections for this producer, sorted by cost
            connections = edges_df[edges_df['producer_id'] == producer_id].copy()
            connections = connections.sort_values('unit_cost_eur')
            
            for _, connection in connections.iterrows():
                if remaining_supply <= 0:
                    break
                
                processor_id = connection['processor_id']
                processor_capacity = next(d['demand'] for d in demands if d['node_id'] == processor_id)
                
                if processor_capacity > 0:
                    allocated = min(remaining_supply, processor_capacity)
                    
                    optimization_results.append({
                        'waste_type': waste_type,
                        'producer_id': producer_id,
                        'processor_id': processor_id,
                        'allocated_volume_kg': allocated,
                        'distance_km': connection['distance_km'],
                        'total_cost_eur': allocated * connection['unit_cost_eur']
                    })
                    
                    remaining_supply -= allocated
                    
                    # Update processor capacity
                    for demand in demands:
                        if demand['node_id'] == processor_id:
                            demand['demand'] -= allocated
                            break
    
    results_df = pd.DataFrame(optimization_results)
    print(f"   ✓ Optimized {len(results_df)} waste allocations")
    print(f"   ✓ Total cost: €{results_df['total_cost_eur'].sum():,.2f}")
    
    print("\n5. 🎨 Creating visualizations...")
    
    # Create interactive map
    barcelona_center = [41.3851, 2.1734]
    m = folium.Map(location=barcelona_center, zoom_start=12, tiles='OpenStreetMap')
    
    # Add producer markers
    producer_totals = forecasts_df.groupby('producer_id')['forecasted_volume_kg'].sum()
    for _, producer in producers_df.iterrows():
        total_waste = producer_totals.get(producer['id'], 0)
        
        folium.CircleMarker(
            location=[producer['latitude'], producer['longitude']],
            radius=8,
            popup=f"<b>{producer['name']}</b><br>Waste: {total_waste:,.0f} kg",
            color='red',
            fill=True,
            fillOpacity=0.7
        ).add_to(m)
    
    # Add processor markers
    for _, processor in processors_df.iterrows():
        size = 10 + (processor['capacity_kg_per_month'] / 1000)
        
        folium.CircleMarker(
            location=[processor['latitude'], processor['longitude']],
            radius=size,
            popup=f"<b>{processor['name']}</b><br>Capacity: {processor['capacity_kg_per_month']:,.0f} kg/month",
            color='purple',
            fill=True,
            fillOpacity=0.7
        ).add_to(m)
    
    # Add flow lines
    for _, flow in results_df.iterrows():
        producer = producers_df[producers_df['id'] == flow['producer_id']].iloc[0]
        processor = processors_df[processors_df['id'] == flow['processor_id']].iloc[0]
        
        weight = 1 + (flow['allocated_volume_kg'] / 1000)
        
        folium.PolyLine(
            locations=[
                [producer['latitude'], producer['longitude']],
                [processor['latitude'], processor['longitude']]
            ],
            popup=f"Waste Flow: {flow['waste_type']}<br>Volume: {flow['allocated_volume_kg']:,.0f} kg<br>Cost: €{flow['total_cost_eur']:,.2f}",
            weight=weight,
            color='blue',
            opacity=0.6
        ).add_to(m)
    
    # Save map
    m.save('waste_optimization_map.html')
    print("   ✅ Interactive map saved as 'waste_optimization_map.html'")
    
    # Create cost analysis chart
    if not results_df.empty:
        plt.figure(figsize=(10, 6))
        cost_by_type = results_df.groupby('waste_type')['total_cost_eur'].sum()
        cost_by_type.plot(kind='bar', color=['green', 'blue', 'orange'])
        plt.title('Total Transportation Cost by Waste Type')
        plt.ylabel('Cost (€)')
        plt.xlabel('Waste Type')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('cost_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("   ✅ Cost analysis chart saved as 'cost_analysis.png'")
        
        print(f"\n📊 Cost Summary:")
        for waste_type, cost in cost_by_type.items():
            print(f"   {waste_type}: €{cost:,.2f}")
    
    print("\n🎉 Analysis complete!")
    print("Generated files:")
    print("  - waste_optimization_map.html (interactive map)")
    print("  - cost_analysis.png (cost breakdown)")
    print("\nKey insights:")
    print(f"  - Total waste forecasted: {forecasts_df['forecasted_volume_kg'].sum():,} kg")
    print(f"  - Total transportation cost: €{results_df['total_cost_eur'].sum():,.2f}")
    print(f"  - Average distance: {results_df['distance_km'].mean():.2f} km")


if __name__ == "__main__":
    main() 