import pandas as pd
import numpy as np

print("Running Github Scraper")

url = 'https://raw.githubusercontent.com/dingkaihua/fsrdc-external-census-projects/master/ProjectsAllMetadata.xlsx'
try:
    all_metadata = pd.read_excel(url, sheet_name="All Metadata")
    abstracts = pd.read_excel(url, sheet_name="Abstracts")
    datasets = pd.read_excel(url, sheet_name="Datasets")
    researchers = pd.read_excel(url, sheet_name="Researchers")
except FileNotFoundError:
    print("File not found. Please check the URL and try again.")
except Exception as e:
    print(f"An error occurred: {e}")

# Merge datasets and researchers to get unique combinations of
# researchers and datasets
dataset_data = pd.merge(datasets, researchers, on=["Title", "PI"])

print("Github Data")
print(dataset_data.head(5))

# Select columns of interest and rename them
selected = dataset_data[["Title", "RDC_x", "PI", "Data Name", "Researcher"]]
selected = selected.rename(columns={
    "Title": "title",
    "RDC_x": "location",
    "PI": "pi",
    "Data Name": "dataset",
    "Researcher": "researcher"
})

# Need to ensure all PIs are in researcher
# First test of code
# Sample DataFrame
df = pd.DataFrame({
    "Title": ["Project A", "Project A", "Project B"],
    "RDC": ["boston", "boston", "chicago"],
    "Data Name": ["dataset1", "dataset1", "dataset2"],
    "PI": ["Alice", "Alice", "Bob"],
    "Researcher": ["Charlie", "Alice", "Dave"]
})

# Get unique combinations for each project based on
# Title, RDC, Data Name, and PI
unique_combos = df[["Title", "RDC", "Data Name", "PI"]].drop_duplicates()

# For each unique combination, check if the PI appears as a researcher.
new_rows = []
for _, row in unique_combos.iterrows():
    title = row["Title"]
    rdc = row["RDC"]
    dataset = row["Data Name"]
    pi_val = row["PI"]

    # Filter rows matching the current combination
    subset = df[(df["Title"] == title) &
                (df["RDC"] == rdc) &
                (df["Data Name"] == dataset)]

    # If the PI is not present in the "Researcher"
    # column for this group, create a new row.
    if not (subset["Researcher"] == pi_val).any():
        new_row = {
            "Title": title,
            "RDC": rdc,
            "Data Name": dataset,
            "PI": pi_val,
            "Researcher": pi_val
        }
        new_rows.append(new_row)

# Step 3: Create a DataFrame from the new rows, then add it to the original data
if new_rows:
    df_new = pd.DataFrame(new_rows)
    # Step 4: Append new rows to the original DataFrame
    df_final = pd.concat([df, df_new], ignore_index=True)
else:
    df_final = df.copy()

# Check output, should have 4 rows!
print("Test Data 1")
print(df_final.head(5))

# Apply sample approach to the full dataframe
# Get unique combinations for each project based on
# Title, RDC, Data Name, and PI
unique_combos = selected[[
    "title", "location", "dataset", "pi"]].drop_duplicates()

# For each unique combination, check if the PI appears as a researcher.
new_rows = []
for _, row in unique_combos.iterrows():
    title = row["title"]
    location = row["location"]
    dataset = row["dataset"]
    pi_val = row["pi"]

    # Filter rows matching the current combination
    subset = selected[(selected["title"] == title) &
                (selected["location"] == location) &
                (selected["dataset"] == dataset)]

    # If the PI is not present in the "Researcher"
    # column for this group, create a new row.
    if not (subset["researcher"] == pi_val).any():
        new_row = {
            "title": title,
            "location": location,
            "dataset": dataset,
            "pi": pi_val,
            "researcher": pi_val
        }
        new_rows.append(new_row)

