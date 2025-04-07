# Import libraries


import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz


# Define function to clean 2024 research output data set
def clean_2024_data(outputs_org):
    """
    Clean 2024 research output dataset

    Parameters:
    - outputs_org: 2024 research output dataframe

    Return:
    Cleaned 2024 research output dataframe
    """
    try:
        # Replace reasearch outputs without OutputTitle with ProjectTitle as title
        outputs_org.loc[outputs_org["OutputTitle"].isna(), "OutputTitle"] = outputs_org.loc[outputs_org["OutputTitle"].isna(), "ProjectTitle"]
        # Replace reasearch outputs without OutputYear with ProjectEndYear as year
        outputs_org.loc[outputs_org["OutputYear"].isna(), "OutputYear"] = outputs_org.loc[outputs_org["OutputYear"].isna(), "ProjectEndYear"]   
        # Only keep the columns needed
        outputs_org = outputs_org[["OutputTitle", "OutputYear", "ProjectRDC", "ProjectPI"]].copy()
        # Change the column names
        outputs_org.columns = ["Title", "Year", "Agency", "PI"]
        # Change the column type of Year column to be int
        outputs_org["Year"] = outputs_org["Year"].astype(int)
        # Strip other text columns
        outputs_org["Title"] = outputs_org["Title"].str.strip()
        outputs_org["Agency"] = outputs_org["Agency"].str.strip()
        outputs_org["PI"] = outputs_org["PI"].str.strip()
        # Return clean 2024 research output dataset
        return outputs_org
    except Exception as e:
        print(f"Error in clean_2024_data: {e}")
        raise

# Define test function for clean_2024_data
def test_clean_2024_data():
    """
    Test the function clean_2024_data()
    """
    # Create test dataframe
    test_data = pd.DataFrame({
        "OutputTitle": [None, " Paper 2 ", " Paper 3 "],
        "ProjectTitle": [" Project 1 ", " Project 2 ", " Project 3 "],
        "OutputYear": [2021, None, 2023],
        "ProjectEndYear": [2021, 2022, 2023],
        "ProjectRDC": [" Boston ", " UCLA ", " Upenn "],
        "ProjectPI": [" David ", " Susan ", " Joe "]})
    
    # Create expected dataframe
    test_expected = pd.DataFrame({
        "Title": ["Project 1", "Paper 2", "Paper 3"],
        "Year": [2021, 2022, 2023],
        "Agency": ["Boston", "UCLA", "Upenn"],
        "PI": ["David", "Susan", "Joe"]})
    
    # Get the result for test data
    test_result = clean_2024_data(test_data)

    # Test if the results are the same
    assert test_result.equals(test_expected), "DataFrame doesn't match expected values"

    print("All test cases passed! (test_clean_2024_data)")


# Define function to clean API result research output dataset
def clean_retreived_data(outputs):
    """
    Clean retrevied result research output dataset

    Parameters:
    - outputs: API result research output dataframe

    Return:
    Cleaned retrevied result research output dataframe
    """
    try: 
        # Convert publication_date column to datetime
        outputs["publication_date"] = pd.to_datetime(outputs["publication_date"])
        # Split the authors and save it in a set
        outputs["authors"] = outputs["authors"].apply(lambda x: {item.strip() for item in x.split(";")})
        # Strip researcher and title column
        outputs["researcher"] = outputs["researcher"].str.strip()
        outputs["title"] = outputs["title"].str.strip()
        # Add a column Unique to identify if the output is unqiue to the dataset
        # (The research output does not exit in 2024 dataset)
        outputs["unique"] = False

        # Return clean retrevied result research output dataset
        return outputs
    except Exception as e:
        print(f"Error in clean_retreived_data: {e}")
        raise

