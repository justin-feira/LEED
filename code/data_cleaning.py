'''
Purpose: Integrated data cleaning and wide format transformation pipeline
Last updated: 12-10-25

Functions:
- clean_and_transform_leed_data: Main pipeline function that handles everything from raw data to wide format
- clean_leed_data: Helper function that performs data cleaning steps
'''

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Make sure we can import functions from the same directory
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from functions import to_wide_var, breakdown_by_version, VERIFICATION_LEVELS

# Determine repository root (assumes this file is in <repo>/code/)
REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data_repository"


def clean_leed_data(data_source, buildings_source=None, categories_only=True):
    """
    Clean LEED data from various sources.
    
    Parameters:
    - data_source: str or DataFrame - Path to CSV, Google Sheets URL, or DataFrame
    - buildings_source: str or DataFrame - Path to buildings mapping CSV or DataFrame
    - categories_only: bool - If True, filter to only category data (default: True)
    
    Returns:
    - pandas.DataFrame: Cleaned long-form data
    """
    # Load main data
    if isinstance(data_source, pd.DataFrame):
        leed = data_source.copy()
    elif isinstance(data_source, (str, Path)):
        data_source_str = str(data_source)
        if data_source_str.startswith('http'):
            # Handle Google Sheets URLs
            if '/edit' in data_source_str:
                # Convert Google Sheets edit URL to CSV export URL
                sheet_id = data_source_str.split('/d/')[1].split('/')[0]
                csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
                leed = pd.read_csv(csv_url)
            else:
                leed = pd.read_csv(data_source_str)
        else:
            leed = pd.read_csv(data_source_str)
    else:
        raise ValueError("data_source must be a DataFrame, file path, or URL")
    
    # Load buildings mapping
    if buildings_source is None:
        buildings_df = pd.read_csv(DATA_DIR / "original_data" / "buildings.csv")
    elif isinstance(buildings_source, pd.DataFrame):
        buildings_df = buildings_source.copy()
    else:
        buildings_df = pd.read_csv(str(buildings_source))
    
    # Create mapping dictionaries
    buildings = dict(zip(buildings_df['building_code'], buildings_df['building']))
    leed_versions = dict(zip(buildings_df['building_code'], buildings_df['leed_code']))
    
    # Map building names and leed versions to main dataframe
    leed['building_name'] = leed['building_code'].map(buildings)
    leed['leed_version'] = leed['building_code'].map(leed_versions)
    
    # Create points_earned column
    leed['points_earned'] = leed['awarded_points'].astype(str) + "/" + leed['potential_points'].astype(str)
    
    # Create cat_and_cat_name column
    leed['cat_and_cat_name'] = leed['cat_code'] + " - " + leed['cat']
    
    # Ensure proper data types
    leed['building_code'] = leed['building_code'].astype(str)
    leed['points_earned'] = leed['points_earned'].astype(str)
    
    # Replace 0/0 with prerequisite
    leed['points_earned'] = leed['points_earned'].replace("0/0", "prerequisite")
    
    # Clean leed_version formatting
    leed['leed_version'] = (leed['leed_version']
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r'^(v|leed[\s-]*)', '', regex=True)
        .str.replace(r'\.0$', '', regex=True)
        .str.replace('_', '.', regex=False)
        .str.strip()
    )
    
    # Filter to categories only if requested
    if categories_only:
        leed = leed[leed['type'] == 'cat'].copy()
        # Create category-specific cat_and_cat_name
        leed['cat_and_cat_name'] = (leed['cat_code'].astype(str) + "(" + 
                                   leed['potential_points'].astype(str) + ")" + 
                                   'v' + leed['leed_version'].astype(str))
    
    return leed


def clean_and_transform_leed_data(inpath, outpath, buildings_source=None, categories_only=True):
    """
    Complete pipeline: clean data and transform to wide format with verification levels.
    
    Parameters:
    - inpath: str - Path to input CSV file or Google Sheets URL
    - outpath: str - Path where the final wide CSV will be saved
    - buildings_source: str or DataFrame - Path to buildings mapping CSV or DataFrame  
    - categories_only: bool - If True, filter to only category data (default: True)
    
    Returns:
    - pandas.DataFrame: Wide-format DataFrame with verification levels
    """
    # Clean the data
    print("Cleaning LEED data...")
    cleaned_data = clean_leed_data(inpath, buildings_source, categories_only)
    
    # Transform to wide format
    print("Transforming to wide format...")
    wide_data = to_wide_var(cleaned_data)
    
    # Save to output path
    outpath = Path(outpath)
    outpath.parent.mkdir(parents=True, exist_ok=True)
    wide_data.to_csv(outpath, index=False)
    print(f"Saved wide data to: {outpath}")
    
    return wide_data


def demo_usage():
    """
    Demonstrates how to use the simplified pipeline.
    """
    print("\n" + "="*50)
    print("DEMO: Using simplified LEED data pipeline")
    print("="*50)
    
    print(f"""
Usage examples:

1. Local CSV file:
    wide_data = clean_and_transform_leed_data(
        inpath="data/original_data.csv",
        outpath="output/cleaned_wide_data.csv"
    )

2. Google Sheets URL:
    wide_data = clean_and_transform_leed_data(
        inpath="https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit",
        outpath="output/cleaned_wide_data.csv"
    )

3. All data types (not just categories):
    wide_data = clean_and_transform_leed_data(
        inpath="data.csv",
        outpath="output.csv",
        categories_only=False
    )

The function returns the wide DataFrame and saves it to the specified output path.
""")


# Example usage and backward compatibility
if __name__ == "__main__":
    # Default behavior - process existing data files
    print("Running simplified LEED data pipeline...")
    
    # Process with categories only (default)
    wide_data = clean_and_transform_leed_data(
        inpath=DATA_DIR / "original_data" / "original_data.csv",
        outpath=DATA_DIR / "final_wide_data" / "cleaned_wide_data_cats.csv",
        categories_only=True
    )
    
    print(f"Processing complete!")
    print(f"Wide data shape: {wide_data.shape}")
    
    # Show demo usage
    demo_usage()