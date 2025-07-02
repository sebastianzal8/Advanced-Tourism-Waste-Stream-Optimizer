"#!/usr/bin/env python3
"""
Advanced Tourism Waste Stream Optimizer

A comprehensive Python solution for analyzing, predicting, and optimizing 
waste management in tourism destinations using time-series forecasting, 
network optimization, and interactive visualization.

Author: Advanced Tourism Waste Stream Optimizer Team
"""

import pandas as pd
import numpy as np
from prophet import Prophet
import networkx as nx
import folium
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
import random
import string
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

class WasteOptimizer:
    """Main class for waste optimization system."""
    
    def __init__(self, random_seed=42):
        """Initialize the waste optimizer with random seed."""
        self.random_seed = random_seed
        random.seed(random_seed)
        np.random.seed(random_seed)
        
        # Barcelona city boundaries (approximate)
        self.barcelona_bounds = {
            'lat_min': 41.35, 'lat_max': 41.45,
            'lon_min': 2.10, 'lon_max': 2.25
        }
        
        # Initialize data containers
        self.producers_df = None
        self.processors_df = None
        self.historical_waste_df = None
        self.forecasts_df = None
        self.results_df = None
        self.network_graph = None
        
        print("✓ Waste Optimizer initialized successfully!")
    
    def generate_synthetic_data(self):
        """Generate synthetic tourism waste data."""
        print("🔧 Generating synthetic data...")
        
        # 1. Create waste producers (hotels/restaurants)
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
                'latitude': random.uniform(self.barcelona_bounds['lat_min'], self.barcelona_bounds['lat_max']),
                'longitude': random.uniform(self.barcelona_bounds['lon_min'], self.barcelona_bounds['lon_max'])
            }
            producers.append(producer)
        
        self.producers_df = pd.DataFrame(producers)
        print(f"✓ Created {len(self.producers_df)} waste producers")
        
        # 2. Create waste processors
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
                'latitude': random.uniform(self.barcelona_bounds['lat_min'], self.barcelona_bounds['lat_max']),
                'longitude': random.uniform(self.barcelona_bounds['lon_min'], self.barcelona_bounds['lon_max']),
                'capacity_kg_per_month': random.randint(5000, 15000)
            }
            processors.append(processor)
        
        self.processors_df = pd.DataFrame(processors)
        print(f"✓ Created {len(self.processors_df)} waste processors")
        
        # 3. Generate historical waste data (12 months)
        waste_types = ['organic', 'plastic', 'paper']
        months = pd.date_range(start='2023-01-01', end='2023-12-31', freq='ME')
        
        historical_waste = []
        
        for producer in producers:
            # Base waste generation (different for each producer)
            base_organic = random.randint(800, 2000)
            base_plastic = random.randint(200, 600)
            base_paper = random.randint(300, 800)
            
            for month in months:
                # Add seasonal variation (peak in summer months)
                seasonal_factor = 1.0
                if month.month in [6, 7, 8]:  # Summer months
                    seasonal_factor = 1.4  # 40% increase
                elif month.month in [12, 1, 2]:  # Winter months
                    seasonal_factor = 0.8  # 20% decrease
                
                # Add some random variation
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
        
        self.historical_waste_df = pd.DataFrame(historical_waste)
        print(f"✓ Generated {len(self.historical_waste_df)} historical waste records")
        
        # Display summary statistics
        print("\n📊 Summary Statistics:")
        print(f"Total waste generated: {self.historical_waste_df['volume_kg'].sum():,} kg")
        print(f"Average monthly waste per producer: {self.historical_waste_df.groupby('producer_id')['volume_kg'].sum().mean():.0f} kg")
        print(f"Total processor capacity: {self.processors_df['capacity_kg_per_month'].sum():,} kg/month")
    
    def forecast_waste_volumes(self):
        """Forecast future waste volumes using Prophet."""
        print("🔮 Starting time-series forecasting with Prophet...")
        
        waste_types = ['organic', 'plastic', 'paper']
        forecasts = []
        
        for producer_id in self.producers_df['id']:
            for waste_type in waste_types:
                # Get historical data for this producer and waste type
                data = self.historical_waste_df[
                    (self.historical_waste_df['producer_id'] == producer_id) & 
                    (self.historical_waste_df['waste_type'] == waste_type)
                ].copy()
                
                if len(data) == 0:
                    continue
                
                # Prepare data for Prophet
                prophet_data = data[['date', 'volume_kg']].rename(columns={
                    'date': 'ds',
                    'volume_kg': 'y'
                })
                
                # Create and fit Prophet model
                model = Prophet(
                    yearly_seasonality=True,
                    weekly_seasonality=False,
                    daily_seasonality=False,
                    seasonality_mode='additive'
                )
                
                try:
                    model.fit(prophet_data)
                    
                    # Create future dates for forecasting (next month)
                    future_dates = pd.DataFrame({
                        'ds': pd.date_range(
                            start=prophet_data['ds'].max() + pd.DateOffset(months=1),
                            periods=1,
                            freq='ME'
                        )
                    })
                    
                    # Make forecast
                    forecast = model.predict(future_dates)
                    
                    # Extract the forecasted value
                    forecasted_volume = int(forecast['yhat'].iloc[0])
                    forecasted_volume = max(0, forecasted_volume)  # Ensure non-negative
                    
                    forecasts.append({
                        'producer_id': producer_id,
                        'waste_type': waste_type,
                        'forecasted_volume_kg': forecasted_volume,
                        'lower_bound': int(forecast['yhat_lower'].iloc[0]),
                        'upper_bound': int(forecast['yhat_upper'].iloc[0])
                    })
                    
                except Exception as e:
                    print(f"⚠️ Error forecasting for {producer_id} - {waste_type}: {e}")
                    # Use simple average as fallback
                    avg_volume = int(data['volume_kg'].mean())
                    forecasts.append({
                        'producer_id': producer_id,
                        'waste_type': waste_type,
                        'forecasted_volume_kg': avg_volume,
                        'lower_bound': avg_volume,
                        'upper_bound': avg_volume
                    })
        
        self.forecasts_df = pd.DataFrame(forecasts)
        print(f"✓ Generated forecasts for {len(self.forecasts_df)} producer-waste type combinations")
        print(f"Total forecasted waste: {self.forecasts_df['forecasted_volume_kg'].sum():,} kg")
    
    def build_network(self):
        """Build transportation network using NetworkX."""
        print("🌐 Constructing waste transportation network...")
        
        # Create directed graph
        self.network_graph = nx.DiGraph()
        
        # Add producer nodes
        for _, producer in self.producers_df.iterrows():
            self.network_graph.add_node(producer['id'], 
                                       name=producer['name'],
                                       type='producer',
                                       latitude=producer['latitude'],
                                       longitude=producer['longitude'])
        
        # Add processor nodes
        for _, processor in self.processors_df.iterrows():
            self.network_graph.add_node(processor['id'],
                                       name=processor['name'],
                                       type='processor',
                                       latitude=processor['latitude'],
                                       longitude=processor['longitude'],
                                       capacity=processor['capacity_kg_per_month'])
        
        # Haversine formula
        def haversine_distance(lat1, lon1, lat2, lon2):
            """Calculate the great circle distance between two points."""
            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            r = 6371  # Radius of earth in kilometers
            return c * r
        
        # Add edges from each producer to each processor
        edges_added = 0
        for _, producer in self.producers_df.iterrows():
            for _, processor in self.processors_df.iterrows():
                # Calculate distance
                distance_km = haversine_distance(
                    producer['latitude'], producer['longitude'],
                    processor['latitude'], processor['longitude']
                )
                
                # Calculate unit cost (€2 per km)
                unit_cost_eur = distance_km * 2
                
                # Add edge with attributes
                self.network_graph.add_edge(producer['id'], processor['id'],
                                          distance_km=round(distance_km, 2),
                                          unit_cost_eur=round(unit_cost_eur, 2))
                edges_added += 1
        
        print(f"✓ Added {edges_added} edges (connections)")
        print(f"Total nodes: {self.network_graph.number_of_nodes()}")
        print(f"Total edges: {self.network_graph.number_of_edges()}")
    
    def optimize_transportation(self):
        """Optimize waste transportation using greedy algorithm."""
        print("⚡ Solving minimum-cost flow optimization...")
        
        waste_types = ['organic', 'plastic', 'paper']
        optimization_results = []
        
        for waste_type in waste_types:
            print(f"\n🔄 Optimizing for {waste_type} waste...")
            
            # Get forecasted volumes for this waste type
            waste_forecasts = self.forecasts_df[self.forecasts_df['waste_type'] == waste_type]
            
            # Create supply (producers) and demand (processors) data
            supplies = []
            demands = []
            
            # Add producers as supply nodes
            for _, forecast in waste_forecasts.iterrows():
                supplies.append({
                    'node_id': forecast['producer_id'],
                    'supply': int(forecast['forecasted_volume_kg'])
                })
            
            # Add processors as demand nodes
            for _, processor in self.processors_df.iterrows():
                demands.append({
                    'node_id': processor['id'],
                    'demand': int(processor['capacity_kg_per_month'])
                })
            
            # Calculate total supply and demand
            total_supply = sum(s['supply'] for s in supplies)
            total_demand = sum(d['demand'] for d in demands)
            
            print(f"  Total supply ({waste_type}): {total_supply:,} kg")
            print(f"  Total demand (capacity): {total_demand:,} kg")
            
            # Greedy allocation algorithm
            print("  🔄 Using greedy allocation algorithm...")
            
            # Sort producers by supply (largest first)
            supplies.sort(key=lambda x: x['supply'], reverse=True)
            
            # Create edges DataFrame for easier analysis
            edges_data = []
            for u, v, data in self.network_graph.edges(data=True):
                edges_data.append({
                    'producer_id': u,
                    'processor_id': v,
                    'producer_name': self.network_graph.nodes[u]['name'],
                    'processor_name': self.network_graph.nodes[v]['name'],
                    'distance_km': data['distance_km'],
                    'unit_cost_eur': data['unit_cost_eur']
                })
            edges_df = pd.DataFrame(edges_data)
            
            # Sort processors by cost (cheapest first for each producer)
            for supply in supplies:
                producer_id = supply['node_id']
                remaining_supply = supply['supply']
                
                # Get all possible connections for this producer
                connections = edges_df[edges_df['producer_id'] == producer_id].copy()
                connections = connections.sort_values('unit_cost_eur')  # Cheapest first
                
                for _, connection in connections.iterrows():
                    if remaining_supply <= 0:
                        break
                    
                    processor_id = connection['processor_id']
                    
                    # Find available capacity at this processor
                    processor_capacity = next(d['demand'] for d in demands if d['node_id'] == processor_id)
                    
                    if processor_capacity > 0:
                        # Allocate as much as possible
                        allocated = min(remaining_supply, processor_capacity)
                        
                        optimization_results.append({
                            'waste_type': waste_type,
                            'producer_id': producer_id,
                            'processor_id': processor_id,
                            'allocated_volume_kg': allocated,
                            'distance_km': connection['distance_km'],
                            'unit_cost_eur': connection['unit_cost_eur'],
                            'total_cost_eur': allocated * connection['unit_cost_eur']
                        })
                        
                        remaining_supply -= allocated
                        
                        # Update processor capacity
                        for demand in demands:
                            if demand['node_id'] == processor_id:
                                demand['demand'] -= allocated
                                break
            
            # Calculate total cost for this waste type
            waste_type_cost = sum(r['total_cost_eur'] for r in optimization_results if r['waste_type'] == waste_type)
            print(f"  Total cost for {waste_type}: €{waste_type_cost:,.2f}")
        
        # Create results DataFrame
        if optimization_results:
            self.results_df = pd.DataFrame(optimization_results)
            print(f"\n🎯 Optimization Complete!")
            print(f"Total allocations: {len(self.results_df)}")
            print(f"Total cost: €{self.results_df['total_cost_eur'].sum():,.2f}")
            
            # Summary by waste type
            print(f"\n📊 Cost Summary by Waste Type:")
            cost_summary = self.results_df.groupby('waste_type')['total_cost_eur'].sum()
            for waste_type, cost in cost_summary.items():
                print(f"  {waste_type}: €{cost:,.2f}")
        else:
            print("❌ No optimization results generated")
            self.results_df = pd.DataFrame()
    
    def create_visualizations(self):
        """Create interactive map and static visualizations."""
        print("🎨 Creating visualizations...")
        
        # 1. Interactive Folium Map
        print("🗺️ Creating interactive map...")
        
        # Center map on Barcelona
        barcelona_center = [41.3851, 2.1734]
        m = folium.Map(location=barcelona_center, zoom_start=12, tiles='OpenStreetMap')
        
        # Color scheme for producers (by total waste volume)
        producer_totals = self.forecasts_df.groupby('producer_id')['forecasted_volume_kg'].sum()
        max_waste = producer_totals.max()
        min_waste = producer_totals.min()
        
        def get_producer_color(waste_volume):
            """Get color based on waste volume (green to red)"""
            normalized = (waste_volume - min_waste) / (max_waste - min_waste)
            return f'#{int(255 * (1-normalized)):02x}{int(255 * normalized):02x}00'
        
        # Add producer markers
        for _, producer in self.producers_df.iterrows():
            total_waste = producer_totals.get(producer['id'], 0)
            color = get_producer_color(total_waste)
            
            folium.CircleMarker(
                location=[producer['latitude'], producer['longitude']],
                radius=8,
                popup=f"""
                <b>{producer['name']}</b><br>
                Total Forecasted Waste: {total_waste:,.0f} kg<br>
                ID: {producer['id']}
                """,
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7
            ).add_to(m)
        
        # Add processor markers
        for _, processor in self.processors_df.iterrows():
            # Size based on capacity
            size = 10 + (processor['capacity_kg_per_month'] / 1000)  # Scale with capacity
            
            folium.CircleMarker(
                location=[processor['latitude'], processor['longitude']],
                radius=size,
                popup=f"""
                <b>{processor['name']}</b><br>
                Capacity: {processor['capacity_kg_per_month']:,.0f} kg/month<br>
                ID: {processor['id']}
                """,
                color='purple',
                fill=True,
                fillColor='purple',
                fillOpacity=0.7
            ).add_to(m)
        
        # Add flow lines
        if not self.results_df.empty:
            for _, flow in self.results_df.iterrows():
                producer = self.producers_df[self.producers_df['id'] == flow['producer_id']].iloc[0]
                processor = self.processors_df[self.processors_df['id'] == flow['processor_id']].iloc[0]
                
                # Line thickness based on allocated volume
                weight = 1 + (flow['allocated_volume_kg'] / 1000)  # Scale with volume
                
                folium.PolyLine(
                    locations=[
                        [producer['latitude'], producer['longitude']],
                        [processor['latitude'], processor['longitude']]
                    ],
                    popup=f"""
                    <b>Waste Flow</b><br>
                    {producer['name']} → {processor['name']}<br>
                    Waste Type: {flow['waste_type']}<br>
                    Volume: {flow['allocated_volume_kg']:,.0f} kg<br>
                    Distance: {flow['distance_km']:.1f} km<br>
                    Cost: €{flow['total_cost_eur']:,.2f}
                    """,
                    weight=weight,
                    color='blue',
                    opacity=0.6
                ).add_to(m)
        
        # Save map
        m.save('waste_optimization_map.html')
        print("✅ Interactive map saved as 'waste_optimization_map.html'")
        
        # 2. Static visualizations
        if not self.results_df.empty:
            # Cost by Waste Type
            plt.figure(figsize=(10, 6))
            cost_by_type = self.results_df.groupby('waste_type')['total_cost_eur'].sum()
            colors = ['green', 'blue', 'orange']
            cost_by_type.plot(kind='bar', color=colors)
            plt.title('Total Transportation Cost by Waste Type')
            plt.ylabel('Cost (€)')
            plt.xlabel('Waste Type')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig('cost_by_waste_type.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print(f"📊 Total costs by waste type:")
            for waste_type, cost in cost_by_type.items():
                print(f"  {waste_type}: €{cost:,.2f}")
            
            # Distance Distribution
            plt.figure(figsize=(10, 6))
            plt.hist(self.results_df['distance_km'], bins=15, color='lightcoral', alpha=0.7, edgecolor='black')
            plt.title('Distribution of Transportation Distances')
            plt.xlabel('Distance (km)')
            plt.ylabel('Number of Allocations')
            plt.grid(True, alpha=0.3)
            plt.savefig('distance_distribution.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print(f"📏 Distance statistics:")
            print(f"  Average distance: {self.results_df['distance_km'].mean():.2f} km")
            print(f"  Min distance: {self.results_df['distance_km'].min():.2f} km")
            print(f"  Max distance: {self.results_df['distance_km'].max():.2f} km")
            
            # Capacity Utilization
            processor_utilization = self.results_df.groupby('processor_id')['allocated_volume_kg'].sum()
            processor_capacities = self.processors_df.set_index('id')['capacity_kg_per_month']
            
            plt.figure(figsize=(10, 6))
            utilization_pct = (processor_utilization / processor_capacities * 100).fillna(0)
            utilization_pct.plot(kind='bar', color='skyblue')
            plt.title('Processor Capacity Utilization')
            plt.ylabel('Utilization (%)')
            plt.xlabel('Processor ID')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig('capacity_utilization.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print(f"🏭 Processor utilization:")
            for proc_id, util in utilization_pct.items():
                print(f"  {proc_id}: {util:.1f}%")
        
        print("🎨 All visualizations complete!")
    
    def run_complete_analysis(self):
        """Run the complete waste optimization analysis."""
        print("🚀 Starting Advanced Tourism Waste Stream Optimization...")
        print("=" * 60)
        
        # Step 1: Generate synthetic data
        self.generate_synthetic_data()
        print()
        
        # Step 2: Forecast waste volumes
        self.forecast_waste_volumes()
        print()
        
        # Step 3: Build transportation network
        self.build_network()
        print()
        
        # Step 4: Optimize transportation
        self.optimize_transportation()
        print()
        
        # Step 5: Create visualizations
        self.create_visualizations()
        print()
        
        print("🎉 Analysis complete! Check the generated files:")
        print("  - waste_optimization_map.html (interactive map)")
        print("  - cost_by_waste_type.png (cost analysis)")
        print("  - distance_distribution.png (distance analysis)")
        print("  - capacity_utilization.png (utilization analysis)")


def main():
    """Main function to run the waste optimization system."""
    # Create and run the waste optimizer
    optimizer = WasteOptimizer(random_seed=42)
    optimizer.run_complete_analysis()


if __name__ == "__main__":
    main()" 
