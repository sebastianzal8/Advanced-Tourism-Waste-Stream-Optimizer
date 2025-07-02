#!/usr/bin/env python3
"""
Setup script for Advanced Tourism Waste Stream Optimizer

This script helps users install dependencies and set up the environment
for running the waste optimization system.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages from requirements.txt"""
    print("📦 Installing required packages...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def check_dependencies():
    """Check if all required packages are available"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'pandas', 'numpy', 'prophet', 'networkx', 
        'folium', 'matplotlib', 'seaborn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies are available!")
        return True

def create_sample_data():
    """Create sample data files for testing"""
    print("📊 Creating sample data...")
    
    # This would create sample CSV files for testing
    # For now, just create a placeholder
    sample_data_dir = "sample_data"
    if not os.path.exists(sample_data_dir):
        os.makedirs(sample_data_dir)
        print(f"  ✅ Created {sample_data_dir} directory")

def main():
    """Main setup function"""
    print("🚀 Advanced Tourism Waste Stream Optimizer Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Setup failed during dependency check")
        sys.exit(1)
    
    # Create sample data
    create_sample_data()
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the Jupyter notebook: jupyter notebook mvp.ipynb")
    print("2. Or run the Python script: python waste_optimizer.py")
    print("3. Open waste_optimization_map.html to view the interactive map")
    
    print("\n📚 Documentation:")
    print("- README.md: Project overview and usage instructions")
    print("- mvp.ipynb: Complete implementation with explanations")
    print("- config.py: Configuration parameters")

if __name__ == "__main__":
    main() 