# Define test function for clean_retreived_data
def test_clean_retreived_data():
    """
    Test the function clean_retreived_data()
    """
    # Create test dataframe
    test_data = pd.DataFrame({
        "publication_date": ["1/1/2015", "6/10/2019", "1/1/2016"],
        "authors": [" David ; Susan ", " Zoe ; Linda ", " Joe ; Harry"],
        "researcher": [" Will ", " Aaron ", " Adrian "],
        "title": [" Paper 1 ", " Paper 2 ", " Paper 3 "]})
    
    # Create expected dataframe
    test_expected = pd.DataFrame({
        "publication_date": ["2015-01-01", "2019-06-10", "2016-01-01"],
        "authors": [{"David", "Susan"}, {"Linda", "Zoe"}, {"Joe", "Harry"}],
        "researcher": ["Will", "Aaron", "Adrian"],
        "title": ["Paper 1", "Paper 2", "Paper 3"],
        "unique": [False, False, False]})
    
    # Convert publication_date to datetime type
    test_expected["publication_date"] = pd.to_datetime(test_expected["publication_date"])
    
    # Get the result for test data
    test_result = clean_retreived_data(test_data)

    # Test if the results are the same
    assert test_result.equals(test_expected), "DataFrame doesn't match expected values"

    print("All test cases passed! (clean_retreived_data)")

# Define function to identify unique records just by year
def find_unique_records_year(outputs_org, outputs):
    """
    Identify records that is outside the year range of 2024 research
    output dataset as unique record, make it in API result df

    Parameters:
    - outputs_org_clean: clean 2024 research output dataframe
    - outputs_clean: clean API result research output dataframe

    Return:
    Modified clean API result research output dataframe with year outside 
    2024 dataset range marked as unique records
    """
    try:
        # Filter unique outputs by year
        # Output published outside the range of 2024 dataset is definitely unique output
        outputs.loc[~outputs["year"].isin(outputs_org.Year.unique()), "unique"] = True

        # Return the result
        return outputs
    except Exception as e:
        print(f"Error in find_unique_records_year: {e}")
        raise

# Define test function for find_unique_records_year when there are unique year
def test_find_unique_records_year_with_matches():
    """
    Test the function find_unique_records_year()
    When there are API retrieved outputs outside the 2024 research output dataset year range
    """
    # Create test dataframe
    test_data = pd.DataFrame({
        "title": ["Paper 1", "Paper 2", "Paper 3"],
        "year": [2011, 2015, 2024],
        "unique": [False, False, False]})
    test_data_org = pd.DataFrame({
        "Title": ["Paper 1", "Paper 2", "Paper 3", "Paper 4", "Paper 5", "Paper 6"],
        "Year": [2010, 2011, 2012, 2013, 2014, 2015]})
    
    # Create expected dataframe
    test_expected = pd.DataFrame({
        "title": ["Paper 1", "Paper 2", "Paper 3"],
        "year": [2011, 2015, 2024],
        "unique": [False, False, True]})
    
    # Get the result for test data
    test_result = find_unique_records_year(test_data_org, test_data)

    # Test if the results are the same
    assert test_result.equals(test_expected), "DataFrame doesn't match expected values"

    print("All test cases passed! (test_find_unique_records_year_with_matches)")

# Define test function for find_unique_records_year when there is no unique years
def test_find_unique_records_year_without_matches():
    """
    Test the function find_unique_records_year()
    When there are no API retrieved outputs outside the 2024 research output dataset year range
    """
    # Create test dataframe
    test_data = pd.DataFrame({
        "title": ["Paper 1", "Paper 2", "Paper 3"],
        "year": [2011, 2013, 2014],
        "unique": [False, False, False]})
    test_data_org = pd.DataFrame({
        "Title": ["Paper 1", "Paper 2", "Paper 3", "Paper 4", "Paper 5", "Paper 6"],
        "Year": [2010, 2011, 2012, 2013, 2014, 2015]})
    
    # Create expected dataframe
    test_expected = pd.DataFrame({
        "title": ["Paper 1", "Paper 2", "Paper 3"],
        "year": [2011, 2013, 2014],
        "unique": [False, False, False]})
    
    # Get the result for test data
    test_result = find_unique_records_year(test_data_org, test_data)

    # Test if the results are the same
    assert test_result.equals(test_expected), "DataFrame doesn't match expected values"

    print("All test cases passed! (test_find_unique_records_year_without_matches)")

