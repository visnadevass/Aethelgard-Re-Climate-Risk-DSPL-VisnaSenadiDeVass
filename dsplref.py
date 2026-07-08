# -*- coding: utf-8 -*-
"""DSPLref.ipynb

Original file is located at
    https://colab.research.google.com/drive/168c4WldUzx6PxKBJKE4MkajqJViviKbq
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Connect Google Drive
from google.colab import drive
drive.mount('/content/drive')

import os

# Define the path to your datasets
datasets_path = '/content/drive/MyDrive/DSPL referred/Datasets'

# List all files and directories in the specified path
try:
    files_in_directory = os.listdir(datasets_path)
    print(f"Files in '{datasets_path}':")
    for f in files_in_directory:
        print(f)
except FileNotFoundError:
    print(f"Error: The directory '{datasets_path}' was not found. Please ensure the path is correct and Google Drive is mounted.")
except Exception as e:
    print(f"An error occurred: {e}")

datasets = {}
datasets_path = '/content/drive/MyDrive/DSPL referred/Datasets'

files_to_load = [
    'global-warming-land.xlsx',
    'global-warming-fossil.xlsx',
    'contribution-to-temp-rise-by-gas.csv',
    'temperature-anomaly.csv',
    'ghg-emissions-by-world-region.xlsx',
    'contribution-temp-rise-degrees.csv'
]

for filename in files_to_load:
    file_path = os.path.join(datasets_path, filename)
    name = os.path.splitext(filename)[0] # Get name without extension

    try:
        if filename.endswith('.csv'):
            datasets[name] = pd.read_csv(file_path)
            print(f"Loaded '{filename}' as '{name}' (CSV).")
        elif filename.endswith(('.xlsx', '.xls')):
            datasets[name] = pd.read_excel(file_path)
            print(f"Loaded '{filename}' as '{name}' (Excel).")
        else:
            print(f"Skipping '{filename}': Unknown file type.")
    except Exception as e:
        print(f"Error loading '{filename}': {e}")

print("\nDatasets loaded:")
for name, df in datasets.items():
    print(f"- {name}: {df.shape[0]} rows, {df.shape[1]} columns")

"""## Dataset Inspection"""

# Iterate through each dataset in the dictionary and print inspection details
for name, df in datasets.items():
    print(f"\n--- Inspecting Dataset: {name} ---")

    # 1. How many rows and columns are there?
    print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")

    # 2. What are the column names?
    print("Columns:")
    for col in df.columns:
        print(f"  - {col}")

    # 3. What data types are present?
    print("Data Types:")
    print(df.info(verbose=True, show_counts=True))

    # 4. Are there missing values?
    print("\nMissing Values (Count):")
    print(df.isnull().sum())
    print("\nMissing Values (Percentage):")
    print(df.isnull().sum() / len(df) * 100)

    # 5. What does the first few rows look like?
    print("\nFirst 5 Rows:")
    display(df.head())

    # 6. What variables might be useful later? (Initial thoughts)
    print("\nInitial thoughts on potentially useful variables: 'Entity', 'Year', and any columns related to 'temperature', 'emissions', or 'contribution' seem important for global warming analysis.")
    print("---------------------------------------------------")

"""## Data Quality Assessment"""

print("\n--- Data Quality Assessment ---")

for name, df in datasets.items():
    print(f"\nDataset: {name}")

    # Are there duplicate rows?
    duplicates = df.duplicated().sum()
    print(f"  - Duplicate Rows: {duplicates}")

    # What is the year range in each dataset?
    if 'Year' in df.columns:
        min_year = df['Year'].min()
        max_year = df['Year'].max()
        print(f"  - Year Range: {min_year} - {max_year}")
    else:
        print("  - Year column not found.")

    # How many unique entities are there?
    if 'Entity' in df.columns:
        unique_entities = df['Entity'].nunique()
        print(f"  - Unique Entities: {unique_entities}")
        # If there are many, we can show a sample or list specific ones later if needed
    else:
        print("  - Entity column not found.")

    # Is the temperature dataset truly global only?
    if name == 'temperature-anomaly' and 'Entity' in df.columns:
        if 'Global' in df['Entity'].unique() and df['Entity'].nunique() == 1:
            print(f"  - '{name}' dataset is truly global (only 'Global' entity found).")
        else:
            print(f"  - '{name}' dataset contains {df['Entity'].nunique()} entities, including: {df['Entity'].unique()[:5]}...") # Show first 5 unique entities if not purely global

    # Impossible Values (initial check - more detailed checks would be column-specific)
    # For numerical columns, one might check for negative values where only positive make sense.
    # For now, we rely on df.info() and df.describe() for initial range checks.
    print("  - Note on 'Impossible Values': This often requires domain knowledge. We've seen data types (df.info()) and missing values (isnull().sum()). Further specific checks would be needed per column if issues are suspected.")

print("\n--- Data Quality Assessment Complete ---")

