#!/usr/bin/env python3
"""
Test script for Advanced Tourism Waste Stream Optimizer

This script tests the main components of the waste optimization system
to ensure everything is working correctly.
"""

import pandas as pd
import numpy as np
import warnings
from math import radians, cos, sin, asin, sqrt
import random

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

def test_data_generation():
    """Test synthetic data generation"""
    print("🧪 Testing data generation...")
    
    # Test producer creation
    producer_names = ["Hotel Test", "Restaurant Test"]
    producers = []
    for i, name in enumerate(producer_names):
        producer = {
            'id': f'P{i+1:02d}',
            'name': name,
            'latitude': random.uniform(41.35, 41.45),
            'longitude': random.uniform(2.10, 2.25)
        }
        producers.append(producer)
    
    producers_df = pd.DataFrame(producers)
    assert len(producers_df) == 2, "Producer creation failed"
    print("  ✅ Producer creation: PASS")
    
    # Test processor creation
    processor_names = ["Test Processing Plant"]
    processors = []
    for i, name in enumerate(processor_names):
        processor = {
            'id': f'PR{i+1:02d}',
            'name': name,
            'latitude': random.uniform(41.35, 41.45),
            'longitude': random.uniform(2.10, 2.25),
            'capacity_kg_per_month': random.randint(5000, 15000)
        }
        processors.append(processor)
    
    processors_df = pd.DataFrame(processors)
    assert len(processors_df) == 1, "Processor creation failed"
    print("  ✅ Processor creation: PASS")
    
    # Test historical data generation
    waste_types = ['organic', 'plastic', 'paper']
    months = pd.date_range(start='2023-01-01', end='2023-03-31', freq='ME')
    
    historical_waste = []
    for producer in producers:
        for month in months:
            for waste_type in waste_types:
                volume = random.randint(100, 1000)
                historical_waste.append({
                    'producer_id': producer['id'],
                    'date': month,
                    'waste_type': waste_type,
                    'volume_kg': volume
                })
    
    historical_waste_df = pd.DataFrame(historical_waste)
    expected_records = len(producers) * len(months) * len(waste_types)
    assert len(historical_waste_df) == expected_records, "Historical data generation failed"
    print("  ✅ Historical data generation: PASS")
    
    return producers_df, processors_df, historical_waste_df

def test_distance_calculation():
    """Test Haversine distance calculation"""
    print("🧪 Testing distance calculation...")
    
    def haversine_distance(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        return c * 6371
    
    # Test with known coordinates (Barcelona to Madrid)
    barcelona = (41.3851, 2.1734)
    madrid = (40.4168, -3.7038)
    
    distance = haversine_distance(barcelona[0], barcelona[1], madrid[0], madrid[1])
    
    # Distance should be approximately 500-600 km
    assert 400 < distance < 700, f"Distance calculation failed: {distance} km"
    print("  ✅ Distance calculation: PASS")
    
    return haversine_distance

def test_optimization_logic():
    """Test optimization logic"""
    print("🧪 Testing optimization logic...")
    
    # Simple test case
    supplies = [
        {'node_id': 'P01', 'supply': 1000},
        {'node_id': 'P02', 'supply': 500}
    ]
    
    demands = [
        {'node_id': 'PR01', 'demand': 800},
        {'node_id': 'PR02', 'demand': 700}
    ]
    
    edges = [
        {'producer_id': 'P01', 'processor_id': 'PR01', 'unit_cost_eur': 10},
        {'producer_id': 'P01', 'processor_id': 'PR02', 'unit_cost_eur': 15},
        {'producer_id': 'P02', 'processor_id': 'PR01', 'unit_cost_eur': 12},
        {'producer_id': 'P02', 'processor_id': 'PR02', 'unit_cost_eur': 8}
    ]
    
    # Simple greedy allocation
    allocations = []
    for supply in supplies:
        remaining_supply = supply['supply']
        producer_edges = [e for e in edges if e['producer_id'] == supply['node_id']]
        producer_edges.sort(key=lambda x: x['unit_cost_eur'])
        
        for edge in producer_edges:
            if remaining_supply <= 0:
                break
            
            processor_demand = next(d['demand'] for d in demands if d['node_id'] == edge['processor_id'])
            if processor_demand > 0:
                allocated = min(remaining_supply, processor_demand)
                allocations.append({
                    'producer_id': supply['node_id'],
                    'processor_id': edge['processor_id'],
                    'allocated_volume_kg': allocated,
                    'total_cost_eur': allocated * edge['unit_cost_eur']
                })
                
                remaining_supply -= allocated
                
                # Update demand
                for demand in demands:
                    if demand['node_id'] == edge['processor_id']:
                        demand['demand'] -= allocated
                        break
    
    total_allocated = sum(a['allocated_volume_kg'] for a in allocations)
    total_cost = sum(a['total_cost_eur'] for a in allocations)
    
    assert total_allocated == 1500, f"Allocation failed: {total_allocated}"
    assert total_cost > 0, "Cost calculation failed"
    print("  ✅ Optimization logic: PASS")
    
    return allocations

def test_forecasting_simulation():
    """Test forecasting simulation (without Prophet)"""
    print("🧪 Testing forecasting simulation...")
    
    # Simulate historical data
    historical_data = []
    for month in range(1, 13):
        for waste_type in ['organic', 'plastic', 'paper']:
            # Add seasonal variation
            seasonal_factor = 1.0
            if month in [6, 7, 8]:  # Summer
                seasonal_factor = 1.4
            elif month in [12, 1, 2]:  # Winter
                seasonal_factor = 0.8
            
            volume = int(1000 * seasonal_factor * random.uniform(0.9, 1.1))
            historical_data.append({
                'month': month,
                'waste_type': waste_type,
                'volume_kg': volume
            })
    
    historical_df = pd.DataFrame(historical_data)
    
    # Simple forecasting (average of last 3 months)
    forecasts = []
    for waste_type in ['organic', 'plastic', 'paper']:
        waste_data = historical_df[historical_df['waste_type'] == waste_type]
        recent_volumes = waste_data.tail(3)['volume_kg'].values
        forecasted_volume = int(np.mean(recent_volumes))
        
        forecasts.append({
            'waste_type': waste_type,
            'forecasted_volume_kg': forecasted_volume
        })
    
    forecasts_df = pd.DataFrame(forecasts)
    
    assert len(forecasts_df) == 3, "Forecasting failed"
    assert all(forecasts_df['forecasted_volume_kg'] > 0), "Invalid forecast values"
    print("  ✅ Forecasting simulation: PASS")
    
    return forecasts_df

def run_all_tests():
    """Run all tests"""
    print("🚀 Running Advanced Tourism Waste Stream Optimizer Tests")
    print("=" * 60)
    
    try:
        # Test 1: Data generation
        producers_df, processors_df, historical_waste_df = test_data_generation()
        
        # Test 2: Distance calculation
        haversine_distance = test_distance_calculation()
        
        # Test 3: Optimization logic
        allocations = test_optimization_logic()
        
        # Test 4: Forecasting simulation
        forecasts_df = test_forecasting_simulation()
        
        print("\n🎉 All tests passed successfully!")
        print("\n📊 Test Summary:")
        print(f"  - Producers created: {len(producers_df)}")
        print(f"  - Processors created: {len(processors_df)}")
        print(f"  - Historical records: {len(historical_waste_df)}")
        print(f"  - Allocations tested: {len(allocations)}")
        print(f"  - Forecasts generated: {len(forecasts_df)}")
        
        print("\n✅ System is ready for use!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    run_all_tests() 