# Define a function to identify unique records using fuzzy matching
def find_unique_records_fuzz(outputs_org, outputs, threshold=90):
    """
    Find unique records in the API result research outputs that does not exist in 2024 research output dataset
    Identify the records are the same between two outputs if:
    - Two outputs are published at the same year
    - Two outputs share the same PI as researcher or author
    (Exact matching or fuzzy matching with a similarity score of 90 or above)
    - Two outputs share the same title
    (Fuzzy matching with a similarity score of 90 or above)

    Parameters:
    - outputs_org: clean dataFrame of 2024 dataset
    - outputs: clean dataFrame of API retrieved research outputs
    - threshold: Minimum similarity score to consider as the same

    Returns:
    - set of unique records indices in API result research outputs
    - dictionary of best matches results if the API record is not unique
    - key: index in API result research output df
    - value: tuple (best match index,best_match_title, best_match_Score)
    in 2024 research output dataset
    """
    try:
        # Keep track of index of unique records and best matches for non-unique records
        unique_indices = set()
        best_matches = {}

        # Loop through all records in outputs to find the closest fuzzy match records
        for idx, row in outputs.iterrows():
            # Filter the records to keep the records with the same year
            outputs_org_filtered = outputs_org[outputs_org["Year"] == row["year"]]

            # Keep track of the best macthed index, title, and similarity score
            best_match_idx = -1
            best_match_title = ""
            best_match_score = 0.0

            # Loop through all records in original 2024 dataset to find the best match
            for idx2, row2 in outputs_org_filtered.iterrows():
                # Check if PI is in authors/researchers (or similarity score is above threshold if not)
                if (row2["PI"] in row["authors"]) or (row2["PI"] == row["researcher"]):
                    # Exact match if we can find it in authors or researcher directly
                    PI_flag = True
                else:
                    # If there is no exact match, we do fuzzy matching on names
                    # Keep track of the author best match score
                    best_PI_score = fuzz.token_sort_ratio(row["researcher"].lower(), row2["PI"].lower())
                    # Loop through the authors list to get the best similarity score
                    for author in row["authors"]:
                        # Calculate author similarity score
                        score_author = fuzz.token_sort_ratio(author.lower(), str(row2["PI"]).lower())
                        # Replace the best_PI score if better
                        if score_author > best_PI_score:
                            best_PI_score = score_author
                    # If the best score is above threshold, we consider it as the same PI
                    # Skip this record if PI are considered the same
                    if best_PI_score < threshold:
                        PI_flag = False
                    else:
                        PI_flag = True

                # Check if two outputs has the same PI, only proceed if True
                if PI_flag:
                    # Get similarity score
                    score = fuzz.token_sort_ratio(str(row["title"]).lower(), str(row2["Title"]).lower())
                    # Replace the best match idx, title, score if this is better
                    if score > best_match_score:
                        best_match_idx = idx2
                        best_match_title = row2["Title"]
                        best_match_score = score

            # If best match is above the threshold, save the best match result
            # Otherwise add idx to unique_indices set
            if best_match_score >= threshold:
                best_matches[idx] = (best_match_idx, best_match_title, best_match_score)
            else:
                unique_indices.add(idx)

        # Return both unique_indices and best_matches
        return unique_indices, best_matches
    except Exception as e:
        print(f"Error in find_unique_records_fuzz: {e}")
        raise