"""## Data Cleaning"""

print("--- Cleaning Column Names ---")

for name, df in datasets.items():
    original_columns = df.columns.tolist()

    # Task 1: Check for and remove leading/trailing spaces
    df.columns = df.columns.str.strip()

    # Task 2: Rename extremely long column names
    # Define a mapping for renaming. Corrected and expanded based on actual column names.
    rename_map = {
        'Change in global mean surface temperature caused by greenhouse gas emissions from agriculture and land use': 'Land_Use_Temp',
        'Change in global mean surface temperature caused by greenhouse gas emissions from fossil fuels and industry': 'Fossil_Fuel_Temp',

        # Corrected: 'surface surface' typo removed
        'Change in global mean surface temperature caused by nitrous oxide emissions': 'Nitrous_Oxide_Temp',
        'Change in global mean surface temperature caused by methane emissions': 'Methane_Temp',
        'Change in global mean surface temperature caused by CO₂ emissions': 'CO2_Temp',

        # Corrected: to match actual column name from 'temperature-anomaly' dataset
        'Global average temperature anomaly relative to 1961-1990': 'Global_Temp_Anomaly',
        'Annual average global surface temperature anomaly relative to the 1961-1990 reference period': 'Global_Temp_Anomaly_Annual',
        'Upper bound of the annual temperature anomaly (95% confidence interval)': 'Temp_Anomaly_Upper_CI',
        'Lower bound of the annual temperature anomaly (95% confidence interval)': 'Temp_Anomaly_Lower_CI',

        # Corrected: to match actual column name from 'ghg-emissions-by-world-region' dataset
        'Annual greenhouse gas emissions in CO₂ equivalents': 'Annual_GHG_Emissions_CO2_Eq',

        # Added: for 'contribution-temp-rise-degrees' dataset
        'Change in global mean surface temperature caused by greenhouse gas emissions': 'Total_GHG_Temp_Contribution'
    }

    # Apply renaming
    df = df.rename(columns=rename_map)

    # Update the dictionary with the cleaned DataFrame
    datasets[name] = df

    print(f"\nDataset: {name}")
    print("  Original Columns (first 5):", original_columns[:5])
    print("  Cleaned Columns (first 5):", df.columns.tolist()[:5])

print("\n--- Column Cleaning Complete ---")

print("--- Handling Missing Values ---")

for name, df in datasets.items():
    print(f"\nDataset: {name}")

    # Drop 'Code' column if it exists
    if 'Code' in df.columns:
        initial_shape = df.shape
        df = df.drop(columns=['Code'])
        print(f"  - Dropped 'Code' column. Shape changed from {initial_shape} to {df.shape}.")

    # Fill missing numerical values for specific columns in 'contribution-to-temp-rise-by-gas'
    if name == 'contribution-to-temp-rise-by-gas':
        for col_to_fill in ['Nitrous_Oxide_Temp', 'Methane_Temp']:
            if col_to_fill in df.columns:
                if df[col_to_fill].isnull().any():
                    missing_count = df[col_to_fill].isnull().sum()
                    df[col_to_fill] = df[col_to_fill].fillna(0)
                    print(f"  - Filled {missing_count} missing values in '{col_to_fill}' with 0.")

    # Update the dictionary with the modified DataFrame
    datasets[name] = df

print("\n--- Missing Value Handling Complete ---")

# Display missing value counts after cleaning for verification
print("\nMissing values after cleaning:")
for name, df in datasets.items():
    print(f"  - {name}:\n{df.isnull().sum()[df.isnull().sum() > 0]}")

print("--- Filtering for 'Global' Entity ---")

for name, df in datasets.items():
    print(f"\nDataset: {name}")

    if 'Entity' in df.columns:
        # Determine the correct global entity string for this dataset
        global_entity_name = None
        if 'Global' in df['Entity'].unique():
            global_entity_name = 'Global'
        elif 'World' in df['Entity'].unique():
            global_entity_name = 'World'

        if global_entity_name:
            initial_rows = df.shape[0]
            df_filtered = df[df['Entity'] == global_entity_name].copy()
            if not df_filtered.empty:
                datasets[name] = df_filtered
                print(f"  - Filtered to '{global_entity_name}' entity only. Rows changed from {initial_rows} to {datasets[name].shape[0]}.")
            else:
                print(f"  - '{global_entity_name}' entity found, but filtering resulted in an empty DataFrame. Keeping original.")
        else:
            print("  - Neither 'Global' nor 'World' entity found in this dataset. No filtering applied.")
    else:
        print("  - 'Entity' column not found in this dataset. No filtering applied.")

print("\n--- 'Global' Entity Filtering Complete ---")

# Display unique entities after filtering for verification
print("\nUnique entities after filtering:")
for name, df in datasets.items():
    if 'Entity' in df.columns:
        print(f"  - {name}: {df['Entity'].unique().tolist()}")
    else:
        print(f"  - {name}: No 'Entity' column.")

