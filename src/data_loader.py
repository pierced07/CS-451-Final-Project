import pandas as pd
from pathlib import Path

def load_raw_data():
    """
    Loads the raw appointment data from the data/raw directory.
    Uses __file__ to ensure paths work regardless of where the script is run from.
    """
    # Get the directory where this script lives (src/)
    current_dir = Path(__file__).parent 
    
    # Navigate up one level to project root, then into data/raw
    project_root = current_dir.parent 
    data_path = project_root / 'data' / 'raw' / 'appointments.csv'
    
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found at {data_path}. Please ensure data is downloaded.")
    
    df = pd.read_csv(data_path)
    return df

# Example usage when running this file directly
if __name__ == "__main__":
    df = load_raw_data()
    print(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns.")