def test_find_unique_records_fuzz_with_matches():
    """
    Test the function find_unique_records when there are matches
    """
    # Create test dataframes
    outputs_org = pd.DataFrame({
        "Title": ["Paper is important", "Exam makes us stronger"],
        "PI": ["Joe H. Biden ", "Louis Harper"],
        "Year": [2023, 2022]})

    outputs = pd.DataFrame({
        "title": ["A paper is important", "Homework values efforts"],
        "researcher": ["Joe Biden", "Cameron Spiker"],
        "authors": [{"Linh Ngygen", "Alice Zhao"}, {"Travis Levitt", "Greyson Hampon"}],
        "year": [2023, 2021]})

    # Create the expected results
    expected_unique = {1}
    expected_matches = {0: (0, "Paper is important", 90)}

    # Get the result for test
    unique_indices, best_matches = find_unique_records_fuzz(outputs_org, outputs)

    # Check if results are the same
    assert unique_indices == expected_unique, f"Expected unique indices {expected_unique}, got {unique_indices}"

    # Check if best_matches has the same keys
    assert set(best_matches.keys()) == set(expected_matches.keys()), f"Expected match keys {expected_matches.keys()}, got {best_matches.keys()}"

    # Check if each match has correct structure and values
    for idx in best_matches:
        assert idx in expected_matches, f"Unexpected match found at index {idx}"
        assert best_matches[idx][0] == expected_matches[idx][0], f"Expected match index {expected_matches[idx][0]}, got {best_matches[idx][0]}"
        assert best_matches[idx][1] == expected_matches[idx][1], f"Expected match title {expected_matches[idx][1]}, got {best_matches[idx][1]}"
        assert best_matches[idx][2] >= expected_matches[idx][2], f"Expected match score >= {expected_matches[idx][2]}, got {best_matches[idx][2]}"

    print("All test cases passed! (test_find_unique_records_fuzz_with_matches)")

def test_find_unique_records_fuzz_all_unique():
    """
    Test the function find_unique_records when all records are unique
    """
    # Create test dataframes
    outputs_org = pd.DataFrame({
        "Title": ["Paper 1", "Paper 2", "Paper 3"],
        "PI": ["David", "Susan", "Sarah"],
        "Year": [2022, 2023, 2022]})

    outputs = pd.DataFrame({
        "title": ["Exam First", "Exam Second", "Exam Three"],
        "researcher": ["Thomas", "Karen", "Michael"],
        "authors": [{"Drake", "Lisa"}, {"Keith", "Paul"}, {"John", "Amy"}],
        "year": [2023, 2022, 2023]})

    # Create the expected ouput
    expected_unique = {0, 1, 2}
    expected_matches = {}

    # Call the function to get the result
    unique_indices, best_matches = find_unique_records_fuzz(outputs_org, outputs)

    # Check if the results are the same
    assert unique_indices == expected_unique, f"Expected all indices to be unique {expected_unique}, got {unique_indices}"
    assert best_matches == expected_matches, f"Expected no matches, got {best_matches}"

    print("All test cases passed! (test_find_unique_records_fuzz_all_unique)")