print("--- Keeping Necessary Columns ---")

# Define a mapping of datasets to their necessary columns
# These include 'Entity', 'Year', and the renamed measurement columns
necessary_columns_map = {
    'global-warming-land': ['Entity', 'Year', 'Land_Use_Temp'],
    'global-warming-fossil': ['Entity', 'Year', 'Fossil_Fuel_Temp'],
    'contribution-to-temp-rise-by-gas': ['Entity', 'Year', 'Nitrous_Oxide_Temp', 'Methane_Temp', 'CO2_Temp'],
    'temperature-anomaly': ['Entity', 'Year', 'Global_Temp_Anomaly', 'Temp_Anomaly_Upper_CI', 'Temp_Anomaly_Lower_CI'],
    'ghg-emissions-by-world-region': ['Entity', 'Year', 'Annual_GHG_Emissions_CO2_Eq'],
    'contribution-temp-rise-degrees': ['Entity', 'Year', 'Total_GHG_Temp_Contribution']
}

for name, df in datasets.items():
    print(f"\nDataset: {name}")

    # Get the list of columns to keep for the current dataset
    cols_to_keep = necessary_columns_map.get(name, [])

    if cols_to_keep:
        # Filter out columns that don't exist in the current DataFrame
        existing_cols_to_keep = [col for col in cols_to_keep if col in df.columns]

        if existing_cols_to_keep:
            initial_shape = df.shape
            df = df[existing_cols_to_keep].copy()
            datasets[name] = df
            print(f"  - Kept columns: {existing_cols_to_keep}. Shape changed from {initial_shape} to {df.shape}.")
        else:
            print("  - No specified necessary columns found in this dataset. Keeping all existing columns.")
    else:
        print("  - No necessary column mapping found for this dataset. Keeping all existing columns.")

print("\n--- Necessary Column Selection Complete ---")

# Display the columns of each dataset after cleaning for verification
print("\nFinal Columns after cleaning:")
for name, df in datasets.items():
    print(f"  - {name}: {df.columns.tolist()}")

"""## Merging Datasets

To prepare the datasets for modeling, we need to merge them into a single DataFrame. First, we'll ensure all datasets cover the same year range.
"""

print("--- Checking Year Ranges and Finding Common Years ---")

# Step 1: Check the year range in every cleaned dataset
all_years = []
for name, df in datasets.items():
    if 'Year' in df.columns:
        min_year = df['Year'].min()
        max_year = df['Year'].max()
        print(f"  - {name}: Year Range = {min_year} - {max_year}")
        all_years.append(set(df['Year'].unique()))
    else:
        print(f"  - {name}: 'Year' column not found.")

# Step 2: Find the years common to all datasets
if all_years:
    common_years = set.intersection(*all_years)
    min_common_year = min(common_years)
    max_common_year = max(common_years)
    print(f"\nCommon Year Range Across All Datasets: {min_common_year} - {max_common_year} ({len(common_years)} years)")
else:
    print("No datasets with 'Year' column found to determine common years.")

# Step 3: Trim datasets to only those common years
print("\n--- Trimming Datasets to Common Years ---")
for name, df in datasets.items():
    if 'Year' in df.columns:
        initial_rows = df.shape[0]
        df_trimmed = df[df['Year'].isin(common_years)].copy()
        datasets[name] = df_trimmed
        print(f"  - {name}: Trimmed from {initial_rows} rows to {df_trimmed.shape[0]} rows.")
    else:
        print(f"  - {name}: No 'Year' column to trim.")

print("\n--- Datasets Trimmed ---")

print("--- Merging Datasets ---")

# Step 4: Merge all datasets together on 'Year'
# Start with the first dataset in the dictionary
merged_df = None
first_dataset = True

for name, df in datasets.items():
    # For merging, we'll drop the 'Entity' column from all but the first DataFrame
    # as we've already filtered to a single global entity.
    df_to_merge = df.drop(columns=['Entity']) if 'Entity' in df.columns and not first_dataset else df.copy()

    if first_dataset:
        merged_df = df_to_merge
        first_dataset = False
    else:
        # Use 'outer' merge to ensure all years are kept, though with common years, 'inner' would also work.
        # 'Year' is the only common column left, so it will merge on that automatically.
        merged_df = pd.merge(merged_df, df_to_merge, on='Year', how='outer')
    print(f"  - Merged '{name}'. Current merged shape: {merged_df.shape}")

print("\n--- Merging Complete ---")

# Step 5: Check the merged dataset
print("\n--- Merged Dataset Summary ---")
print(f"Shape of merged dataset: {merged_df.shape}")

print("\nMissing values in merged dataset:")
print(merged_df.isnull().sum()[merged_df.isnull().sum() > 0])

print("\nFirst few rows of merged dataset:")
display(merged_df.head())

print("\nData types of merged dataset:")
print(merged_df.info())

