# LEED Data Cleaning & Processing Pipeline
**Author:** Justin Feira  
**Date Created:** 10/27/2025  
**Last Updated:** 12/10/2025

Code referenced in LEED process documentation. Transforms base spreadsheet data into ArcGIS ready wide form data with building certification levels.

This code was written for the LEED project at the Center for Geospatial Analysis at William and Mary. The purpose is to transform the base LEED data, transcribed literally in spreadsheets (original data available in the LEED Google Drive under "LEED Data Structure"), into wide form, spatial join ready data.

## Quick Start Tutorial

### 1. Clone the Repository
```bash
# Clone the repository to your local machine
git clone https://github.com/your-username/LEED_data_cleaning_f25.git
cd LEED_data_cleaning_f25

# Install required dependencies
pip install pandas requests pathlib
```

### 2. Repository Structure
```
LEED/
├── README.md
├── code/
│   ├── execution.py          # Main script - run this!
│   ├── data_cleaning.py      # Core processing functions
│   └── functions.py          # Helper functions
├── data_repository/
│   └── original_data/
│       ├── original_data.csv # Raw LEED data
│       └── buildings.csv     # Building information
└── final_wide_data/          # Output files (generated)
    ├── cleaned_wide_data_cats.csv     # Categories only
    ├── cleaned_wide_data_full.csv     # All data types
    ├── cleaned_wide_leed_data_2_2.csv # LEED 2.2 buildings
    ├── cleaned_wide_leed_data_3_0.csv # LEED 3.0 buildings
    └── cleaned_wide_leed_data_4_0.csv # LEED 4.0 buildings
```

### 3. Adding New Data

#### Step 3a: Update the Master Sheet
1. Open the **LEED Data Structure** Google Sheet (available in LEED Google Drive)
2. Add new building data following the existing format:
   - **Building Name**: Exact building name
   - **Category**: LEED category 
   - **Credit Name**: Specific LEED credit
   - **Points Earned**: Numerical points value
   - **Points Available**: Total points possible
   - **LEED Version**: Version number
   - **Data Type**: Usually "Category" for most entries

#### Step 3b: Export Updated Data
1. Download the updated Google Sheet as CSV
2. Save it as `original_data.csv` in `data_repository/original_data/`
3. **For new buildings**: Add verification levels in `code/execution.py`:
   - Open `execution.py` and find the `VERIFICATION_LEVELS` dictionary
   - Add your new building with exact name matching the CSV: `'Building Name': 'Gold'` (or 'Silver'/'Certified')
   - Building names must EXACTLY match those in your CSV data

### 4. Generate Updated Wide Form Data

#### Option A: Complete Pipeline (Recommended)
Run the main execution script to process everything:

```bash
cd code
python execution.py
```

This will:
- **Automatically clear old data** from final_wide_data folder
- Process the raw data
- Clean and transform it
- Generate wide-form data for all buildings
- Create version-specific files (LEED 2.2, 3.0, 4.0)
- Add building certification levels (Gold, Silver, Certified)
- **Warn you** if any buildings are missing verification levels

#### Option B: Custom Processing
For more control, use the core function directly:

```python
from data_cleaning import clean_and_transform_leed_data

# Categories only (default)
wide_data = clean_and_transform_leed_data(
    inpath="../data_repository/original_data/original_data.csv",
    outpath="../final_wide_data/my_custom_output.csv"
)

# All data types
wide_data = clean_and_transform_leed_data(
    inpath="../data_repository/original_data/original_data.csv",
    outpath="../final_wide_data/full_data.csv",
    categories_only=False
)
```

### 5. Output Files Explained

After running the pipeline, you'll get:

- **`cleaned_wide_data_cats.csv`**: Main file with category data only (recommended for most analysis)
- **`cleaned_wide_data_full.csv`**: Complete dataset including all data types
- **`cleaned_wide_leed_data_X_X.csv`**: Version-specific files for targeted analysis
- **`verification_level` column**: Added to all files showing certification level (Gold/Silver/Certified)

### 6. Using the Data

The wide-form data is ready for:
- **ArcGIS spatial joins**: Each building is one row with all LEED categories as columns
- **Statistical analysis**: Easy comparison across buildings and categories
- **Visualization**: Direct input into plotting libraries

### 7. Managing Building Verification Levels

**Adding New Buildings:**
1. Open `code/execution.py`
2. Find the `VERIFICATION_LEVELS` dictionary (around line 15)
3. Add your building with exact name matching:
   ```python
   'Your Building Name': 'Gold',  # or 'Silver' or 'Certified'
   ```
4. **Critical**: Building name must EXACTLY match what appears in your CSV
5. Run the pipeline - it will warn you if any buildings are still missing


### 8. Troubleshooting

**Common Issues:**
- **File not found**: Ensure `original_data.csv` and `buildings.csv` are in the correct directory
- **Missing verification levels**: 
  - Check that building names in your CSV EXACTLY match those in the `VERIFICATION_LEVELS` dictionary in `execution.py`
  - The script will show a warning with missing building names
  - Add missing buildings to the dictionary with exact name matching
- **Empty output**: Verify the Google Sheet export format matches the expected structure
- **Old data persisting**: The script automatically clears the output folder, but check permissions if files remain

**Getting Help:**
- Check the console output for specific error messages
- Verify data formatting matches existing entries in the master sheet
- Contact the Center for Geospatial Analysis for access to the LEED Google Drive

## Data Repository
Contains original long form CSV files along with the processed results.

## Functions
- `clean_and_transform_leed_data()`: Main pipeline function
- `to_wide_var()`: Transforms long data to wide format
- `version_data()`: Filters data by LEED version

---
*For questions or issues, send me a message on github or at justinfeira@gmail.com*