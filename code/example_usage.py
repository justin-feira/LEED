"""
Example usage of the simplified LEED data pipeline
"""
import sys
from pathlib import Path

# Add the code directory to path
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from data_cleaning import clean_and_transform_leed_data

# Example 1: Process local CSV file with categories only (default)
print("Example 1: Categories only (default)")
wide_data1 = clean_and_transform_leed_data(
    inpath="../data_repository/original_data/original_data.csv",
    outpath="../data_repository/temp/example1_output.csv",
    categories_only=True
)
print(f"Shape: {wide_data1.shape}")
print(f"Columns include verification_level: {'verification_level' in wide_data1.columns}")

print("\n" + "-"*50 + "\n")

# Example 2: Process with all data types (not just categories)
print("Example 2: All data types")
wide_data2 = clean_and_transform_leed_data(
    inpath="../data_repository/original_data/original_data.csv",
    outpath="../data_repository/temp/example2_output.csv",
    categories_only=False
)
print(f"Shape: {wide_data2.shape}")
print(f"Has verification levels: {'verification_level' in wide_data2.columns}")

print("\n" + "-"*50 + "\n")

# Example 3: Show how to use with Google Sheets
print("Example 3: Google Sheets usage")
print("""
# To use with Google Sheets, replace YOUR_SHEET_ID with actual sheet ID:
wide_data = clean_and_transform_leed_data(
    inpath="https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit",
    outpath="output/my_leed_data.csv"
)

# The function automatically converts the URL to CSV export format
# and processes the data exactly the same way
""")