# Define function to complete Part 3 all steps
def data_pipeline(API):
    """
    Define function to complete everything for API/ webscrapping data
    
    Parameters:
    - data_file_name: file name for API or webscrapping data
    - API: whether the data is API data
    """
    # Print messages for information
    if API:
        print("Processing API data:")
    else:
        print("Processing webscraping data:")


    # Read in 2024 ResearchOutputs.xlsx file
    try:
        url = "https://raw.githubusercontent.com/dingkaihua/fsrdc-external-census-projects/master/ResearchOutputs.xlsx"
        outputs_org = pd.read_excel(url, sheet_name='Sheet1')
    except FileNotFoundError:
        print("Error: The file 'ResearchOutputs.xlsx' was not found.")
    except Exception as e:
        print(f"An error occurred while reading the Excel file: {str(e)}")

    # Clean 2024 research output data
    outputs_org = clean_2024_data(outputs_org)
    # Call the test function for clean_2024_data
    test_clean_2024_data()

    # Read API/ webscraping retrieved researcch outputs from csv file
    try:
        # Read in different files based on if it's API data
        if API:
            # API data
            outputs = pd.read_csv("../part2/openalex_researcher_datasets_matches.csv")
        else:
            # Webscraping data
            outputs = pd.read_csv("../part1/web_scraping_full_output.csv")      
    except FileNotFoundError:
        print("Error: The file was not found.")
    except Exception as e:
        print(f"An error occurred while reading the Excel file: {str(e)}")

    # Clean result research output data
    outputs = clean_retreived_data(outputs)
    # Call the test function for clean_api_data
    test_clean_retreived_data()

    # Identify the unique records only by year
    outputs = find_unique_records_year(outputs_org, outputs)
    # Call the test function for find_unique_records_year when there are unique years
    test_find_unique_records_year_with_matches()
    # Call the test function for find_unique_records_year when there is no unique years
    test_find_unique_records_year_without_matches()

    # Identify the unique records using fuzzy matching
    unique_indices, best_matches = find_unique_records_fuzz(outputs_org, outputs)
    # Call the test function for find_unique_records_fuzz when there are matches
    test_find_unique_records_fuzz_with_matches()
    # Call the test function for find_unique_records_fuzz when all records are unqiue
    test_find_unique_records_fuzz_all_unique()

    # Set unique to be true for unique records retreived by fuzzy matching
    outputs.loc[outputs.index.isin(unique_indices), "unique"] = True

    # Save the matching information for all matched research outputs
    # Add best match idx, title, score to outputs
    outputs["best_match_idx"] = None
    outputs["best_match_title"] = None
    outputs["best_match_score"] = None

    # Update the columns for records that have matches
    for idx, match_info in best_matches.items():
        match_idx, match_title, match_score = match_info
        outputs.loc[idx, "best_match_idx"] = match_idx
        outputs.loc[idx, "best_match_title"] = match_title
        outputs.loc[idx, "best_match_score"] = match_score
    
    # Save all unique records in unique_records
    # Based on whether it is API data
    if API:
        unique_records = outputs.loc[outputs["unique"] == True,
            ['title', 'doi', 'abstract', 'year', 'publication_date',
             'cited_by_count', 'authors', 'affiliations', 'topics',
             'source_display_name', 'type_crossref', 'researcher', 'author_id',
             'queried_dataset_terms', 'matched_dataset_terms', 'location']]
    else:
        unique_records = outputs.loc[outputs["unique"] == True,
            ['title', 'doi', 'abstract', 'year', 'publication_date',
              'cited_by_count', 'authors', 'affiliations', 'topics',
              'source_display_name', 'type_crossref', 'researcher',
              'matched_dataset_terms', 'mention_restricted_data',
              'mention_disclosure_review', 'mention_rdc']]

    
    # Export the unique records into a csv file
    # Based on whether it's API data, give differnt names for files
    if API:
        unique_output_file_name = "unique_research_outputs.csv"
        matched_output_file_name = "matched_research_outputs.csv"
    else:
        unique_output_file_name = "unique_outputs_webscraping.csv"
        matched_output_file_name = "matched_outputs_webscraping.csv"
    unique_records.to_csv(unique_output_file_name, index=False)

    # Save all matched records in matched_records
    matched_records = outputs[outputs["unique"] == False].drop(columns="unique")

    # Export the matched records into a csv file
    matched_records.to_csv(matched_output_file_name, index=False)

    # Print value counts for unique and match records
    print("\nSummary:")
    print(f"{len(outputs)} research outputs in total")
    print(f"- {len(unique_records)} unique research outputs")
    print(f"- {len(matched_records)} non-unique research outputs")
    print()


# Define function to complete Part 3 all steps
def part3_pipeline():
    # Complete everything for API data
    data_pipeline(True)
    # Complete everything for webscrapping data
    data_pipeline(False)

if __name__ == "__main__":
    part3_pipeline()