# Step 3: Create a DataFrame from the new rows, then add it to the original data
if new_rows:
    selected_new = pd.DataFrame(new_rows)
    # Step 4: Append new rows to the original DataFrame
    selected_final = pd.concat([selected, selected_new], ignore_index=True)
else:
    selected_final = df.copy()

# Check output, should have 4 rows!
print("Selected Data")
print(selected_final.head(5))

print(selected.shape)

print(selected_final.shape)

# Generate new terms to search that are the RDC, Census Bureau and FSRDC
# First testing on sample data
# Create a sample DataFrame with some made-up data.
df_final = pd.DataFrame({
    "Title": ["Project A", "Project A", "Project B", "Project B"],
    "RDC": ["boston", "boston", "chicago", "chicago"],
    "PI": ["Alice", "Alice", "Bob", "Bob"],
    "Researcher": ["Charlie", "Alice", "Dave", "Eve"],
    "Data Name": ["abc", "def", "xyz", "lmn"]
})

print("Original DataFrame:")
print(df_final)
print("\n")

# Step 1: Extract unique combinations of Title, RDC, PI, and Researcher.
unique_combos = df_final[["Title", "RDC", "PI", "Researcher"]].drop_duplicates()

# Step 2: For each unique combination, create three new rows with the desired Data Name values.
new_rows = []
for _, row in unique_combos.iterrows():
    title = row["Title"]
    rdc = row["RDC"]
    pi = row["PI"]
    researcher = row["Researcher"]

    # New row with Data Name as "<RDC> RDC" (e.g., "boston RDC")
    new_rows.append({
        "Title": title,
        "RDC": rdc,
        "PI": pi,
        "Researcher": researcher,
        "Data Name": f"{rdc} RDC"
    })

    # New row with Data Name "FSRDC"
    new_rows.append({
        "Title": title,
        "RDC": rdc,
        "PI": pi,
        "Researcher": researcher,
        "Data Name": "FSRDC"
    })

    # New row with Data Name "Census Bureau"
    new_rows.append({
        "Title": title,
        "RDC": rdc,
        "PI": pi,
        "Researcher": researcher,
        "Data Name": "Census Bureau"
    })

# Convert the list of new rows into a DataFrame.
new_entries = pd.DataFrame(new_rows)

# Step 3: Append the new rows to the original DataFrame.
final_df = pd.concat([df_final, new_entries], ignore_index=True)

# Sample output should have each researcher with the location and other terms
print("Test Data 2")
print(final_df.head(10))

# get the unique combinations (dropping duplicates)
unique_combos = selected_final[[
    "title", "location", "pi", "researcher"]].drop_duplicates()

# Create an empty list to collect new rows
new_rows = []

# For each unique combination, create three new rows with the desired Data Name values.
for _, row in unique_combos.iterrows():
    title = row["title"]
    rdc = row["location"]
    pi = row["pi"]
    researcher = row["researcher"]

    # Create a new row with Data Name as "rdc RDC" (e.g., "boston RDC")
    new_rows.append({
        "title": title,
        "location": rdc,
        "pi": pi,
        "researcher": researcher,
        "dataset": f"{rdc} RDC"
    })

    # Create a new row with Data Name "FSRDC"
    new_rows.append({
        "title": title,
        "location": rdc,
        "pi": pi,
        "researcher": researcher,
        "dataset": "FSRDC"
    })

    # Create a new row with Data Name "Census Bureau"
    new_rows.append({
        "title": title,
        "location": rdc,
        "pi": pi,
        "researcher": researcher,
        "dataset": "Census Bureau"
    })

# Convert the list of new rows into a DataFrame
new_entries = pd.DataFrame(new_rows)

# Optionally, append these new rows to your original DataFrame.
final_dataset = pd.concat([selected_final, new_entries], ignore_index=True)

# Check the dataset shape
print("Final Dataset")
print(final_dataset.shape)

# Save the data
final_dataset.to_csv("dataset_data.csv", index=False)