cleaned_dataset_path = '/content/drive/MyDrive/DSPL referred/Cleaned dataset/cleaned_merged_data.csv'
merged_df.to_csv(cleaned_dataset_path, index=False)
print(f"Cleaned dataset saved to: {cleaned_dataset_path}")

"""## Exploratory Data Analysis (EDA)

Now that our datasets are merged and cleaned, we can begin Exploratory Data Analysis to understand distributions, trends, patterns, and relationships within the data, directly addressing Task 1 of your coursework.

### Step 5.1 – Summary Statistics

We'll start by looking at the descriptive statistics of our `merged_df` to understand the central tendency, dispersion, and shape of its distribution.
"""

print("--- Summary Statistics of Merged Dataset ---")
display(merged_df.describe())

"""### Step 5.2 – Distribution Plots

To understand the distribution of each variable, we'll create histograms and Kernel Density Estimate (KDE) plots. This helps us identify skewness, potential outliers, and the overall shape of the data for each numerical column.
"""

print("--- Generating Distribution Plots ---")

# Exclude 'Year' and 'Entity' as they are not typically analyzed with histograms for distribution
columns_for_distribution = merged_df.select_dtypes(include=np.number).columns.drop(['Year'])

# Determine grid size for subplots
num_cols = len(columns_for_distribution)
num_rows = (num_cols + 1) // 2 # 2 plots per row

plt.figure(figsize=(15, 5 * num_rows))
plt.suptitle('Distribution of Numerical Variables', y=1.02, fontsize=16)

for i, col in enumerate(columns_for_distribution):
    plt.subplot(num_rows, 2, i + 1)
    sns.histplot(merged_df[col], kde=True, bins=30)
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency / Density')

plt.tight_layout(rect=[0, 0.03, 1, 0.98]) # Adjust layout to prevent title overlap
plt.show()
print("\n--- Distribution Plots Complete ---")

"""### Step 5.3 – Boxplots

Next, we'll create boxplots for each numerical variable to visually identify potential outliers and understand the spread of the data. While climate data may not have many random outliers, this is still a good practice in EDA.
"""

print("--- Generating Boxplots ---")

# Exclude 'Year' and 'Entity' as they are not suitable for boxplots in this context
columns_for_boxplots = merged_df.select_dtypes(include=np.number).columns.drop(['Year'])

# Determine grid size for subplots
num_cols_boxplot = len(columns_for_boxplots)
num_rows_boxplot = (num_cols_boxplot + 1) // 2 # 2 plots per row

plt.figure(figsize=(15, 5 * num_rows_boxplot))
plt.suptitle('Boxplots of Numerical Variables', y=1.02, fontsize=16)

for i, col in enumerate(columns_for_boxplots):
    plt.subplot(num_rows_boxplot, 2, i + 1)
    sns.boxplot(y=merged_df[col])
    plt.title(f'Boxplot of {col}')
    plt.ylabel(col)

plt.tight_layout(rect=[0, 0.03, 1, 0.98]) # Adjust layout to prevent title overlap
plt.show()
print("\n--- Boxplots Complete ---")

"""### Step 5.4 – Time Series Line Graphs

To understand the trends and patterns over time, we will create line graphs for key variables against the 'Year'. This will allow us to observe how each factor has evolved from 1851 to 2021.
"""

print("--- Generating Time Series Line Graphs ---")

# Define the columns for which to generate time series plots
variables_to_plot = [
    'Global_Temp_Anomaly',
    'Annual_GHG_Emissions_CO2_Eq',
    'CO2_Temp',
    'Methane_Temp',
    'Nitrous_Oxide_Temp',
    'Fossil_Fuel_Temp',
    'Land_Use_Temp',
    'Total_GHG_Temp_Contribution'
]

# Define titles for the plots for better readability
plot_titles = {
    'Global_Temp_Anomaly': 'Global Temperature Anomaly vs Year',
    'Annual_GHG_Emissions_CO2_Eq': 'Annual GHG Emissions (CO₂ Eq) vs Year',
    'CO2_Temp': 'CO₂ Contribution to Temp Rise vs Year',
    'Methane_Temp': 'Methane Contribution to Temp Rise vs Year',
    'Nitrous_Oxide_Temp': 'Nitrous Oxide Contribution to Temp Rise vs Year',
    'Fossil_Fuel_Temp': 'Fossil Fuel Contribution to Temp Rise vs Year',
    'Land_Use_Temp': 'Land Use Contribution to Temp Rise vs Year',
    'Total_GHG_Temp_Contribution': 'Total GHG Temperature Contribution vs Year'
}

# Create subplots for each variable
# Adjusting grid size based on the number of variables
num_plots = len(variables_to_plot)
num_rows_ts = (num_plots + 1) // 2 # 2 plots per row

plt.figure(figsize=(18, 6 * num_rows_ts))
plt.suptitle('Time Series Trends of Key Climate Variables (1851-2021)', y=1.02, fontsize=18)

