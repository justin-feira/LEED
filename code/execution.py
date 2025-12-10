"""
LEED Data Processing Pipeline
Processes original_data.csv and buildings.csv to create final wide-format data with verification levels.
"""
import sys
from pathlib import Path

# Make sure the current directory (code/) is on sys.path so we can import sibling modules
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from data_cleaning import clean_and_transform_leed_data
from functions import breakdown_by_version, to_wide_var

# Building verification levels mapping
# IMPORTANT: Building names must EXACTLY match those in your CSV data
VERIFICATION_LEVELS = {
    'Lemon and Hardy Halls': 'Certified',
    'Rec Center Renovations': 'Certified',
    'Cohen Career Center': 'Gold',
    'Miller Hall (Mason School of Business': 'Gold',
    'School of Education': 'Gold',
    'Tucker Hall': 'Gold',
    'Chancellors Hall': 'Gold',
    'ISC 3': 'Gold',
    'Landrum Hall': 'Silver',
    'Marshall Wythe School of Law Addition': 'Silver',
    'McLeod Tyler Wellness Center': 'Gold',
    'Music Arts Center': 'Silver',
    'PBK Memorial Hall': 'Silver',
    'West Utility Plant': 'Gold',
    'Greek Fraternity Community Building': 'Silver',
    'House 620': 'Gold',
    'House 630': 'Gold',
    'House 640': 'Gold',
    'Houses 660, 670, 710, 720, 730, 740, 750, 760': 'Gold',
    'Alumni House Addition': 'Silver',
    'Campus Living Center': 'Silver',
    'Sadler West Expansion': 'Silver'
}

# Set up paths
repo_root = HERE.parent
data_dir = repo_root / "data_repository"

# Input paths
original_data_path = data_dir / "original_data" / "original_data.csv"
buildings_path = data_dir / "original_data" / "buildings.csv"

# Output paths
main_output_path = data_dir / "final_wide_data" / "cleaned_wide_data_cats.csv"
full_output_path = data_dir / "final_wide_data" / "cleaned_wide_data_full.csv"

def main():
    """
    Main execution function that processes LEED data from original files to final wide format.
    """
    # Update the verification levels in functions.py
    import functions
    functions.VERIFICATION_LEVELS = VERIFICATION_LEVELS
    
    # Clean output directory to remove old/duplicate files
    output_dir = data_dir / "final_wide_data"
    if output_dir.exists():
        print(f"Clearing output directory: {output_dir}")
        for file in output_dir.glob("*.csv"):
            file.unlink()
    
    print("="*60)
    print("LEED Data Processing Pipeline")
    print("="*60)
    print(f"Using verification levels for {len(VERIFICATION_LEVELS)} buildings")
    print("Note: All existing files in final_wide_data have been cleared")
    
    # Process categories-only data (default)
    print("\n1. Processing category data (categories_only=True)...")
    wide_data_cats = clean_and_transform_leed_data(
        inpath=original_data_path,
        outpath=main_output_path,
        buildings_source=buildings_path,
        categories_only=True
    )
    
    # Create version-specific files for categories
    print("\n2. Creating version-specific files for categories...")
    # First, get the cleaned long data for breakdown
    from data_cleaning import clean_leed_data
    cleaned_cats = clean_leed_data(original_data_path, buildings_path, categories_only=True)
    breakdown_by_version(cleaned_cats, function=to_wide_var, output_dir=data_dir / "final_wide_data")
    
    # Process full data (all types, not just categories)
    print("\n3. Processing full data (categories_only=False)...")
    wide_data_full = clean_and_transform_leed_data(
        inpath=original_data_path,
        outpath=full_output_path,
        buildings_source=buildings_path,
        categories_only=False
    )
    
    # Summary
    print("\n" + "="*60)
    print("PROCESSING COMPLETE")
    print("="*60)
    print(f"Categories data shape: {wide_data_cats.shape}")
    print(f"Full data shape: {wide_data_full.shape}")
    print(f"\nOutput files created:")
    print(f"  - Main categories: {main_output_path}")
    print(f"  - Full data: {full_output_path}")
    print(f"  - Version-specific files in: {data_dir / 'final_wide_data'}")
    
    # Show verification levels sample
    print(f"\nSample verification levels:")
    verification_sample = wide_data_cats[['building_name', 'verification_level']].head(3)
    print(verification_sample.to_string(index=False))
    
    # Check for any buildings without verification levels
    missing_verification = wide_data_cats[wide_data_cats['verification_level'].isna()]
    if len(missing_verification) > 0:
        print(f"\n⚠️  WARNING: {len(missing_verification)} buildings missing verification levels:")
        for building in missing_verification['building_name'].values:
            print(f"  - '{building}'")
        print("\n📝 To add verification levels for new buildings:")
        print("   1. Edit the VERIFICATION_LEVELS dictionary in execution.py")
        print("   2. Ensure building names EXACTLY match those in your CSV")
        print("   3. Re-run this script")
    
    return {
        'categories_data': wide_data_cats,
        'full_data': wide_data_full
    }

if __name__ == "__main__":
    results = main()