for i, col in enumerate(variables_to_plot):
    plt.subplot(num_rows_ts, 2, i + 1)
    sns.lineplot(x='Year', y=col, data=merged_df, marker='o', markersize=4, linewidth=1.5)
    plt.title(plot_titles.get(col, f'Trend of {col} over Time'), fontsize=14)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel(col.replace('_', ' '), fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

plt.tight_layout(rect=[0, 0.03, 1, 0.98]) # Adjust layout to prevent title overlap
plt.show()
print("\n--- Time Series Line Graphs Complete ---")

"""### Step 5.5 – Correlation Analysis

To understand the relationships between the different climate factors and identify potential multicollinearity, we will compute the Pearson correlation coefficients and visualize them using a heatmap.
"""

print("--- Generating Correlation Matrix and Heatmap ---")

# Exclude 'Year' and 'Entity' as they are not suitable for correlation analysis with other numerical features
correlation_df = merged_df.select_dtypes(include=np.number).drop(columns=['Year'])

# Calculate the correlation matrix
correlation_matrix = correlation_df.corr(method='pearson')

print("Correlation Matrix (Pearson coefficients):")
display(correlation_matrix)

# Visualize the correlation matrix using a heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Matrix of Numerical Variables', fontsize=16)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=45)
plt.tight_layout()
plt.show()

print("\n--- Correlation Matrix and Heatmap Complete ---")

"""### Step 5.6 – Feature Selection

Based on the previous EDA and correlation analysis, we will now define our target variable (`y`) and predictor variables (`X`) for the upcoming regression modeling. This step is crucial for preparing the data in a format suitable for machine learning algorithms.
"""

print("--- Performing Feature Selection ---")

# Define the Target Variable (y)
y = merged_df["Global_Temp_Anomaly"]
print(f"Target variable (y) defined with shape: {y.shape}")

# Define the Predictor Variables (X)
# Based on correlation analysis, some highly correlated variables are selected.
X = merged_df[[
    "Land_Use_Temp",
    "Fossil_Fuel_Temp",
    "Nitrous_Oxide_Temp",
    "Methane_Temp",
    "CO2_Temp",
    "Annual_GHG_Emissions_CO2_Eq",
    "Total_GHG_Temp_Contribution"
]]
print(f"Predictor variables (X) defined with shape: {X.shape}")

print("\n--- Feature Selection Complete ---")

"""### Multicollinearity Analysis with Variance Inflation Factor (VIF)

Given the strong correlations observed in the heatmap, it's crucial to assess multicollinearity using the Variance Inflation Factor (VIF). High VIF values indicate that a predictor variable is highly correlated with other predictor variables in the model, which can lead to unstable regression coefficients. This analysis will guide our final feature selection for regression modeling.
"""

print("--- Performing Multicollinearity Analysis with VIF ---")

# Import the required library
from statsmodels.stats.outliers_influence import variance_inflation_factor

# The predictor variables X have already been defined in the previous step.
# X = merged_df[[
#     "Land_Use_Temp",
#     "Fossil_Fuel_Temp",
#     "Nitrous_Oxide_Temp",
#     "Methane_Temp",
#     "CO2_Temp",
#     "Annual_GHG_Emissions_CO2_Eq",
#     "Total_GHG_Temp_Contribution"
# ]]

# Compute VIF
vif_data = pd.DataFrame()
vif_data["Feature"] = X.columns
vif_data["VIF"] = [
    variance_inflation_factor(X.values, i)
    for i in range(X.shape[1])
]

print("Variance Inflation Factor (VIF) for Predictor Variables:")
display(vif_data.sort_values(by="VIF", ascending=False))

print("\n--- Multicollinearity Analysis Complete ---")

"""### Reduce Multicollinearity

To address the severe multicollinearity, we will remove variables that are mathematically or conceptually redundant. Specifically, we will remove 'Total_GHG_Temp_Contribution' (as it's a sum of other contributions) and 'Fossil_Fuel_Temp' (due to its high overlap with CO₂ contribution and other factors). After removing these variables, we will recalculate the VIF values to assess the improvement.
"""

print("--- Reducing Multicollinearity by Removing Variables ---")

# Redefine Predictor Variables (X) by removing highly correlated/redundant features
X = merged_df[[
    "Land_Use_Temp",
    "CO2_Temp",
    "Methane_Temp",
    "Nitrous_Oxide_Temp",
    "Annual_GHG_Emissions_CO2_Eq"
]]

print(f"New Predictor variables (X) defined with shape: {X.shape}")

# Recalculate VIF for the updated X
vif_data_reduced = pd.DataFrame()
vif_data_reduced["Feature"] = X.columns
vif_data_reduced["VIF"] = [
    variance_inflation_factor(X.values, i)
    for i in range(X.shape[1])
]

print("\nRecalculated Variance Inflation Factor (VIF) for Reduced Predictor Variables:")
display(vif_data_reduced.sort_values(by="VIF", ascending=False))

print("\n--- Multicollinearity Reduction and VIF Recalculation Complete ---")

"""### Further Reduce Multicollinearity

Since the VIF values are still very high, we need to continue reducing multicollinearity. We will remove the variable with the highest VIF from the current set, which is 'Nitrous_Oxide_Temp', and then recalculate the VIFs once more.
"""

print("--- Further Reducing Multicollinearity by Removing 'Nitrous_Oxide_Temp' ---")

# Redefine Predictor Variables (X) by removing the feature with the highest VIF ('Nitrous_Oxide_Temp')
X = merged_df[[
    "Land_Use_Temp",
    "CO2_Temp",
    "Methane_Temp",
    "Annual_GHG_Emissions_CO2_Eq"
]]

print(f"New Predictor variables (X) defined with shape: {X.shape}")

# Recalculate VIF for the updated X
vif_data_further_reduced = pd.DataFrame()
vif_data_further_reduced["Feature"] = X.columns
vif_data_further_reduced["VIF"] = [
    variance_inflation_factor(X.values, i)
    for i in range(X.shape[1])
]

print("\nRecalculated Variance Inflation Factor (VIF) for Further Reduced Predictor Variables:")
display(vif_data_further_reduced.sort_values(by="VIF", ascending=False))

print("\n--- Further Multicollinearity Reduction and VIF Recalculation Complete ---")

"""### Continued Multicollinearity Reduction

Given that VIF values remain high, we will continue the process by removing the variable with the highest current VIF, 'Annual_GHG_Emissions_CO2_Eq'. This is an iterative process, and we aim to bring VIF values below a generally accepted threshold (e.g., 10 or 5).
"""

print("--- Continuing Multicollinearity Reduction by Removing 'Annual_GHG_Emissions_CO2_Eq' ---")

# Redefine Predictor Variables (X) by removing the feature with the highest VIF ('Annual_GHG_Emissions_CO2_Eq')
X = merged_df[[
    "Land_Use_Temp",
    "CO2_Temp",
    "Methane_Temp"
]]

print(f"New Predictor variables (X) defined with shape: {X.shape}")

# Recalculate VIF for the updated X
vif_data_final_reduced = pd.DataFrame()
vif_data_final_reduced["Feature"] = X.columns
vif_data_final_reduced["VIF"] = [
    variance_inflation_factor(X.values, i)
    for i in range(X.shape[1])
]

print("\nRecalculated Variance Inflation Factor (VIF) for Final Reduced Predictor Variables:")
display(vif_data_final_reduced.sort_values(by="VIF", ascending=False))

print("\n--- Multicollinearity Reduction and VIF Recalculation Complete ---")

"""### Final Multicollinearity Reduction Step (Iteration 3)

We continue the iterative process of multicollinearity reduction. Since 'Methane_Temp' now has the highest VIF, we will remove it from our predictor variables `X` and recalculate the VIFs to see if we can reach an acceptable threshold (typically below 10 or 5).
"""

print("--- Final Multicollinearity Reduction by Removing 'Methane_Temp' ---")

# Redefine Predictor Variables (X) by removing the feature with the highest VIF ('Methane_Temp')
X = merged_df[[
    "Land_Use_Temp",
    "CO2_Temp"
]]

print(f"New Predictor variables (X) defined with shape: {X.shape}")

# Recalculate VIF for the updated X
vif_data_final_final_reduced = pd.DataFrame()
vif_data_final_final_reduced["Feature"] = X.columns
vif_data_final_final_reduced["VIF"] = [
    variance_inflation_factor(X.values, i)
    for i in range(X.shape[1])
]

print("\nRecalculated Variance Inflation Factor (VIF) for the Final Predictor Variables:")
display(vif_data_final_final_reduced.sort_values(by="VIF", ascending=False))

print("\n--- Final Multicollinearity Reduction and VIF Recalculation Complete ---")

"""### Final VIF Check and Potential Last Reduction

After several iterations, we observe that 'Land_Use_Temp' and 'CO2_Temp' still exhibit VIFs around 27, which is higher than the desired threshold. To finalize the multicollinearity reduction, we will remove one of these remaining variables. As both have similar VIFs, we will remove 'CO2_Temp'. This will leave 'Land_Use_Temp' as the sole remaining predictor variable from the original set of `_Temp` contributions, which will inherently have a VIF of 1.

### Revised Feature Selection for Multicollinearity

Based on feedback, the previous approach of aggressively reducing variables until VIF is minimal (or undefined for a single variable) is not recommended. For datasets with inherent multicollinearity, such as climate data where many factors are naturally correlated over time, it's more appropriate to:

1.  **Retain scientifically meaningful variables**, even if they exhibit some correlation.
2.  **Employ regression techniques robust to multicollinearity**, such as Ridge Regression.

We will redefine our predictor variables `X` to include a set of key, scientifically relevant features and then move towards a modeling approach that can handle the expected multicollinearity.
"""

print("--- Re-defining Predictor Variables (X) for Robust Modeling ---")

# Redefine Predictor Variables (X) to include a scientifically relevant set
X = merged_df[[
    "Land_Use_Temp",
    "CO2_Temp",
    "Methane_Temp",
    "Nitrous_Oxide_Temp"
]]

print(f"Re-defined Predictor variables (X) with shape: {X.shape}")

# Recalculate VIF for this chosen set to understand the current level of multicollinearity
from statsmodels.stats.outliers_influence import variance_inflation_factor

vif_data_revised = pd.DataFrame()
vif_data_revised["Feature"] = X.columns
vif_data_revised["VIF"] = [
    variance_inflation_factor(X.values, i)
    for i in range(X.shape[1])
]

print("\nRecalculated Variance Inflation Factor (VIF) for the Revised Predictor Variables:")
display(vif_data_revised.sort_values(by="VIF", ascending=False))

print("\n--- Predictor Variable Redefinition Complete. Proceeding with Ridge Regression. ---")

"""### Next Steps: Preparing for Ridge Regression

With our `X` (predictor variables) and `y` (target variable `Global_Temp_Anomaly`) now defined, the next logical step is to prepare the data for a regression model. Given the remaining multicollinearity (as indicated by the VIF values, which are still somewhat high but acceptable for Ridge Regression), we will proceed with **Ridge Regression**. This will involve:

1.  **Splitting the data** into training and testing sets.
2.  **Scaling the features** (important for Ridge Regression).
3.  **Training a Ridge Regression model**.
4.  **Evaluating the model's performance**.

This approach will allow us to build a robust predictive model while accounting for the inherent correlations in the climate data.

### Step 1: Split the dataset

As specified, we will split the data chronologically into training (1851–1990) and testing (1991 onwards) sets, without using `train_test_split()` due to the time-series nature of the data.
"""

# Define target variable
y = merged_df["Global_Temp_Anomaly"]

# Training data (1851–1990)
train = merged_df[merged_df["Year"] <= 1990]

# Testing data (1991–2021)
test = merged_df[merged_df["Year"] > 1990]

X_train = train[
    [
        "Land_Use_Temp",
        "CO2_Temp",
        "Methane_Temp",
        "Nitrous_Oxide_Temp"
    ]
]

y_train = train["Global_Temp_Anomaly"]

X_test = test[
    [
        "Land_Use_Temp",
        "CO2_Temp",
        "Methane_Temp",
        "Nitrous_Oxide_Temp"
    ]
]

y_test = test["Global_Temp_Anomaly"]

print("Training data shape:", X_train.shape)
print("Testing data shape:", X_test.shape)

"""### Step 2: Standardise the features

Ridge Regression performs best when variables are on the same scale, so we will use `StandardScaler` to transform our features.
"""

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Features standardised successfully.")

"""### Step 3: Train the Ridge Regression model

Now we will train the Ridge Regression model using the scaled training data.
"""

from sklearn.linear_model import Ridge

ridge_model = Ridge(alpha=1.0)

ridge_model.fit(X_train_scaled, y_train)

print("Ridge Regression model trained successfully.")

"""### Step 4: Make predictions

With the model trained, we can now make predictions on our scaled test set.
"""

y_pred = ridge_model.predict(X_test_scaled)

print("Predictions completed.")

"""### Step 5: Evaluate the model

Finally, we will evaluate the performance of our Ridge Regression model using common regression metrics such as Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and R-squared (R²).
"""

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
import numpy as np

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("Model Evaluation")
print("----------------")
print(f"MAE : {mae:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"R²  : {r2:.4f}")

"""### Step 6: Visualise the Model Results

To better understand and communicate the model's performance, we will create several visualizations:

1.  **Actual vs Predicted Temperature Anomaly**
2.  **Residual Plot**
3.  **Predicted vs Actual Scatter Plot**

#### 1. Actual vs Predicted Temperature Anomaly
"""

plt.figure(figsize=(12,6))

plt.plot(test["Year"], y_test.values,
         label="Actual",
         linewidth=2)

plt.plot(test["Year"], y_pred,
         label="Predicted",
         linewidth=2,
         linestyle="--")

plt.title("Actual vs Predicted Global Temperature Anomaly")
plt.xlabel("Year")
plt.ylabel("Temperature Anomaly (°C)")
plt.legend()
plt.grid(True)

plt.show()

"""#### 2. Residual Plot

Residuals help determine whether the model is making systematic errors. A good residual plot should show points randomly scattered around the zero line.
"""

residuals = y_test - y_pred

plt.figure(figsize=(10,6))

plt.scatter(y_pred, residuals)

plt.axhline(y=0, linestyle="--", color='red')

plt.title("Residual Plot")
plt.xlabel("Predicted Temperature Anomaly")
plt.ylabel("Residuals")

plt.grid(True)
plt.show()

"""#### 3. Predicted vs Actual Scatter Plot

The closer the points are to the diagonal line, the better the predictions.
"""

plt.figure(figsize=(8,8))

plt.scatter(y_test, y_pred)

plt.plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    linestyle="--",
    color='red'
)

plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.title("Predicted vs Actual Temperature Anomaly")

plt.grid(True)
plt.show()

"""### Step 7: Generate a 10-Year Forecast (2022-2031)

To estimate temperature anomalies over the next decade (2022-2031), we first need to forecast the values of our predictor variables (`Land_Use_Temp`, `CO2_Temp`, `Methane_Temp`, `Nitrous_Oxide_Temp`) for these future years. Since we don't have external projections, we'll use a simple linear regression model for each predictor based on its historical trend.

Once we have the forecasted predictor values, we will scale them using our pre-fitted `StandardScaler` and then use our trained `Ridge` model to predict the `Global_Temp_Anomaly` for the next 10 years.
"""

from sklearn.linear_model import LinearRegression

# Define the forecast years
forecast_years = np.arange(2022, 2032)

# Prepare an empty DataFrame for future predictors
future_predictors_df = pd.DataFrame({'Year': forecast_years})

# List of predictor variables
predictor_cols = ["Land_Use_Temp", "CO2_Temp", "Methane_Temp", "Nitrous_Oxide_Temp"]

# For each predictor, fit a linear model and forecast future values
for col in predictor_cols:
    # Use the entire merged_df for historical trends for each predictor
    X_historic_trend = merged_df[['Year']]
    y_historic_trend = merged_df[col]

    # Fit a simple linear regression model
    trend_model = LinearRegression()
    trend_model.fit(X_historic_trend, y_historic_trend)

    # Predict for future years
    future_predictors_df[col] = trend_model.predict(future_predictors_df[['Year']])

print("Forecasted Predictor Values for 2022-2031:")
display(future_predictors_df.head(10))

# Scale the forecasted predictor values using the previously fitted scaler
X_forecast_scaled = scaler.transform(future_predictors_df[predictor_cols])

# Predict future temperature anomalies using the trained Ridge model
y_forecast = ridge_model.predict(X_forecast_scaled)

# Create a DataFrame for the forecast results
forecast_results = pd.DataFrame({
    'Year': forecast_years,
    'Predicted Temperature Anomaly (°C)': y_forecast
})

print("10-Year Forecast for Global Temperature Anomaly:")
display(forecast_results)

"""### Plotting the Forecasted Temperature Anomalies

Now, let's visualize the entire timeline, combining the historical actual values, the model's predictions on the test set, and our new 10-year forecast.
"""

plt.figure(figsize=(14, 7))

# Plot Actual Historical Data
plt.plot(merged_df['Year'], merged_df['Global_Temp_Anomaly'], label='Actual Historical (1851-2021)', color='blue', linewidth=1.5)

# Plot Model Predictions on Test Data
plt.plot(test["Year"], y_pred, label="Model Prediction (1991-2021)", color='orange', linestyle='--', linewidth=2)

# Plot 10-Year Forecast
plt.plot(forecast_results['Year'], forecast_results['Predicted Temperature Anomaly (°C)'], label='10-Year Forecast (2022-2031)', color='red', linestyle=':', linewidth=2)

# Add a vertical line to mark the start of the forecast period
plt.axvline(x=2021.5, color='gray', linestyle='-.', label='Start of Forecast (2022)')

plt.title("Global Temperature Anomaly: Historical, Predicted, and 10-Year Forecast")
plt.xlabel("Year")
plt.ylabel("Temperature Anomaly (°C)")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 6))

# Plot Model Predictions on Test Data
plt.plot(test["Year"], y_pred, label="Model Prediction (1991-2021)", color='orange', linestyle='--', linewidth=2)

plt.title("Zoomed-in: Model Predictions for Global Temperature Anomaly (1991-2021)")
plt.xlabel("Year")
plt.ylabel("Predicted Temperature Anomaly (°C)")
plt.legend()
plt.grid(True)
plt.xticks(test["Year"][::5]) # Show ticks for every 5 years for better readability
plt.tight_layout()
plt.show()

"""### Zoomed-in Plot: 10-Year Temperature Anomaly Forecast (2022-2031)

This plot specifically visualizes the projected increase in global temperature anomalies over the next decade, from 2022 to 2031.
"""

plt.figure(figsize=(10, 6))

# Plot 10-Year Forecast only
plt.plot(forecast_results['Year'], forecast_results['Predicted Temperature Anomaly (°C)'],
         label='10-Year Forecast (2022-2031)',
         color='red',
         marker='o',
         linestyle='-',
         linewidth=2)

plt.title("10-Year Forecast: Predicted Global Temperature Anomaly (2022-2031)")
plt.xlabel("Year")
plt.ylabel("Predicted Temperature Anomaly (°C)")
plt.legend()
plt.grid(True)
plt.xticks(forecast_results['Year'])
plt.tight_layout()
plt.show()
