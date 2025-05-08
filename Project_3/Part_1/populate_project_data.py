# Import libraries
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz

# Define function to read in data
def read_data():
    # Load in outputs of each group
    print("\nReading in output data of all groups...")
    data1 = pd.read_csv("Data/group1.csv")
    data2 = pd.read_csv("Data/group2.csv")
    data3 = pd.read_csv("Data/group3.csv")
    data4 = pd.read_csv("Data/group4.csv")
    data5 = pd.read_csv("Data/group5.csv")
    data6 = pd.read_csv("Data/group6.csv")
    data7 = pd.read_csv("Data/group7.csv")
    data8 = pd.read_csv("Data/group8.csv")
    print("Completed reading in output data of all groups.\n")

    # Read in all metadata outputs
    print("Reading in all metadata ...")
    url = 'https://raw.githubusercontent.com/dingkaihua/fsrdc-external-census-projects/master/ProjectsAllMetadata.xlsx'
    all_metadata = pd.read_excel(url, sheet_name="All Metadata")
    print("Completed reading in all metadata.\n")

    # Return dfs
    return (data1, data2, data3, data4, data5, data6, data7, data8, all_metadata)

# ---------- Data Preparation for Outputs of All Groups ----------
# Define helper function to copy the df and make all column names lowercase
def lowercase_columns_copy(df):
    print(" Making column names lowercase ...")
    try:
        # Make a copy of the original df
        df_copy = df.copy()

        # Convert all column names to lowercase
        df_copy.columns = df_copy.columns.str.lower()

        print(" Completed making column names lowercase.")

        # Return final df
        return df_copy
    except Exception as e:
        print(f"Error in lowercase_columns_copy: {str(e)}")
        return None

# Define test function for lowercase_columns_copy()
def test_lowercase_columns_copy():
    # Create test DataFrame
    test_df = pd.DataFrame({
        'Name': ['John', 'Jane', 'Alex'],
        'AGE': [25, 30, 35],
        'Job_Title': ['Engineer', 'Doctor', 'Teacher']
    })
    
    # Apply the function
    result_df = lowercase_columns_copy(test_df)
    
    # Check if original DataFrame is unchanged
    assert list(test_df.columns) == ['Name', 'AGE', 'Job_Title'], "Original DataFrame should not be modified"
    # Check if new DataFrame has lowercase columns
    assert list(result_df.columns) == ['name', 'age', 'job_title'], "All column names should be lowercase"
    # Check if data is the same
    assert result_df.values.tolist() == test_df.values.tolist(), "Data values should remain the same"
    print(" [Passed] - Test for function lowercase_columns_copy()")

# Define helper function to add column idx and group in a df
# so that it could help to easily locate the record later
def add_group_idx(df, group_number):
    print(" Adding group and index columns...")
    try:
        # Add group and index columns
        df["group"] = group_number
        df["idx"] = df.index
        print(" Completed adding group and index columns.")
    except Exception as e:
        print(f"Error in add_group_idx: {str(e)}")
        raise

# Define test function for add_group_idx()
def test_add_group_idx():
    # Create test DataFrame
    test_df = pd.DataFrame({
        'product': ['Laptop', 'Phone', 'Tablet'],
        'price': [1000, 800, 500]
    }, index=[0, 1, 2])
    
    # Apply the function with group number 1
    add_group_idx(test_df, 1)
    
    # Check if group column is added with correct value
    assert "group" in test_df.columns, "Group column should be added"
    assert all(test_df['group'] == 1), "All values in group column should be 1"
    # Check if idx column contains the original index values
    assert 'idx' in test_df.columns, "idx column should be added"
    assert test_df['idx'].tolist() == [0, 1, 2], "idx column should contain original index values"
    # Original index should still be preserved
    assert test_df.index.tolist() == [0, 1, 2], "Original index should be preserved"
    print(" [Passed] - Test for function test_add_group_idx()")

# ----- Prepare Group 1 Output Data -----
# Define function to prepare group 1 output data
def prepare_group_1(data1):
    print("Preparing group 1 output data...")
    # Make copy of df and make all column names lowercase
    clean_data1 = lowercase_columns_copy(data1)

    # Rename some of the columns
    try:
        clean_data1 = clean_data1.rename(
            columns={'title': 'OutputTitle', 'project_id': 'ProjID',
                    'project_pi': 'ProjectPI', 'agency': 'ProjectRDC',
                    'project_status': 'ProjectStatus', 'year': 'OutputYear'})
    except Exception as e:
        print(f"Error renaming columns: {str(e)}")
        raise

    # Drop unnecessary columns
    try:
        clean_data1 = clean_data1.drop(columns=['keywords'])
    except Exception as e:
        print(f"Error dropping columns: {str(e)}")
        raise

    # Add columns group and idx to df
    add_group_idx(clean_data1, 1)
    print("Completed preparing group 1 output data.\n")

    # Return the cleaned df
    return clean_data1

# Define test function for prepare_group_1()
def test_prepare_group_1():
    # Create a test dataframe
    test_data = pd.DataFrame({
        'title': ['Sample Title'],
        'project_id': [123],
        'project_pi': ['John Doe'],
        'agency': ['RDC Agency'],
        'project_status': ['Active'],
        'year': [2023],
        'keywords': ['test, sample']
    })

    # Call the function with the test data
    result = prepare_group_1(test_data)

    # Assert that the result is a dataframe
    assert isinstance(result, pd.DataFrame), "Result is not a DataFrame"

    # Assert that column names were renamed correctly
    assert 'OutputTitle' in result.columns, "Column 'title' was not renamed to 'OutputTitle'"
    assert 'ProjID' in result.columns, "Column 'project_id' was not renamed to 'ProjID'"
    assert 'ProjectPI' in result.columns, "Column 'project_pi' was not renamed to 'ProjectPI'"
    assert 'ProjectRDC' in result.columns, "Column 'agency' was not renamed to 'ProjectRDC'"
    assert 'ProjectStatus' in result.columns, "Column 'project_status' was not renamed to 'ProjectStatus'"
    assert 'OutputYear' in result.columns, "Column 'year' was not renamed to 'OutputYear'"

    # Assert that unwanted columns were dropped
    assert 'keywords' not in result.columns, "Column 'keywords' was not dropped"

    # Assert that group and idx columns were added
    assert 'group' in result.columns, "Column 'group' was not added"
    assert 'idx' in result.columns, "Column 'idx' was not added"

    # Assert group value is correct
    assert result['group'].iloc[0] == 1, "Group value is not set to 1"
    print(" [Passed] - Test for function prepare_group_1()")

# ----- Prepare Group 2 Output Data -----
# Define function to prepare group 2 output data
def prepare_group_2(data2):
    print("Preparing group 2 output data...")
    # Make copy of df and make all column names lowercase
    clean_data2 = lowercase_columns_copy(data2)

    # Rename some of the columns
    try:
        clean_data2 = clean_data2.rename(
            columns={'title': 'OutputTitle', 'year': 'OutputYear',
                    'type_crossref': 'OutputType', 'author_id': 'openalex_id',
                    'location': 'ProjectRDC'})
    except Exception as e:
        print(f"Error renaming columns: {str(e)}")
        raise

    # Get rid of brackets in authors column to make it consistent
    # Get rid of single and double qutoation marks
    # Replace comma with semicolon too
    clean_data2["authors"] = (clean_data2["authors"]
                            .str.replace("{", "")
                            .str.replace("}", "")
                            .str.replace("'", "")
                            .str.replace('"', "")
                            .str.replace(",", ";")
                            .str.strip())

    # Drop unneccessary columns
    try:
        clean_data2 = clean_data2.drop(
            columns=['publication_date', 'cited_by_count', 'topics'])
    except Exception as e:
        print(f"Error dropping columns: {str(e)}")
        raise

    # Add columns group and idx to df
    add_group_idx(clean_data2, 2)
    print("Completed preparing group 2 output data.\n")

    # Return the cleaned df
    return clean_data2

# Define test function for prepare_group_2()
def test_prepare_group_2():
    # Create a test dataframe
    test_data = pd.DataFrame({
        'title': ['Sample Title'],
        'year': [2023],
        'type_crossref': ['Article'],
        'author_id': ['A12345'],
        'location': ['RDC Location'],
        'authors': ["{'John Doe', 'Jane Smith'}"],
        'publication_date': ['2023-01-01'],
        'cited_by_count': [10],
        'topics': ['economics, data']
    })

    # Call the function with the test data
    result = prepare_group_2(test_data)

    # Assert that the result is a dataframe
    assert isinstance(result, pd.DataFrame), "Result is not a DataFrame"
    
    # Assert that column names were renamed correctly
    assert 'OutputTitle' in result.columns, "Column 'title' was not renamed to 'OutputTitle'"
    assert 'OutputYear' in result.columns, "Column 'year' was not renamed to 'OutputYear'"
    assert 'OutputType' in result.columns, "Column 'type_crossref' was not renamed to 'OutputType'"
    assert 'openalex_id' in result.columns, "Column 'author_id' was not renamed to 'openalex_id'"
    assert 'ProjectRDC' in result.columns, "Column 'location' was not renamed to 'ProjectRDC'"
    
    # Assert that authors column was cleaned properly
    assert result['authors'].iloc[0] == "John Doe; Jane Smith", "Authors column was not cleaned correctly"
    
    # Assert that unwanted columns were dropped
    assert 'publication_date' not in result.columns, "Column 'publication_date' was not dropped"
    assert 'cited_by_count' not in result.columns, "Column 'cited_by_count' was not dropped"
    assert 'topics' not in result.columns, "Column 'topics' was not dropped"

    # Assert that group and idx columns were added
    assert 'group' in result.columns, "Column 'group' was not added"
    assert 'idx' in result.columns, "Column 'idx' was not added"

    # Assert group value is correct
    assert result['group'].iloc[0] == 2, "Group value is not set to 2"
    print(" [Passed] - Test for function prepare_group_2()")

# ----- Prepare Group 3 Output Data -----
# Define function to prepare group 3 output data
def prepare_group_3(data3):
    print("Preparing group 3 output data...")
    # Make copy of df and make all column names lowercase
    clean_data3 = lowercase_columns_copy(data3)

    # Rename some of the columns
    try:
        clean_data3 = clean_data3.rename(
            columns={'title': 'OutputTitle', 'rdc': 'ProjectRDC',
                    'start year': 'ProjectYearStarted',
                    'end year': 'ProjectYearEnded',
                    'pi': 'ProjectPI', 'publication_year': 'OutputYear',
                    'is_published': 'OutputStatus', 'type_crossref': 'OutputType',
                    'author': 'authors','author_affiliation': 'affiliations'})
    except Exception as e:
        print(f"Error renaming columns: {str(e)}")
        raise

    # Drop unneccessary columns
    try:
        clean_data3 = clean_data3.drop(
            columns=['unnamed: 0', '# of papers', '# of fsrdc-relevant papers',
                    'fsrdc evidence', 'has fsrdc evidence?', 'cited_by_count', 
                    'primary_topic', 'field', 'updated_date', 'author_address_locality',
                    'author_address_region', 'author_address_country', 'data_source',
                    'keywords', 'record_id'])
    except Exception as e:
        print(f"Error dropping columns: {str(e)}")
        raise

    # Add columns group and idx to df
    add_group_idx(clean_data3, 3)
    print("Completed preparing group 3 output data.\n")

    # Return the cleaned df
    return clean_data3

# Define test function for prepare_group_3()
def test_prepare_group_3():
    # Create a test datafram
    test_data = pd.DataFrame({
        'title': ['Sample Title'],
        'rdc': ['Test RDC'],
        'start year': [2020],
        'end year': [2023],
        'pi': ['Jane Doe'],
        'publication_year': [2022],
        'is_published': ['Yes'],
        'type_crossref': ['Article'],
        'author': ['John Smith'],
        'author_affiliation': ['University'],
        'unnamed: 0': [1],
        '# of papers': [5],
        '# of fsrdc-relevant papers': [3],
        'fsrdc evidence': ['Yes'],
        'has fsrdc evidence?': [True],
        'cited_by_count': [10],
        'primary_topic': ['Economics'],
        'field': ['Social Science'],
        'updated_date': ['2023-01-01'],
        'author_address_locality': ['City'],
        'author_address_region': ['State'],
        'author_address_country': ['Country'],
        'data_source': ['Source'],
        'keywords': ['research, census'],
        'record_id': [12345]
    })
    
    # Call the function with the test data
    result = prepare_group_3(test_data)
    
    # Assert that the result is a dataframe
    assert isinstance(result, pd.DataFrame), "Result is not a DataFrame"
    
    # Assert that column names were renamed correctly
    assert 'OutputTitle' in result.columns, "Column 'title' was not renamed correctly"
    assert 'ProjectRDC' in result.columns, "Column 'rdc' was not renamed correctly"
    assert 'ProjectYearStarted' in result.columns, "Column 'start year' was not renamed correctly"
    assert 'ProjectYearEnded' in result.columns, "Column 'end year' was not renamed correctly"
    assert 'ProjectPI' in result.columns, "Column 'pi' was not renamed correctly"
    assert 'OutputYear' in result.columns, "Column 'publication_year' was not renamed correctly"
    assert 'OutputStatus' in result.columns, "Column 'is_published' was not renamed correctly"
    assert 'OutputType' in result.columns, "Column 'type_crossref' was not renamed correctly"
    assert 'authors' in result.columns, "Column 'author' was not renamed correctly"
    assert 'affiliations' in result.columns, "Column 'author_affiliation' was not renamed correctly"
    
    # Assert that unwanted columns were dropped
    dropped_columns = ['unnamed: 0', '# of papers', '# of fsrdc-relevant papers',
                      'fsrdc evidence', 'has fsrdc evidence?', 'cited_by_count', 
                      'primary_topic', 'field', 'updated_date', 'author_address_locality',
                      'author_address_region', 'author_address_country', 'data_source',
                      'keywords', 'record_id']
    
    for col in dropped_columns:
        assert col not in result.columns, f"Column '{col}' was not dropped"
    
    # Assert that group and idx columns were added
    assert 'group' in result.columns, "Column 'group' was not added"
    assert 'idx' in result.columns, "Column 'idx' was not added"
    
    # Assert group value is correct
    assert result['group'].iloc[0] == 3, "Group value is not set to 3"
    
    print(" [Passed] - Test for function prepare_group_3()")

# ----- Prepare Group 4 Output Data -----
# Define function to prepare group 4 output data
def prepare_group_4(data4):
    print("Preparing group 4 output data...")
    # Make copy of df and make all column names lowercase
    clean_data4 = lowercase_columns_copy(data4)

    # Rename some of the columns
    try:
        clean_data4 = clean_data4.rename(
            columns={'title': 'OutputTitle','year': 'OutputYear'})
    except Exception as e:
        print(f"Error renaming columns: {str(e)}")
        raise

    # Drop unnecessary column
    try:
        clean_data4 = clean_data4.drop(
            columns=['citations', 'has_fsrdc_evidence'])
    except Exception as e:
        print(f"Error dropping columns: {str(e)}")
        raise

    # clean author column, get rid of double quotation mark and ()
    clean_data4['authors'] = clean_data4['authors'].str.replace('"', '')
    clean_data4["authors"] = clean_data4["authors"].str.replace(r"\(.*\);", "", regex=True)
    clean_data4["authors"] = clean_data4["authors"].str.replace(r"\(.*\)", "", regex=True)

    # Add columns group and idx to df
    add_group_idx(clean_data4, 4)
    print("Completed preparing group 4 output data.\n")

    # Return the cleaned df
    return clean_data4

# Define test function for prepare_group_4()
def test_prepare_group_4():
    # Create a test dataframe
    test_data = pd.DataFrame({
        'title': ['Sample Article'],
        'year': [2022],
        'authors': ['"Smith, John (Harvard); "Jones, Mary (Stanford)"'],
        'citations': [25],
        'has_fsrdc_evidence': [True]
    })
    
    # Call the function with the test data
    result = prepare_group_4(test_data)
    
    # Assert that the result is a dataframe
    assert isinstance(result, pd.DataFrame), "Result is not a DataFrame"
    
    # Assert that column names were renamed correctly
    assert 'OutputTitle' in result.columns, "Column 'title' was not renamed to 'OutputTitle'"
    assert 'OutputYear' in result.columns, "Column 'year' was not renamed to 'OutputYear'"
    
    # Assert that unwanted columns were dropped
    assert 'citations' not in result.columns, "Column 'citations' was not dropped"
    assert 'has_fsrdc_evidence' not in result.columns, "Column 'has_fsrdc_evidence' was not dropped"
    
    # Assert that authors column was cleaned properly
    assert '"' not in result['authors'].iloc[0], "Double quotes were not removed from authors column"
    assert '(' not in result['authors'].iloc[0], "Parentheses were not removed from authors column"
    assert ')' not in result['authors'].iloc[0], "Parentheses were not removed from authors column"
    
    # Assert that group and idx columns were added
    assert 'group' in result.columns, "Column 'group' was not added"
    assert 'idx' in result.columns, "Column 'idx' was not added"
    
    # Assert group value is correct
    assert result['group'].iloc[0] == 4, "Group value is not set to 4"
    
    print(" [Passed] - Test for function prepare_group_4()")

# ----- Prepare Group 5 Output Data -----
# Define function to prepare group 5 output data
def prepare_group_5(data5):
    print("Preparing group 5 output data...")
    # Make copy of df and make all column names lowercase
    clean_data5 = lowercase_columns_copy(data5)

    # Rename some of the columns
    try:
        clean_data5 = clean_data5.rename(
            columns={'pi': 'ProjectPI', 'year': 'OutputYear',
                    'title': 'OutputTitle'})
    except Exception as e:
        print(f"Error renaming columns: {str(e)}")
        raise

    # Drop unnecessary column
    try:
        clean_data5 = clean_data5.drop(columns=["title_clean"])
    except Exception as e:
        print(f"Error dropping columns: {str(e)}")
        raise

    # Add columns group and idx to df
    add_group_idx(clean_data5, 5)
    print("Completed preparing group 5 output data.\n")

    # Return the cleaned df
    return clean_data5

# Define test function for prepare_group_5()
def test_prepare_group_5():
    # Create a test dataframe
    test_data = pd.DataFrame({
        'pi': ['Dr. Jane Smith'],
        'year': [2021],
        'title': ['Research on Economic Impacts'],
        'title_clean': ['research economic impacts']
    })
    
    # Call the function with the test data
    result = prepare_group_5(test_data)
    
    # Assert that the result is a dataframe
    assert isinstance(result, pd.DataFrame), "Result is not a DataFrame"
    
    # Assert that column names were renamed correctly
    assert 'ProjectPI' in result.columns, "Column 'pi' was not renamed to 'ProjectPI'"
    assert 'OutputYear' in result.columns, "Column 'year' was not renamed to 'OutputYear'"
    assert 'OutputTitle' in result.columns, "Column 'title' was not renamed to 'OutputTitle'"
    
    # Assert that unwanted column was dropped
    assert 'title_clean' not in result.columns, "Column 'title_clean' was not dropped"
    
    # Assert that group and idx columns were added
    assert 'group' in result.columns, "Column 'group' was not added"
    assert 'idx' in result.columns, "Column 'idx' was not added"
    
    # Assert group value is correct
    assert result['group'].iloc[0] == 5, "Group value is not set to 5"
    
    print(" [Passed] - Test for function prepare_group_5()")

# ----- Prepare Group 6 Output Data -----
# Define function to prepare group 6 output data
def prepare_group_6(data6):
    print("Preparing group 6 output data...")
    # Make copy of df and make all column names lowercase
    clean_data6 = lowercase_columns_copy(data6)

    # Rename some of the columns
    try:
        clean_data6 = clean_data6.rename(
            columns={'title': 'OutputTitle', 'researchers': 'researcher',
                    'year': 'OutputYear', 'rdc': 'ProjectRDC'})
    except Exception as e:
        print(f"Error renaming columns: {str(e)}")
        raise

    # Drop unnecessary column
    try:
        clean_data6 = clean_data6.drop(
            columns=['no. researchers', 'keywords'])
    except Exception as e:
        print(f"Error dropping columns: {str(e)}")
        raise

    # Add columns group and idx to df
    add_group_idx(clean_data6, 6)
    print("Completed preparing group 6 output data.\n")

    # Return the cleaned df
    return clean_data6

# Define test function for prepare_group_6()
def test_prepare_group_6():
    # Create a test dataframe
    test_data = pd.DataFrame({
        'title': ['Impact of Policy Changes'],
        'researchers': ['John Smith, Jane Doe'],
        'year': [2022],
        'rdc': ['Census RDC'],
        'no. researchers': [2],
        'keywords': ['policy, economics, census']
    })
    
    # Call the function with the test data
    result = prepare_group_6(test_data)
    
    # Assert that the result is a dataframe
    assert isinstance(result, pd.DataFrame), "Result is not a DataFrame"
    
    # Assert that column names were renamed correctly
    assert 'OutputTitle' in result.columns, "Column 'title' was not renamed to 'OutputTitle'"
    assert 'researcher' in result.columns, "Column 'researchers' was not renamed to 'researcher'"
    assert 'OutputYear' in result.columns, "Column 'year' was not renamed to 'OutputYear'"
    assert 'ProjectRDC' in result.columns, "Column 'rdc' was not renamed to 'ProjectRDC'"
    
    # Assert that unwanted columns were dropped
    assert 'no. researchers' not in result.columns, "Column 'no. researchers' was not dropped"
    assert 'keywords' not in result.columns, "Column 'keywords' was not dropped"
    
    # Assert that group and idx columns were added
    assert 'group' in result.columns, "Column 'group' was not added"
    assert 'idx' in result.columns, "Column 'idx' was not added"
    
    # Assert group value is correct
    assert result['group'].iloc[0] == 6, "Group value is not set to 6"
    
    print(" [Passed] - Test for function prepare_group_6()")

# ----- Prepare Group 7 Output Data -----
# Define function to prepare group 7 output data
def prepare_group_7(data7):
    print("Preparing group 7 output data...")
    # Make copy of df and make all column names lowercase
    clean_data7 = lowercase_columns_copy(data7)

    # Rename some of the columns
    try:
        clean_data7 = clean_data7.rename(columns={'title': 'OutputTitle'})
    except Exception as e:
        print(f"Error renaming columns: {str(e)}")
        raise

    # Drop unnecessary column
    try:
        clean_data7 = clean_data7.drop(columns=['is_fsrdc'])
    except Exception as e:
        print(f"Error dropping columns: {str(e)}")
        raise

    # Add columns group and idx to df
    add_group_idx(clean_data7, 7)
    print("Completed preparing group 7 output data.\n")

    # Return the cleaned df
    return clean_data7

# Define test function for prepare_group_7()
def test_prepare_group_7():
    # Create a test dataframe
    test_data = pd.DataFrame({
        'title': ['Economic Analysis Study'],
        'is_fsrdc': [True],
        'other_column': ['Some data']  # Added to ensure other columns remain
    })
    
    # Call the function with the test data
    result = prepare_group_7(test_data)
    
    # Assert that the result is a dataframe
    assert isinstance(result, pd.DataFrame), "Result is not a DataFrame"
    
    # Assert that column name was renamed correctly
    assert 'OutputTitle' in result.columns, "Column 'title' was not renamed to 'OutputTitle'"
    
    # Assert that unwanted column was dropped
    assert 'is_fsrdc' not in result.columns, "Column 'is_fsrdc' was not dropped"
    
    # Assert that other columns remain unchanged
    assert 'other_column' in result.columns, "Other columns were incorrectly affected"
    
    # Assert that group and idx columns were added
    assert 'group' in result.columns, "Column 'group' was not added"
    assert 'idx' in result.columns, "Column 'idx' was not added"
    
    # Assert group value is correct
    assert result['group'].iloc[0] == 7, "Group value is not set to 7"
    
    print(" [Passed] - Test for function prepare_group_7()")

# ----- Prepare Group 8 Output Data -----
# Define function to prepare group 8 output data
def prepare_group_8(data8):
    print("Preparing group 8 output data...")
    # Make copy of df and rename some of the columns
    try:
        clean_data8 = data8.copy().rename(
            columns={'DOI': 'doi', 'Authors': 'authors',
                    'Abstract': 'abstract', 'ProjectPI': 'researcher'})
    except Exception as e:
        print(f"Error renaming columns: {str(e)}")
        raise

    # Use semicolon to separate different ProjectPI
    clean_data8["researcher"] = (clean_data8["researcher"]
                                .str.replace('&', ';'))

    # Change comma separted ProjectPI to semicolon separated
    clean_data8.loc[~clean_data8["researcher"].str.contains(';', na=True), "researcher"] = (
        clean_data8.loc[~clean_data8["researcher"].str.contains(';', na=True), "researcher"].str.replace(',', ';')
    )

    # Change & separted ProjectPI to semicolon separated
    clean_data8["authors"] = (clean_data8["authors"]
                            .str.replace('&', ';'))

    # Change comma separted authors to semicolon separated
    clean_data8.loc[~clean_data8["authors"].str.contains(';', na=True), "authors"] = (
        clean_data8.loc[~clean_data8["authors"].str.contains(';', na=True), "authors"].str.replace(',', ';')
    )

    # Drop unnecessary column
    try:
        clean_data8 = clean_data8.drop(
            columns=['Unnamed: 0', 'ProjectID', 'ProjectStatus', 'ProjectRDC',
                    'ProjectStartYear', 'ProjectEndYear', 'OutputBiblio', 
                    'OutputStatus', 'OutputVenue', 'OutputMonth', 'DoiExtract', 
                    'NormTitle', 'MatchType', 'Uniqueness', 'FuzzScores',
                    'FSRDC_related'])
    except Exception as e:
        print(f"Error dropping columns: {str(e)}")
        raise

    # Add columns group and idx to df
    add_group_idx(clean_data8, 8)
    print("Completed preparing group 8 output data.\n")

    # Return the cleaned df
    return clean_data8

# Define test function for prepare_group_8()
def test_prepare_group_8():
    # Create a test dataframe
    test_data = pd.DataFrame({
        'DOI': ['10.1234/abcd'],
        'Authors': ['Smith, J & Doe, J'],
        'Abstract': ['This is a test abstract.'],
        'ProjectPI': ['Johnson, A & Williams, B'],
        'Unnamed: 0': [1],
        'ProjectID': ['P12345'],
        'ProjectStatus': ['Active'],
        'ProjectRDC': ['Census'],
        'ProjectStartYear': [2020],
        'ProjectEndYear': [2023],
        'OutputBiblio': ['Citation info'],
        'OutputStatus': ['Published'],
        'OutputVenue': ['Journal'],
        'OutputMonth': [6],
        'DoiExtract': ['extract'],
        'NormTitle': ['normalized'],
        'MatchType': ['exact'],
        'Uniqueness': [0.95],
        'FuzzScores': [0.85],
        'FSRDC_related': [True],
        'OutputTitle': ['Research Paper Title'],  # Keeping this column
        'OutputYear': [2022]  # Keeping this column
    })
    
    # Call the function with the test data
    result = prepare_group_8(test_data)
    
    # Assert that the result is a dataframe
    assert isinstance(result, pd.DataFrame), "Result is not a DataFrame"
    
    # Assert that column names were renamed correctly
    assert 'doi' in result.columns, "Column 'DOI' was not renamed to 'doi'"
    assert 'authors' in result.columns, "Column 'Authors' was not renamed to 'authors'"
    assert 'abstract' in result.columns, "Column 'Abstract' was not renamed to 'abstract'"
    assert 'researcher' in result.columns, "Column 'ProjectPI' was not renamed to 'researcher'"
    
    # Assert that authors and researcher columns were formatted correctly
    assert '&' not in result['authors'].iloc[0], "& characters were not removed from authors"
    assert '&' not in result['researcher'].iloc[0], "& characters were not removed from researcher"
    assert ';' in result['authors'].iloc[0], "Semicolons not added to authors"
    assert ';' in result['researcher'].iloc[0], "Semicolons not added to researcher"
    
    # Assert that unwanted columns were dropped
    columns_to_drop = ['Unnamed: 0', 'ProjectID', 'ProjectStatus', 'ProjectRDC',
                      'ProjectStartYear', 'ProjectEndYear', 'OutputBiblio', 
                      'OutputStatus', 'OutputVenue', 'OutputMonth', 'DoiExtract', 
                      'NormTitle', 'MatchType', 'Uniqueness', 'FuzzScores',
                      'FSRDC_related']
    
    for col in columns_to_drop:
        assert col not in result.columns, f"Column '{col}' was not dropped"
    
    # Assert that other columns remain
    assert 'OutputTitle' in result.columns, "Column 'OutputTitle' was incorrectly affected"
    assert 'OutputYear' in result.columns, "Column 'OutputYear' was incorrectly affected"
    
    # Assert that group and idx columns were added
    assert 'group' in result.columns, "Column 'group' was not added"
    assert 'idx' in result.columns, "Column 'idx' was not added"
    
    # Assert group value is correct
    assert result['group'].iloc[0] == 8, "Group value is not set to 8"
    
    print(" [Passed] - Test for function prepare_group_8()")

# ----- Prepare All_Metadata Data -----
# Define function to prepare all metadata
def prepare_project_data(all_metadata):
    print("Preparing all_metadata...")
    # Extract unique project information in all_metadata
    try:
        project = (
            all_metadata
            .drop_duplicates(
                subset=['Proj ID', 'Status', 'Title', 'RDC', 'Start Year', 'End Year', 'PI']
            )[['Proj ID', 'Status', 'Title', 'RDC', 'Start Year', 'End Year', 'PI']])
    except Exception as e:
        print(f"Error extracting unique project information: {str(e)}")
        raise
    print("Completed preparing all_metadata.\n")

    # Return the df with unique projects
    return project

# Define test function for prepare_project_data()
def test_prepare_project_data():
    # Create a test dataframe
    test_data = pd.DataFrame({
        'Proj ID': ['P001', 'P001', 'P002', 'P003', 'P003'],
        'Status': ['Active', 'Active', 'Completed', 'Active', 'Active'],
        'Title': ['Project A', 'Project A', 'Project B', 'Project C', 'Project C'],
        'RDC': ['Census', 'Census', 'Federal', 'State', 'State'],
        'Start Year': [2020, 2020, 2019, 2021, 2021],
        'End Year': [2023, 2023, 2022, 2024, 2024],
        'PI': ['Dr. Smith', 'Dr. Smith', 'Dr. Jones', 'Dr. Williams', 'Dr. Williams'],
        'Extra Column 1': ['Value1', 'Value2', 'Value3', 'Value4', 'Value5'],
        'Extra Column 2': [10, 20, 30, 40, 50]
    })
    
    # Call the function with the test data
    result = prepare_project_data(test_data)
    
    # Assert that the result is a dataframe
    assert isinstance(result, pd.DataFrame), "Result is not a DataFrame"
    
    # Assert that only the specified columns are present
    expected_columns = ['Proj ID', 'Status', 'Title', 'RDC', 'Start Year', 'End Year', 'PI']
    for col in expected_columns:
        assert col in result.columns, f"Column '{col}' is missing"
    assert len(result.columns) == len(expected_columns), "Extra columns were included"
    
    # Assert that duplicates were removed
    assert len(result) == 3, "Duplicates were not removed correctly"
    
    # Assert that the content is correct - unique project IDs
    proj_ids = result['Proj ID'].tolist()
    assert set(proj_ids) == {'P001', 'P002', 'P003'}, "Unique project IDs not preserved correctly"
    
    print(" [Passed] - Test for function prepare_project_data()")

# ---------- Data Integration ----------
# Define function to integrate all group output data
def integrate_groups_data(clean_data1, clean_data2, clean_data3,
                          clean_data4, clean_data5,clean_data6,
                          clean_data7, clean_data8):
    print("Integrating all group output data...")
    # Get set of all columns in all 8 dfs
    all_cols_set = set()
    for i in range(1,9):
        # Get the df for group i
        df_name = eval(f"clean_data{i}")
        # Add all columns in df to cols_set
        all_cols_set = all_cols_set | set(df_name.columns)

    # Make copy of all clean_data dfs
    for i in range(1, 9):
        # Create a copy expanded_data
        globals()[f"expanded_data{i}"] = eval(f"clean_data{i}").copy()

    # Add columns that are not in the df to each of the dataframe
    for i in range(1,9):
        # Get the df for group i
        df_name = eval(f"expanded_data{i}")
        # Add all columns that are not in this df
        for col in (all_cols_set - set(df_name.columns)):
            df_name[col] = np.nan

    # Concatenate all data
    combined_data = pd.concat([expanded_data1, expanded_data2, expanded_data3,
                            expanded_data4, expanded_data5, expanded_data6,
                            expanded_data7, expanded_data8], ignore_index=True)
    print("Completed integrating all group output data.\n")

    # Define the new column order
    cols_order = ['group', 'idx', 'doi', 'source', 'url',
                'authors', 'researcher',
                'acknowledgments', 'fsrdc_acknowledgments_evidence',
                'data_descriptions',
                'dataset mentions','dataset_mentions', 'fsrdc_data_sources_evidence',
                'matched_dataset_terms', 'queried_dataset_terms',
                'disclosure_review', 'fsrdc_disclosure_evidence',
                'rdc_mentions', 'fsrdc_rdc_locations_evidence',
                'agency',
                'abstract',
                'affiliations', 'raw_affiliation_strings', 'detailed_affiliations',
                'host_organization_name',
                'institution_display_names',
                'openalex_id', 'orcid_id',
                'source_display_name',
                'ProjID', 'ProjectStatus', 'ProjectTitle', 'ProjectRDC',
                'ProjectYearStarted', 'ProjectYearEnded', 'ProjectPI',
                'OutputTitle', 'OutputType', 'OutputStatus', 'OutputYear',
                'OutputVolume', 'OutputNumber', 'OutputPages']

    try:
        # Reorder the columns using the new order
        combined_data = combined_data.reindex(columns=cols_order)
    except Exception as e:
        print(f"Error reordering columns: {str(e)}")
        raise

    # Return the combine data
    return combined_data

# Define test function for integrate_groups_data()
def test_integrate_groups_data():
    # Create minimal test dataframes for each group with different column structures
    # Each group has different columns to test the column merging logic
    test_data1 = pd.DataFrame({
        'group': [1], 'idx': [1], 'OutputTitle': ['Title 1'], 'ProjID': ['P001']
    })
    
    test_data2 = pd.DataFrame({
        'group': [2], 'idx': [1], 'OutputTitle': ['Title 2'], 'openalex_id': ['A123'], 
        'authors': ['Author 2']
    })
    
    test_data3 = pd.DataFrame({
        'group': [3], 'idx': [1], 'OutputTitle': ['Title 3'], 'ProjectRDC': ['RDC 3'],
        'OutputYear': [2021]
    })
    
    test_data4 = pd.DataFrame({
        'group': [4], 'idx': [1], 'OutputTitle': ['Title 4'], 'authors': ['Author 4']
    })
    
    test_data5 = pd.DataFrame({
        'group': [5], 'idx': [1], 'OutputTitle': ['Title 5'], 'ProjectPI': ['PI 5']
    })
    
    test_data6 = pd.DataFrame({
        'group': [6], 'idx': [1], 'OutputTitle': ['Title 6'], 'researcher': ['Researcher 6']
    })
    
    test_data7 = pd.DataFrame({
        'group': [7], 'idx': [1], 'OutputTitle': ['Title 7'], 'doi': ['10.1234/abcd']
    })
    
    test_data8 = pd.DataFrame({
        'group': [8], 'idx': [1], 'OutputTitle': ['Title 8'], 'abstract': ['Abstract 8']
    })
    
    # Call the function with the test data
    result = integrate_groups_data(test_data1, test_data2, test_data3, test_data4, 
                                 test_data5, test_data6, test_data7, test_data8)
    
    # Assert that the result is a dataframe
    assert isinstance(result, pd.DataFrame), "Result is not a DataFrame"
    
    # Assert that all rows from all groups are present
    assert len(result) == 8, "Not all rows from all groups are present"
    
    # Assert that all groups are represented
    assert set(result['group']) == {1, 2, 3, 4, 5, 6, 7, 8}, "Not all groups are represented"
    
    # Assert that columns from all groups are present
    assert 'ProjID' in result.columns, "Column from group 1 is missing"
    assert 'openalex_id' in result.columns, "Column from group 2 is missing"
    assert 'ProjectRDC' in result.columns, "Column from group 3 is missing"
    assert 'authors' in result.columns, "Shared column is missing"
    assert 'ProjectPI' in result.columns, "Column from group 5 is missing"
    assert 'researcher' in result.columns, "Column from group 6 is missing"
    assert 'doi' in result.columns, "Column from group 7 is missing"
    assert 'abstract' in result.columns, "Column from group 8 is missing"
    
    # Assert that columns are in the correct order (check a few key columns)
    cols_list = result.columns.tolist()
    assert cols_list.index('group') < cols_list.index('doi'), "Column 'group' is not before 'doi'"
    assert cols_list.index('doi') < cols_list.index('authors'), "Column 'doi' is not before 'authors'"
    assert cols_list.index('abstract') < cols_list.index('ProjID'), "Column 'abstract' is not before 'ProjID'"
    assert cols_list.index('ProjectPI') < cols_list.index('OutputTitle'), "Column 'ProjectPI' is not before 'OutputTitle'"
    
    # Assert that NaN values were added for missing columns in each group
    assert pd.isna(result.loc[result['group'] == 1, 'doi'].iloc[0]), "NaN not added for missing column in group 1"
    assert pd.isna(result.loc[result['group'] == 2, 'abstract'].iloc[0]), "NaN not added for missing column in group 2"
    assert pd.isna(result.loc[result['group'] == 3, 'doi'].iloc[0]), "NaN not added for missing column in group 3"
    
    print(" [Passed] - Test for function integrate_groups_data()")

# ---------- Data Cleaning ----------
# ----- Clean DOI column -----
# Define function to clean DOI column
def clean_doi(combined_data):
    try:
        # There are some incomplete DOI values
        # Complete incomplete DOI
        combined_data.loc[~combined_data["doi"].str.contains("http", na=True), "doi"] = (
            "https://doi.org/" + combined_data.loc[~combined_data["doi"].str.contains("http", na=True), "doi"].str.strip()
        )
        # Check if there is no incomplete doi left after the change
        assert len(combined_data[~combined_data["doi"].str.contains("http", na=True)]) == 0
        print(" Completed cleaning doi column.")
    except Exception as e:
        print(f"Error cleaning DOI column: {str(e)}")
        raise

    # Return clean data
    return combined_data

# Define test function for clean_doi()
def test_clean_doi():
    # Create a test dataframe
    test_data = pd.DataFrame({
        'doi': [
            '10.1234/abcd',                # Plain DOI without http
            'https://doi.org/10.5678/efgh', # Complete DOI with https
            'http://doi.org/10.9012/ijkl',  # Complete DOI with http
            np.nan,                         # Missing DOI
            '  10.3456/mnop  '              # DOI with whitespace
        ],
        'other_column': ['A', 'B', 'C', 'D', 'E']  # Other column for completeness
    })
    
    # Create a copy to compare before/after
    expected_data = test_data.copy()
    expected_data['doi'] = [
        'https://doi.org/10.1234/abcd',     # Should be prefixed
        'https://doi.org/10.5678/efgh',     # Should remain unchanged
        'http://doi.org/10.9012/ijkl',      # Should remain unchanged
        np.nan,                             # Should remain NaN
        'https://doi.org/10.3456/mnop'      # Should be trimmed and prefixed
    ]
    
    # Call the function with the test data
    test_data = clean_doi(test_data)
    
    # Assert that DOIs were properly formatted
    # Check each row individually to handle NaN values
    assert test_data.iloc[0]['doi'] == 'https://doi.org/10.1234/abcd', "Plain DOI not properly formatted"
    assert test_data.iloc[1]['doi'] == 'https://doi.org/10.5678/efgh', "Complete HTTPS DOI was modified"
    assert test_data.iloc[2]['doi'] == 'http://doi.org/10.9012/ijkl', "Complete HTTP DOI was modified"
    assert pd.isna(test_data.iloc[3]['doi']), "NaN DOI was modified"
    assert test_data.iloc[4]['doi'] == 'https://doi.org/10.3456/mnop', "DOI with whitespace not properly cleaned"
    
    # Assert that all non-NaN DOIs now contain 'http'
    mask = ~test_data['doi'].isna()
    assert test_data.loc[mask, 'doi'].str.contains('http').all(), "Not all DOIs contain 'http'"
    
    # Assert that other columns remain unchanged
    assert (test_data['other_column'] == expected_data['other_column']).all(), "Other columns were modified"
    
    print(" [Passed] - Test for function clean_doi()")

# ----- Clean source and url column -----
# Define function to clean source and url columns
def clean_source_url(combined_data):
    try:
        # url only exists when source is arXiv, other sources don't have urls
        # Drop column source and rename url column
        combined_data = combined_data.drop(columns="source")
        combined_data = combined_data.rename(columns={'url': 'arxiv_url'})
        print(" Completed cleaning source and url column.")
    except Exception as e:
        print(f"Error cleaning source and URL columns: {str(e)}")
        raise

    # Return clean data
    return combined_data

# Define test function for clean_source_url()
def test_clean_source_url():
    # Create a test dataframe
    test_data = pd.DataFrame({
        'source': ['arXiv', 'Journal', 'Conference', np.nan],
        'url': ['https://arxiv.org/abs/1234.5678', np.nan, np.nan, np.nan],
        'other_column': ['A', 'B', 'C', 'D']  # Other column for completeness
    })
    
    # Make a function call that modifies the test_data in place
    test_data = clean_source_url(test_data)
    
    # Assert that 'source' column has been dropped
    assert 'source' not in test_data.columns, "Column 'source' was not dropped"
    
    # Assert that 'url' column has been renamed to 'arxiv_url'
    assert 'url' not in test_data.columns, "Column 'url' was not renamed"
    assert 'arxiv_url' in test_data.columns, "Column 'arxiv_url' was not created"
    
    # Assert that the content of the renamed column remains the same
    assert test_data['arxiv_url'].iloc[0] == 'https://arxiv.org/abs/1234.5678', "URL values were altered"
    assert pd.isna(test_data['arxiv_url'].iloc[1]), "Non-arXiv URL values were altered"
    
    # Assert that other columns remain unchanged
    assert 'other_column' in test_data.columns, "Other columns were affected"
    assert test_data['other_column'].iloc[0] == 'A', "Values in other columns were altered"
    
    print(" [Passed] - Test for function clean_source_url()")

# ----- Clean authors and researcher column -----
# Define function to clean authors and researcher columns
def clean_authors_researcher(combined_data):
    try:
        # Combine authors and researcher column
        combined_data["authors_all"] = combined_data["researcher"].fillna("") + combined_data["authors"].fillna("")
        # Split column based on semicolon and save in set
        combined_data['authors_set'] = combined_data["authors_all"].apply(
            lambda x: {author.strip().lower() for author in x.split(';')}
        )
        combined_data[["authors", "researcher", "authors_all", "authors_set"]].head()
        print(" Completed cleaning authors and researcher column.")
    except Exception as e:
        print(f"Error cleaning authors and researcher columns: {str(e)}")
        raise

    # Return clean data
    return combined_data

# Define test function for clean_authors_researcher()
def test_clean_authors_researcher():
    # Create a minimal test dataframe
    test_data = pd.DataFrame({
        'authors': ['John Smith; Jane Doe'],
        'researcher': [np.nan]
    })
    
    # Call the function
    result = clean_authors_researcher(test_data)
    
    # Check that new columns were created correctly
    assert 'authors_all' in result.columns, "authors_all column not created"
    assert 'authors_set' in result.columns, "authors_set column not created"
    
    # Check the content of authors_all
    assert result['authors_all'].iloc[0] == 'John Smith; Jane Doe', "authors_all not combined correctly"
    
    # Check the content of authors_set
    expected_set = {'john smith', 'jane doe'}
    assert result['authors_set'].iloc[0] == expected_set, "authors_set not created correctly"
    
    print(" [Passed] - Test for function clean_authors_researcher()")

# ----- Clean acknowledgement evidence column -----
# Define function to clean acknowledgement evidence columns
def clean_acknowledgement_evidence(combined_data):
    try:
        # Update acknowledgments column based on fsrdc_acknowledgments_evidence
        # two columns existed in two separate data files
        combined_data.loc[combined_data["fsrdc_acknowledgments_evidence"].notna(), "acknowledgments"] = True
        print(" Completed cleaning acknowledgement evidence column.")
    except Exception as e:
        print(f"Error cleaning acknowledgement evidence column: {str(e)}")
        raise

    # Return clean data
    return combined_data

# Define test function for clean_acknowledgement_evidence()
def test_clean_acknowledgement_evidence():
    # Create a test dataframe
    test_data = pd.DataFrame({
        'acknowledgments': [None, False, True, None, 'Text Acknowledgment'],
        'fsrdc_acknowledgments_evidence': ['Evidence 1', None, 'Evidence 3', None, 'Evidence 5'],
        'other_column': ['A', 'B', 'C', 'D', 'E']  # Other column for completeness
    })
    
    # Call the function with the test data
    result = clean_acknowledgement_evidence(test_data)
    
    # Assert that the result is a dataframe
    assert isinstance(result, pd.DataFrame), "Result is not a DataFrame"
    
    # Assert that acknowledgments column is updated correctly
    # Row 0: fsrdc_acknowledgments_evidence exists, so acknowledgments should be True
    assert result['acknowledgments'].iloc[0] is True, "Acknowledgments not updated to True when evidence exists (Row 0)"
    
    # Row 1: fsrdc_acknowledgments_evidence is None, so acknowledgments should remain False
    assert result['acknowledgments'].iloc[1] is False, "Acknowledgments incorrectly updated when no evidence (Row 1)"
    
    # Row 2: Both columns have values, acknowledgments should still be True
    assert result['acknowledgments'].iloc[2] is True, "Existing True acknowledgments should remain True (Row 2)"
    
    # Row 3: Both columns are None, acknowledgments should remain None
    assert result['acknowledgments'].iloc[3] is None, "Acknowledgments incorrectly updated when both are None (Row 3)"
    
    # Row 4: fsrdc_acknowledgments_evidence exists, text acknowledgment should be replaced with True
    assert result['acknowledgments'].iloc[4] is True, "Text acknowledgments not updated to True when evidence exists (Row 4)"
    
    # Assert that fsrdc_acknowledgments_evidence column remains unchanged
    assert result['fsrdc_acknowledgments_evidence'].equals(test_data['fsrdc_acknowledgments_evidence']), "fsrdc_acknowledgments_evidence column was modified"
    
    # Assert that other columns remain unchanged
    assert result['other_column'].equals(test_data['other_column']), "Other columns were modified"
    
    print(" [Passed] - Test for function clean_acknowledgement_evidence()")

# ----- Clean dataset evidence column -----
# Define function to clean dataset evidence columns
def clean_dataset_evidence(combined_data):
    try:
        # Update dataset_mentions column based on other related column
        combined_data.loc[combined_data["dataset mentions"].notna(), "dataset_mentions"] = True
        combined_data.loc[combined_data["fsrdc_data_sources_evidence"].notna(), "dataset_mentions"] = True
        combined_data.loc[combined_data["matched_dataset_terms"].notna(), "dataset_mentions"] = True
        print(" Completed cleaning dataset evidence column.")
    except Exception as e:
        print(f"Error cleaning dataset evidence column: {str(e)}")
        raise

    # Return clean data
    return combined_data

# Define test function for clean_dataset_evidence()
def test_clean_dataset_evidence():
    # Create a test dataframe
    test_data = pd.DataFrame({
        'dataset_mentions': [None, False, True, None, None, 'Text mention'],
        'dataset mentions': ['Data 1', None, None, None, None, None],
        'fsrdc_data_sources_evidence': [None, 'Source 2', None, None, None, None],
        'matched_dataset_terms': [None, None, None, 'Term 4', None, None],
        'queried_dataset_terms': ['Query 1', 'Query 2', 'Query 3', 'Query 4', 'Query 5', 'Query 6'],
        'other_column': ['A', 'B', 'C', 'D', 'E', 'F']  # Other column for completeness
    })
    
    # Call the function with the test data
    result = clean_dataset_evidence(test_data)
    
    # Assert that the result is a dataframe
    assert isinstance(result, pd.DataFrame), "Result is not a DataFrame"
    
    # Assert that dataset_mentions column is updated correctly
    # Row 0: 'dataset mentions' exists, so dataset_mentions should be True
    assert result['dataset_mentions'].iloc[0] is True, "dataset_mentions not updated from dataset mentions evidence (Row 0)"
    
    # Row 1: 'fsrdc_data_sources_evidence' exists, so dataset_mentions should be True (even though it was False)
    assert result['dataset_mentions'].iloc[1] is True, "dataset_mentions not updated from fsrdc_data_sources_evidence (Row 1)"
    
    # Row 2: dataset_mentions is already True, should remain True
    assert result['dataset_mentions'].iloc[2] is True, "Existing True dataset_mentions should remain True (Row 2)"
    
    # Row 3: 'matched_dataset_terms' exists, so dataset_mentions should be True
    assert result['dataset_mentions'].iloc[3] is True, "dataset_mentions not updated from matched_dataset_terms (Row 3)"
    
    # Row 4: None of the evidence columns has values, dataset_mentions should remain None
    assert result['dataset_mentions'].iloc[4] is None, "dataset_mentions incorrectly updated when no evidence (Row 4)"
    
    # Assert that evidence columns remain unchanged
    assert result['dataset mentions'].equals(test_data['dataset mentions']), "dataset mentions column was modified"
    assert result['fsrdc_data_sources_evidence'].equals(test_data['fsrdc_data_sources_evidence']), "fsrdc_data_sources_evidence column was modified"
    assert result['matched_dataset_terms'].equals(test_data['matched_dataset_terms']), "matched_dataset_terms column was modified"
    assert result['queried_dataset_terms'].equals(test_data['queried_dataset_terms']), "queried_dataset_terms column was modified"
    
    # Assert that other columns remain unchanged
    assert result['other_column'].equals(test_data['other_column']), "Other columns were modified"
    
    print(" [Passed] - Test for function clean_dataset_evidence()")

# ----- Clean disclosure evidence column -----
# Define function to clean disclosure evidence columns
def clean_disclosure_evidence(combined_data):
    try:
        # Update disclosure_review column based on other related columns
        combined_data.loc[combined_data["fsrdc_disclosure_evidence"].notna(), "disclosure_review"] = True
        print(" Completed cleaning disclosure evidence column.")
    except Exception as e:
        print(f"Error cleaning disclosure evidence column: {str(e)}")
        raise

    # Return clean data
    return combined_data

# Define test function for clean_disclosure_evidence()
def test_clean_disclosure_evidence():
    # Create a test dataframe
    test_data = pd.DataFrame({
        'disclosure_review': [None, False, True],
        'fsrdc_disclosure_evidence': ['Evidence 1', None, 'Evidence 3']
    })
    
    # Call the function
    result = clean_disclosure_evidence(test_data)
    
    # Check that disclosure_review is updated when fsrdc_disclosure_evidence exists
    assert result['disclosure_review'].iloc[0] is True, "disclosure_review not updated when evidence exists"
    
    # Check that disclosure_review remains unchanged when fsrdc_disclosure_evidence is None
    assert result['disclosure_review'].iloc[1] is False, "disclosure_review incorrectly updated when no evidence"
    
    # Check that existing True value remains True
    assert result['disclosure_review'].iloc[2] is True, "Existing True value not preserved"
    
    print("[Passed] - Test for function clean_disclosure_evidence()")

# ----- Clean rdc evidence column -----
# Define function to clean rdc evidence columns
def clean_rdc_evidence(combined_data):
    try:
        # Update disclosure_review column based on other related columns
        combined_data.loc[combined_data["fsrdc_rdc_locations_evidence"].notna(), "rdc_mentions"] = True
        print(" Completed cleaning rdc column.")
    except Exception as e:
        print(f"Error cleaning RDC column: {str(e)}")
        raise

    # Return clean data
    return combined_data

# Define test function for clean_rdc_evidence()
def test_clean_rdc_evidence():
    # Create a test dataframe
    test_data = pd.DataFrame({
        'rdc_mentions': [None, False, True, None, 'Text mention'],
        'fsrdc_rdc_locations_evidence': ['Location 1', None, 'Location 3', None, 'Location 5'],
        'other_column': ['A', 'B', 'C', 'D', 'E']  # Other column for completeness
    })
    
    # Call the function with the test data
    result = clean_rdc_evidence(test_data)
    
    # Assert that the result is a dataframe
    assert isinstance(result, pd.DataFrame), "Result is not a DataFrame"
    
    # Assert that rdc_mentions column is updated correctly
    # Row 0: fsrdc_rdc_locations_evidence exists, so rdc_mentions should be True
    assert result['rdc_mentions'].iloc[0] is True, "rdc_mentions not updated to True when evidence exists (Row 0)"
    
    # Row 1: fsrdc_rdc_locations_evidence is None, so rdc_mentions should remain False
    assert result['rdc_mentions'].iloc[1] is False, "rdc_mentions incorrectly updated when no evidence (Row 1)"
    
    # Row 2: Both columns have values, rdc_mentions should still be True
    assert result['rdc_mentions'].iloc[2] is True, "Existing True rdc_mentions should remain True (Row 2)"
    
    # Row 3: Both columns are None, rdc_mentions should remain None
    assert result['rdc_mentions'].iloc[3] is None, "rdc_mentions incorrectly updated when both are None (Row 3)"
    
    # Row 4: fsrdc_rdc_locations_evidence exists, text rdc_mentions should be replaced with True
    assert result['rdc_mentions'].iloc[4] is True, "Text rdc_mentions not updated to True when evidence exists (Row 4)"
    
    # Assert that fsrdc_rdc_locations_evidence column remains unchanged
    assert result['fsrdc_rdc_locations_evidence'].equals(test_data['fsrdc_rdc_locations_evidence']), "fsrdc_rdc_locations_evidence column was modified"
    
    # Assert that other columns remain unchanged
    assert result['other_column'].equals(test_data['other_column']), "Other columns were modified"
    
    print(" [Passed] - Test for function clean_rdc_evidence()")

# All records have valid Project ID
# All records have valid RDC values, start and end year at the same time, and project PI
# ----- Clean records without Project ID -----

# # Define list of project columns
# proj_cols = ['ProjID', 'ProjectStatus', 'ProjectTitle', 'ProjectRDC',
#             'ProjectYearStarted', 'ProjectYearEnded', 'ProjectPI']

# Define funtion to clean records without Project ID
def clean_without_projid(combined_data, project):
    try:
        # Check Title column if there is any invalid Project Title
        # Set Project title for these records to be nan since they are not correct
        combined_data.loc[(combined_data["ProjID"].isna())
                        & (combined_data["ProjectTitle"].notna())
                        & (~combined_data["ProjectTitle"]
                            .str.strip().str.lower()
                            .isin(project["Title"].str.strip().str.lower().unique())),
                        "ProjectTitle"] = np.nan
        print(" Completed cleaning records without Project ID.")
    except Exception as e:
        print(f"Error cleaning records without Project ID: {str(e)}")
        raise

    # Return clean data
    return combined_data

# Define test function for clean_without_projid()
def test_clean_without_projid():
    # Create a test dataframe
    test_combined_data = pd.DataFrame({
        'ProjID': [None, 'P001', None, None, 'P002', None],
        'ProjectTitle': [
            'Valid Project',      # No ProjID, but valid title (in project df)
            'Project One',        # Has ProjID, so title should remain unchanged
            'Invalid Project',    # No ProjID, invalid title (not in project df)
            None,                 # No ProjID, no title
            'Another Project',    # Has ProjID, so title should remain unchanged
            'Another Invalid'     # No ProjID, invalid title (not in project df)
        ],
        'other_column': ['A', 'B', 'C', 'D', 'E', 'F']  # Other column for completeness
    })
    
    # Create a test dataframe for project
    test_project = pd.DataFrame({
        'Proj ID': ['P001', 'P002', 'P003'],
        'Title': ['Project One', 'Another Project', 'Valid Project'],
        'Status': ['Active', 'Active', 'Completed'],
        'RDC': ['RDC1', 'RDC2', 'RDC3'],
        'Start Year': [2020, 2021, 2019],
        'End Year': [2023, 2024, 2022],
        'PI': ['John Doe', 'Jane Smith', 'Bob Johnson']
    })
    
    # Call the function with the test data
    result = clean_without_projid(test_combined_data, test_project)
    
    # Assert that the result is a dataframe
    assert isinstance(result, pd.DataFrame), "Result is not a DataFrame"
    
    # Assert that ProjectTitle is cleaned correctly
    # Row 0: No ProjID but title is in project df, should remain unchanged
    assert result['ProjectTitle'].iloc[0] == 'Valid Project', "Valid project title without ProjID was incorrectly modified"
    
    # Row 1: Has ProjID, should remain unchanged
    assert result['ProjectTitle'].iloc[1] == 'Project One', "Project title with ProjID was incorrectly modified"
    
    # Row 2: No ProjID and title not in project df, should be set to NaN
    assert pd.isna(result['ProjectTitle'].iloc[2]), "Invalid project title without ProjID was not set to NaN"
    
    # Row 3: No ProjID and no title, should remain NaN
    assert pd.isna(result['ProjectTitle'].iloc[3]), "NaN project title was incorrectly modified"
    
    # Row 4: Has ProjID, should remain unchanged
    assert result['ProjectTitle'].iloc[4] == 'Another Project', "Project title with ProjID was incorrectly modified"
    
    # Row 5: No ProjID and title not in project df, should be set to NaN
    assert pd.isna(result['ProjectTitle'].iloc[5]), "Invalid project title without ProjID was not set to NaN"
    
    # Assert that ProjID column remains unchanged
    assert result['ProjID'].equals(test_combined_data['ProjID']), "ProjID column was modified"
    
    # Assert that other columns remain unchanged
    assert result['other_column'].equals(test_combined_data['other_column']), "Other columns were modified"
    
    print(" [Passed] - Test for function clean_without_projid()")

# ----- Clean records with Project ID -----
# Define funtion to clean records with Project ID
def clean_with_projid(combined_data, project):
    try:
        # Merge project and combined_data based on project id
        corrected_proj_data = pd.merge(combined_data, project, how="left",
                                    left_on="ProjID", right_on="Proj ID")
        # Replace project information for records with project ID
        proj_col_mapping = {
            'Status': 'ProjectStatus',
            'Title': 'ProjectTitle',
            'RDC': 'ProjectRDC',
            'Start Year': 'ProjectYearStarted',
            'End Year': 'ProjectYearEnded',
            'PI': 'ProjectPI'
        }

        # Replace the corresonding column values
        for col1, col2 in proj_col_mapping.items():
            mask = corrected_proj_data["ProjID"].notnull()
            corrected_proj_data.loc[mask, col2] = corrected_proj_data.loc[mask, col1]

        # Drop other columns
        corrected_proj_data = corrected_proj_data.drop(
            columns=['Proj ID', 'Status', 'Title', 'RDC',
                    'Start Year', 'End Year', 'PI'])

        # Define the new column order
        cols_order = [
            'ProjID', 'ProjectStatus', 'ProjectTitle', 'ProjectRDC',
            'ProjectYearStarted', 'ProjectYearEnded', 'ProjectPI',
            'OutputTitle', 'OutputType', 'OutputStatus', 'OutputYear',
            'OutputVolume', 'OutputNumber', 'OutputPages',
            'group', 'idx', 'doi', 'arxiv_url', 'authors_set',
            'acknowledgments', 'fsrdc_acknowledgments_evidence',
            'data_descriptions',
            'dataset_mentions', 'dataset mentions', 'fsrdc_data_sources_evidence',
            'matched_dataset_terms', 'queried_dataset_terms',
            'disclosure_review', 'fsrdc_disclosure_evidence',
            'rdc_mentions', 'fsrdc_rdc_locations_evidence',
            'agency', 'abstract',
            'affiliations', 'raw_affiliation_strings', 'detailed_affiliations',
            'host_organization_name', 'institution_display_names', 'openalex_id',
            'orcid_id', 'source_display_name', 'authors', 'researcher', 'authors_all']

        # Rearrage column order
        corrected_proj_data = corrected_proj_data.reindex(columns=cols_order)

        # Drop records without output title
        corrected_proj_data = corrected_proj_data.dropna(subset=["OutputTitle"])
        print(" Completed cleaning records with Project ID.")
    except Exception as e:
        print(f"Error cleaning records with Project ID: {str(e)}")
        raise

    # Return data with correct Project information populated
    return corrected_proj_data

# Define test function for clean_with_projid()
def test_clean_with_projid():
    # Create a test dataframe
    test_combined_data = pd.DataFrame({
        'ProjID': ['P001', None, 'P002', 'P003', 'P004'],
        'ProjectStatus': ['Old Status 1', 'No ProjID Status', 'Old Status 2', 'Old Status 3', 'Old Status 4'],
        'ProjectTitle': ['Old Title 1', 'No ProjID Title', 'Old Title 2', 'Old Title 3', 'Old Title 4'],
        'ProjectRDC': ['Old RDC 1', 'No ProjID RDC', 'Old RDC 2', 'Old RDC 3', 'Old RDC 4'],
        'ProjectYearStarted': [2010, 2011, 2012, 2013, 2014],
        'ProjectYearEnded': [2020, 2021, 2022, 2023, 2024],
        'ProjectPI': ['Old PI 1', 'No ProjID PI', 'Old PI 2', 'Old PI 3', 'Old PI 4'],
        'OutputTitle': ['Output 1', 'Output 2', 'Output 3', None, 'Output 5'],
        'group': [1, 2, 3, 4, 5],
        'idx': [1, 2, 3, 4, 5],
        'doi': ['doi1', 'doi2', 'doi3', 'doi4', 'doi5'],
        'arxiv_url': ['url1', 'url2', 'url3', 'url4', 'url5'],
        'acknowledgments': [True, False, True, False, True],
        'fsrdc_acknowledgments_evidence': ['Evidence 1', None, 'Evidence 3', None, 'Evidence 5'],
        'dataset_mentions': [True, False, True, False, True],
        'dataset mentions': ['Data 1', None, 'Data 3', None, 'Data 5'],
        'fsrdc_data_sources_evidence': ['Source 1', None, 'Source 3', None, 'Source 5'],
        'matched_dataset_terms': ['Terms 1', None, 'Terms 3', None, 'Terms 5'],
        'queried_dataset_terms': ['Query 1', 'Query 2', 'Query 3', 'Query 4', 'Query 5'],
        'disclosure_review': [True, False, True, False, True],
        'fsrdc_disclosure_evidence': ['Evidence 1', None, 'Evidence 3', None, 'Evidence 5'],
        'rdc_mentions': [True, False, True, False, True],
        'fsrdc_rdc_locations_evidence': ['Location 1', None, 'Location 3', None, 'Location 5'],
        'agency': ['Agency 1', 'Agency 2', 'Agency 3', 'Agency 4', 'Agency 5'],
        'abstract': ['Abstract 1', 'Abstract 2', 'Abstract 3', 'Abstract 4', 'Abstract 5'],
        'authors': ['Author 1', 'Author 2', 'Author 3', 'Author 4', 'Author 5'],
        'researcher': ['Researcher 1', 'Researcher 2', 'Researcher 3', 'Researcher 4', 'Researcher 5'],
        'authors_all': ['All 1', 'All 2', 'All 3', 'All 4', 'All 5'],
        'authors_set': [{'author 1'}, {'author 2'}, {'author 3'}, {'author 4'}, {'author 5'}]
    })
    
    # Create additional columns for combined_data to match the full column list in your function
    for col in ['data_descriptions', 'affiliations', 'raw_affiliation_strings', 
                'detailed_affiliations', 'host_organization_name', 'institution_display_names', 
                'openalex_id', 'orcid_id', 'source_display_name', 'OutputType', 'OutputStatus', 
                'OutputYear', 'OutputVolume', 'OutputNumber', 'OutputPages']:
        test_combined_data[col] = [f"{col}_{i}" for i in range(1, 6)]
    
    # Create a test dataframe for project
    test_project = pd.DataFrame({
        'Proj ID': ['P001', 'P002', 'P003', 'P004'],
        'Status': ['Active', 'Completed', 'Active', 'Pending'],
        'Title': ['Correct Title 1', 'Correct Title 2', 'Correct Title 3', 'Correct Title 4'],
        'RDC': ['Correct RDC 1', 'Correct RDC 2', 'Correct RDC 3', 'Correct RDC 4'],
        'Start Year': [2015, 2016, 2017, 2018],
        'End Year': [2025, 2026, 2027, 2028],
        'PI': ['Correct PI 1', 'Correct PI 2', 'Correct PI 3', 'Correct PI 4']
    })
    
    # Call the function with the test data
    result = clean_with_projid(test_combined_data, test_project)
    
    # Assert that the result is a dataframe
    assert isinstance(result, pd.DataFrame), "Result is not a DataFrame"
    
    # Assert that records without OutputTitle are dropped
    assert len(result) == 4, "Records without OutputTitle were not dropped"
    assert 'Output 4' not in result['OutputTitle'].values, "Record with None OutputTitle was not dropped"
    
    # Assert that project information is updated for records with ProjID
    # Row with ProjID 'P001'
    p001_row = result[result['ProjID'] == 'P001'].iloc[0]
    assert p001_row['ProjectStatus'] == 'Active', "ProjectStatus not updated for P001"
    assert p001_row['ProjectTitle'] == 'Correct Title 1', "ProjectTitle not updated for P001"
    assert p001_row['ProjectRDC'] == 'Correct RDC 1', "ProjectRDC not updated for P001"
    assert p001_row['ProjectYearStarted'] == 2015, "ProjectYearStarted not updated for P001"
    assert p001_row['ProjectYearEnded'] == 2025, "ProjectYearEnded not updated for P001"
    assert p001_row['ProjectPI'] == 'Correct PI 1', "ProjectPI not updated for P001"
    
    # Row with ProjID 'P002'
    p002_row = result[result['ProjID'] == 'P002'].iloc[0]
    assert p002_row['ProjectStatus'] == 'Completed', "ProjectStatus not updated for P002"
    assert p002_row['ProjectTitle'] == 'Correct Title 2', "ProjectTitle not updated for P002"
    assert p002_row['ProjectRDC'] == 'Correct RDC 2', "ProjectRDC not updated for P002"
    assert p002_row['ProjectYearStarted'] == 2016, "ProjectYearStarted not updated for P002"
    assert p002_row['ProjectYearEnded'] == 2026, "ProjectYearEnded not updated for P002"
    assert p002_row['ProjectPI'] == 'Correct PI 2', "ProjectPI not updated for P002"
    
    # Assert that original columns from project dataframe are dropped
    project_columns = ['Proj ID', 'Status', 'Title', 'RDC', 'Start Year', 'End Year', 'PI']
    for col in project_columns:
        assert col not in result.columns, f"Project column '{col}' was not dropped"
    
    # Assert that columns are in the correct order
    expected_first_columns = [
        'ProjID', 'ProjectStatus', 'ProjectTitle', 'ProjectRDC',
        'ProjectYearStarted', 'ProjectYearEnded', 'ProjectPI',
        'OutputTitle'
    ]
    for i, col in enumerate(expected_first_columns):
        assert result.columns[i] == col, f"Column order incorrect: {col} should be at position {i}"
    
    # Assert that rows without ProjID remain unchanged (except for dropped columns from project df)
    no_projid_row = result[result['ProjID'].isna()].iloc[0]
    assert no_projid_row['ProjectStatus'] == 'No ProjID Status', "ProjectStatus incorrectly modified for row without ProjID"
    assert no_projid_row['ProjectTitle'] == 'No ProjID Title', "ProjectTitle incorrectly modified for row without ProjID"
    assert no_projid_row['ProjectRDC'] == 'No ProjID RDC', "ProjectRDC incorrectly modified for row without ProjID"
    assert no_projid_row['ProjectYearStarted'] == 2011, "ProjectYearStarted incorrectly modified for row without ProjID"
    assert no_projid_row['ProjectYearEnded'] == 2021, "ProjectYearEnded incorrectly modified for row without ProjID"
    assert no_projid_row['ProjectPI'] == 'No ProjID PI', "ProjectPI incorrectly modified for row without ProjID"
    
    print(" [Passed] - Test for function clean_with_projid()")

# ---------- Deduplication ----------
# Define function to deduplicate data
def deduplicate_data(corrected_proj_data):
    print("Deduplicating records...")
    try:
        # Drop records without output title
        corrected_proj_data = corrected_proj_data.dropna(subset=["OutputTitle"])
    except Exception as e:
        print(f"Error dropping records without output title: {str(e)}")
        raise

    # Step 1: Include all records with unique doi, 
    # and all records without doi (with unique output title) in group 2 output
    try:
        # Get all records of group 2 outputs
        group2_results = corrected_proj_data[corrected_proj_data["group"] == 2]

        # Get all deduplicated records with doi based on doi column
        group2_deduplicated_doi_data = (group2_results[
            group2_results["doi"].notnull()].drop_duplicates(subset="doi"))

        # Get all deduplicated records without doi based on OutputTitle column
        group2_deduplicated_no_doi_data = (group2_results[
            group2_results["doi"].isnull()].drop_duplicates(subset="OutputTitle"))

        # Concatenate the data above as deduplicated data
        deduplicated_data = pd.concat([group2_deduplicated_doi_data,
                                    group2_deduplicated_no_doi_data],
                                    ignore_index=True)
        print(" Completed deduplicating group 2 records.")
    except Exception as e:
        print(f"Error processing group 2 records: {str(e)}")
        raise

    # Step 2: Include all records with unique doi in group 1 output
    # (records not in group 2 output)
    try:
        # Get only records with doi in group 1 outputs
        group1_doi_results = corrected_proj_data[(corrected_proj_data["group"] == 1)
                                                & (corrected_proj_data["doi"].notnull())]
        # Deduplicate based on doi columns
        group1_deduplicated_doi_results = (group1_doi_results
                                        .drop_duplicates(subset="doi"))

        # Get all unique records with doi not in deduplicated data
        group1_deduplicated_doi_data = group1_deduplicated_doi_results[
            ~group1_deduplicated_doi_results["doi"].isin(deduplicated_data["doi"])]

        # Concatenate the data above to the deduplicated data
        deduplicated_data = pd.concat([deduplicated_data,
                                    group1_deduplicated_doi_data],
                                    ignore_index=True)
        print(" Completed deduplicating group 1 records.")
    except Exception as e:
        print(f"Error processing group 1 records: {str(e)}")
        raise

    # Step 3: Include all records with unique doi in group 6 output
    # (records not in group 1, 2 outputs)
    try:
        # Get only records with doi in group 6 outputs
        group6_doi_results = corrected_proj_data[(corrected_proj_data["group"] == 6)
                                                & (corrected_proj_data["doi"].notnull())]
        # Deduplicate based on doi columns
        group6_deduplicated_doi_results = (group6_doi_results
                                        .drop_duplicates(subset="doi"))

        # Get all unique records with doi not in deduplicated data
        group6_deduplicated_doi_data = group6_deduplicated_doi_results[
            ~group6_deduplicated_doi_results["doi"].isin(deduplicated_data["doi"])]

        # Concatenate the data above to the deduplicated data
        deduplicated_data = pd.concat([deduplicated_data,
                                    group6_deduplicated_doi_data],
                                    ignore_index=True)
        print(" Completed deduplicating group 6 records.")
    except Exception as e:
        print(f"Error processing group 6 records: {str(e)}")
        raise

    # Step 4: Include all records with unique doi in all other group outputs
    # (records not in group 1, 2, 6 outputs)
    try:
        # Get only records with doi in the rest of outputs
        other_doi_results = corrected_proj_data[(corrected_proj_data["group"] != 1)
                                                & (corrected_proj_data["group"] != 2)
                                                & (corrected_proj_data["group"] != 6)
                                                & (corrected_proj_data["doi"].notnull())]
        # Deduplicate based on doi columns
        other_deduplicated_doi_results = (other_doi_results
                                        .drop_duplicates(subset="doi"))

        # Get all unique records with doi not in deduplicated data
        other_deduplicated_doi_data = other_deduplicated_doi_results[
            ~other_deduplicated_doi_results["doi"].isin(deduplicated_data["doi"])]

        # Concatenate the data above to the deduplicated data
        deduplicated_data = pd.concat([deduplicated_data,
                                    other_deduplicated_doi_data],
                                    ignore_index=True)
        print(" Completed deduplicating other group records.")
    except Exception as e:
        print(f"Error processing other group records: {str(e)}")
        raise
    print("Completed deduplicating records.\n")

    # Return deduplicated data
    return deduplicated_data

# Define test function for deduplicate_data()
def test_deduplicate_data():
    # Create a test dataframe
    test_data = pd.DataFrame({
        'group': [2, 2, 2, 2, 1, 1, 1, 6, 6, 3, 4, 5],
        'doi': [
            'doi1', 'doi2', None, None,           # Group 2: 2 with DOI, 2 without
            'doi3', 'doi1', 'doi5',               # Group 1: 3 with DOI (1 duplicate with group 2)
            'doi6', 'doi2',                        # Group 6: 2 with DOI (1 duplicate with group 2)
            'doi7', 'doi8', 'doi1'                 # Other groups: 3 with DOI (1 duplicate)
        ],
        'OutputTitle': [
            'Title 1', 'Title 2', 'Title 3', 'Title 3',  # Group 2: duplicate title for no-DOI records
            'Title 4', 'Title 5', 'Title 6',
            'Title 7', 'Title 8',
            'Title 9', 'Title 10', 'Title 11'
        ],
        'ProjID': ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12'],
        # Add other required columns with dummy values
        'ProjectStatus': ['Status'] * 12,
        'ProjectTitle': ['Project'] * 12,
        'ProjectRDC': ['RDC'] * 12,
        'ProjectYearStarted': [2020] * 12,
        'ProjectYearEnded': [2022] * 12,
        'ProjectPI': ['PI'] * 12,
        'idx': list(range(1, 13))
    })
    
    # Add other columns needed by the function
    for col in ['authors_set', 'acknowledgments', 'fsrdc_acknowledgments_evidence',
                'data_descriptions', 'dataset_mentions', 'dataset mentions',
                'fsrdc_data_sources_evidence', 'matched_dataset_terms',
                'queried_dataset_terms', 'disclosure_review', 'fsrdc_disclosure_evidence',
                'rdc_mentions', 'fsrdc_rdc_locations_evidence', 'agency', 'abstract',
                'affiliations', 'raw_affiliation_strings', 'detailed_affiliations',
                'host_organization_name', 'institution_display_names', 'openalex_id',
                'orcid_id', 'source_display_name', 'authors', 'researcher', 'authors_all',
                'arxiv_url', 'OutputType', 'OutputStatus', 'OutputYear', 'OutputVolume',
                'OutputNumber', 'OutputPages']:
        test_data[col] = [f"{col}_{i}" for i in range(1, 13)]
    
    # Call the function with the test data
    result = deduplicate_data(test_data)
    
    # Assert that the result is a dataframe
    assert isinstance(result, pd.DataFrame), "Result is not a DataFrame"
    
    # Assert correct number of deduplicated records
    # Expected records: 
    # - Group 2: 2 with DOI + 1 without DOI (deduplicated) = 3
    # - Group 1: 2 with DOI (excluding doi1 which is already in group 2) = 2
    # - Group 6: 1 with DOI (excluding doi2 which is already in group 2) = 1
    # - Other groups: 2 with DOI (excluding doi1 which is already included) = 2
    # Total: 8 records
    assert len(result) == 8, f"Expected 8 deduplicated records, got {len(result)}"
    
    # Group 2 deduplication checks
    # Check Group 2 DOI records are included
    group2_doi_records = result[(result['group'] == 2) & (result['doi'].notna())]
    assert len(group2_doi_records) == 2, "Group 2 records with DOI not correctly deduplicated"
    
    # Check Group 2 no-DOI records are deduplicated by title
    group2_no_doi_records = result[(result['group'] == 2) & (result['doi'].isna())]
    assert len(group2_no_doi_records) == 1, "Group 2 records without DOI not correctly deduplicated"
    
    # Group 1 deduplication checks
    # Check Group 1 records (should exclude doi1 as it's in Group 2)
    group1_records = result[result['group'] == 1]
    assert len(group1_records) == 2, "Group 1 records not correctly deduplicated"
    assert 'doi1' not in group1_records['doi'].values, "Duplicate DOI from Group 1 not excluded"
    
    # Group 6 deduplication checks
    # Check Group 6 records (should exclude doi2 as it's in Group 2)
    group6_records = result[result['group'] == 6]
    assert len(group6_records) == 1, "Group 6 records not correctly deduplicated"
    assert 'doi2' not in group6_records['doi'].values, "Duplicate DOI from Group 6 not excluded"
    
    # Other groups deduplication checks
    # Check other group records (should exclude doi1 as it's already included)
    other_records = result[(result['group'] != 1) & (result['group'] != 2) & (result['group'] != 6)]
    assert len(other_records) == 2, "Other group records not correctly deduplicated"
    assert 'doi1' not in other_records['doi'].values, "Duplicate DOI from other groups not excluded"
    
    # Check all DOIs in the result are unique
    assert len(result['doi'].dropna().unique()) == len(result['doi'].dropna()), "Result contains duplicate DOIs"
    
    print(" [Passed] - Test for function deduplicate_data()")

# ---------- Matching Project Information ----------
# ----- Match based on PI -----
# Define function to match based on PI
def match_on_pi(deduplicated_data, project):
    print(" Matching project information based on PI...")
    # Save a copy of depulicated data
    pre_match_data = deduplicated_data.copy()
    # If certain PI only has one project, then the output belongs to that project
    try:
        # Get PI project count
        pi_project_count = project.groupby("PI")["Proj ID"].count().reset_index()
        pi_project_count.columns = ["PI", "ProjCount"]
        pi_one_proj_set = set(pi_project_count.loc[pi_project_count["ProjCount"] == 1, "PI"])
    except Exception as e:
        print(f"Error calculating PI project counts: {str(e)}")
        raise

    try:
        # Define mask used for matching pi
        pi_mask = (
            (pre_match_data["ProjID"].isnull())
            & (pre_match_data["ProjectPI"].isin(pi_one_proj_set)))
    except Exception as e:
        print(f"Error creating PI matching mask: {str(e)}")
        raise

    # Match project information for records with PI that has only one project
    try:
        # Merge pre_match_data and project
        pi_proj_data = pd.merge(
            pre_match_data.loc[pi_mask, ["group", "idx", "ProjectPI"]],
            project, how="inner", left_on= "ProjectPI", right_on="PI")

        # Define new mapping
        pi_col_mapping = {
            'Proj ID': 'ProjID',
            'Status': 'ProjectStatus',
            'Title': 'ProjectTitle',
            'RDC': 'ProjectRDC',
            'Start Year': 'ProjectYearStarted',
            'End Year': 'ProjectYearEnded'
        }

        # Merge two dfs based on group and idx
        pi_proj_data = pd.merge(
            pre_match_data, pi_proj_data[["group", "idx"] + list(project.columns)],
            how="left", on=["group", "idx"])

        # Redefine mask
        pi_mask = (
            (pi_proj_data["ProjID"].isnull())
            & (pi_proj_data["ProjectPI"].isin(pi_one_proj_set)))

        # Populate project information for records with PI that only have one project
        for col1, col2 in pi_col_mapping.items():
            pi_proj_data.loc[pi_mask, col2] = pi_proj_data.loc[pi_mask, col1]

        # Drop unneccessary columns
        pi_proj_data = pi_proj_data.drop(columns=list(project.columns))
    except Exception as e:
        print(f"Failed to match project information based on PI: {str(e)}")
        raise

    print(" Completed matching project information based on PI.")

    # Return records after matching
    return pi_proj_data

# Define test function for match_on_pi()
def test_match_on_pi():
    # Create a simpler test dataframe
    test_deduplicated_data = pd.DataFrame({
        'group': [1, 2, 3],
        'idx': [1, 2, 3],
        'ProjID': [None, None, 'P003'],  # First two have no ProjID
        'ProjectPI': ['Single Project PI', 'Multiple Projects PI', 'Already Has ProjID'],
        'ProjectTitle': ['Title 1', 'Title 2', 'Title 3']
    })
    
    # Add minimal required columns
    for col in ['ProjectStatus', 'ProjectRDC', 'ProjectYearStarted', 'ProjectYearEnded', 'OutputTitle']:
        test_deduplicated_data[col] = [f"{col}_{i}" for i in range(1, 4)]
    
    # Create a simple test dataframe for project
    test_project = pd.DataFrame({
        'Proj ID': ['P001', 'P002', 'P003', 'P004'],
        'Status': ['Active', 'Active', 'Completed', 'Pending'],
        'Title': ['Project 1', 'Project 2', 'Project 3', 'Project 4'],
        'RDC': ['RDC A', 'RDC B', 'RDC C', 'RDC D'],
        'Start Year': [2010, 2011, 2012, 2013],
        'End Year': [2020, 2021, 2022, 2023],
        'PI': ['Single Project PI', 'Multiple Projects PI', 'Already Has ProjID', 'Multiple Projects PI']
    })
    
    # Call the function with the test data
    result = match_on_pi(test_deduplicated_data, test_project)
    
    # Test only the core functionality: PI with single project gets matched
    single_pi_row = result[result['ProjectPI'] == 'Single Project PI'].iloc[0]
    assert single_pi_row['ProjID'] == 'P001', "ProjID not matched for PI with single project"
    
    # For comparison, PI with multiple projects should not be matched
    multi_pi_row = result[result['ProjectPI'] == 'Multiple Projects PI'].iloc[0]
    assert pd.isna(multi_pi_row['ProjID']), "ProjID incorrectly matched for PI with multiple projects"
    
    print(" [Passed] - Test for function match_on_pi()")

# ----- Match based on PI and RDC -----
# If certain PI only has one project in certain RDC, then the output belongs to that project
# Define function to match based on PI and RDC
def match_on_pi_rdc(pi_proj_data, project):
    try:
        print(" Matching project information based on PI and RDC...")
        # Get PI RDC project count
        pi_rdc_project_count = project.groupby(["PI", "RDC"])["Proj ID"].count().reset_index()
        pi_rdc_project_count.columns = ["PI", "RDC", "ProjCount"]
        pi_rdc_one_proj_set = set(
            zip(
                pi_rdc_project_count.loc[pi_rdc_project_count["ProjCount"] == 1, "PI"],
                pi_rdc_project_count.loc[pi_rdc_project_count["ProjCount"] == 1, "RDC"]
            )
        )
    except Exception as e:
        print(f"Error calculating PI RDC project counts: {str(e)}")
        raise

    try:
        # Create tuples of PI and RDC from pre_match_data
        pi_proj_data["PI_RDC_Tuple"] = list(
            zip(pi_proj_data["ProjectPI"].fillna(""),
                pi_proj_data["ProjectRDC"].fillna("")))

        # Define mask used for matching PI and RDC
        pi_rdc_mask = (
            (pi_proj_data["ProjID"].isnull())
            & (pi_proj_data["PI_RDC_Tuple"].isin(pi_rdc_one_proj_set))
        )
    except Exception as e:
        print(f"Error creating PI RDC matching mask: {str(e)}")
        raise

    # Match project information for records with PI and RDC that have only one project
    try:
        # Merge pre_match_data and project
        pi_rdc_proj_data = pd.merge(
            pi_proj_data.loc[pi_rdc_mask, ["group", "idx", "ProjectPI", "ProjectRDC"]],
            project, how="inner", left_on=["ProjectPI", "ProjectRDC"],
            right_on=["PI", "RDC"])

        # Define new mapping
        pi_rdc_col_mapping = {
            'Proj ID': 'ProjID',
            'Status': 'ProjectStatus',
            'Title': 'ProjectTitle',
            'RDC': 'ProjectRDC',
            'Start Year': 'ProjectYearStarted',
            'End Year': 'ProjectYearEnded'
        }

        # Merge two dfs based on group and idx
        pi_rdc_proj_data = pd.merge(
            pi_proj_data,
            pi_rdc_proj_data[["group", "idx"] + list(project.columns)],
            how="left",
            on=["group", "idx"]
        )

        # Redefine mask with the merged data
        pi_rdc_mask = (
            (pi_rdc_proj_data["ProjID"].isnull())
            & (pi_rdc_proj_data["PI_RDC_Tuple"].isin(pi_rdc_one_proj_set))
        )

        # Populate project information for records with PI and RDC that only have one project
        for col1, col2 in pi_rdc_col_mapping.items():
            pi_rdc_proj_data.loc[pi_rdc_mask, col2] = pi_rdc_proj_data.loc[pi_rdc_mask, col1]

        # Drop unneccessary columns
        pi_rdc_proj_data = pi_rdc_proj_data.drop(columns=list(project.columns))
    except Exception as e:
        print(f"Failed to match project information based on PI and RDC: {str(e)}")
        raise

    print(" Completed matching project information based on PI and RDC.\n")

    # Return records after matching
    return pi_rdc_proj_data

# Define test function for match_on_pi_rdc()
def test_match_on_pi_rdc():
    # Create a simple test dataframe
    test_pi_proj_data = pd.DataFrame({
        'group': [1, 2, 3, 4],
        'idx': [1, 2, 3, 4],
        'ProjID': [None, None, 'P003', None],  # First two have no ProjID
        'ProjectPI': ['PI-A', 'PI-B', 'PI-C', 'PI-A'],
        'ProjectRDC': ['RDC-X', 'RDC-Y', 'RDC-Z', 'RDC-Y'],
        'ProjectTitle': ['Title 1', 'Title 2', 'Title 3', 'Title 4']
    })
    
    # Add minimal required columns
    for col in ['ProjectStatus', 'ProjectYearStarted', 'ProjectYearEnded', 'OutputTitle']:
        test_pi_proj_data[col] = [f"{col}_{i}" for i in range(1, 5)]
    
    # Create a simple test dataframe for project
    test_project = pd.DataFrame({
        'Proj ID': ['P001', 'P002', 'P003', 'P004', 'P005'],
        'Status': ['Active', 'Active', 'Completed', 'Pending', 'Active'],
        'Title': ['Project 1', 'Project 2', 'Project 3', 'Project 4', 'Project 5'],
        'RDC': ['RDC-X', 'RDC-Y', 'RDC-Z', 'RDC-Y', 'RDC-X'],
        'Start Year': [2010, 2011, 2012, 2013, 2014],
        'End Year': [2020, 2021, 2022, 2023, 2024],
        'PI': ['PI-A', 'PI-B', 'PI-C', 'PI-B', 'PI-D']
    })
    
    # Call the function with the test data
    result = match_on_pi_rdc(test_pi_proj_data, test_project)
    
    # Row 0: (PI-A, RDC-X) should be matched to P001
    assert result.loc[0, 'ProjID'] == 'P001', "PI-A + RDC-X not matched to P001"
    
    # Row 1: (PI-B, RDC-Y) should not be matched as this combination has multiple projects
    assert pd.isna(result.loc[1, 'ProjID']), "PI-B + RDC-Y incorrectly matched despite having multiple projects"
    
    # Row 2: Already has ProjID, should not be changed
    assert result.loc[2, 'ProjID'] == 'P003', "Existing ProjID was modified"
    
    # Row 3: (PI-A, RDC-Y) should not be matched as this combination has no projects
    assert pd.isna(result.loc[3, 'ProjID']), "PI-A + RDC-Y incorrectly matched despite not being in project data"
    
    # Verify project columns are dropped
    project_columns = ['Proj ID', 'Status', 'Title', 'RDC', 'Start Year', 'End Year', 'PI']
    for col in project_columns:
        assert col not in result.columns, f"Project column '{col}' was not dropped"
    
    print(" [Passed] - Test for function match_on_pi_rdc()")

# ----- Fuzzy matching -----
# Define function to do fuzzy matching
def update_projects_with_fuzzy_match(df, project, match_threshold=80,
                                    use_rdc=True, use_year=True, use_pi=True,
                                    use_authors=False,
                                    relax_author_threshold=False,
                                    relax_threshold=False):
    # Create a copy of df to avoid modifying the original
    updated_df = df.copy()

    # Get the mask for records where ProjID is null
    null_projid_mask = updated_df['ProjID'].isnull()

    # Define the mapping between project and df columns
    column_mapping = {
        'Proj ID': 'ProjID',
        'Status': 'ProjectStatus',
        'Title': 'ProjectTitle',
        'RDC': 'ProjectRDC',
        'Start Year': 'ProjectYearStarted',
        'End Year': 'ProjectYearEnded',
        'PI': 'ProjectPI'
    }

    progress_counter = 0
    # Process each row with null ProjID
    for idx in updated_df[null_projid_mask].index:
        # Track progress
        progress_counter += 1
        if progress_counter % 1000 == 0:
            print(f"   Processed {progress_counter} rows")

        # Get the current row data
        row = updated_df.loc[idx]

        # Skip if we don't have OutputTitle for fuzzy matching
        if pd.isna(row['OutputTitle']):
            continue

        # Filter project based on ProjectRDC, ProjectPI if they're not null
        filtered_project = project.copy()

        if use_rdc and pd.notna(row['ProjectRDC']):
            filtered_project = filtered_project[
                filtered_project['RDC'] == row['ProjectRDC']]

        if (use_year and pd.notna(row['ProjectYearStarted'])
            and pd.notna(row['ProjectYearEnded'])):
            filtered_project = filtered_project[
                (filtered_project['Start Year'].astype(int) == int(row['ProjectYearStarted']))
                & (filtered_project['End Year'].dropna().astype(int) == int(row['ProjectYearEnded']))]

        if use_pi and pd.notna(row['ProjectPI']):
            filtered_project = filtered_project[
                filtered_project['PI'] == row['ProjectPI']]

        if use_authors:
            tmp_df = filtered_project[
                filtered_project['PI'].str.lower().str.strip().isin(row['authors_set'])]
            if len(tmp_df) != 0:
                filtered_project = tmp_df
            else:
                # Fuzzy matching between authors_set and PI values
                best_pi_index = None
                best_pi_score = 0

                # Calculate fuzzy match scores for each project in filtered_project
                for proj_idx, proj_row in filtered_project.iterrows():
                    pi_value = str(proj_row['PI']).lower().strip()

                    # Get the best match score from any author in authors_set
                    best_author_score = 0
                    for author in row['authors_set']:
                        if pd.notna(author) and pd.notna(pi_value):
                            # Calculate fuzzy match score
                            score = fuzz.token_sort_ratio(author.lower().strip(), pi_value)
                            best_author_score = max(best_author_score, score)

                    # Store the project index and its best score
                    if best_author_score > best_pi_score:
                        best_pi_index = proj_idx
                        best_pi_score = best_author_score

                if relax_author_threshold | (best_pi_score > match_threshold):
                    filtered_project = filtered_project.loc[[best_pi_index], :]

        # If we've filtered down to 0 records, skip this row
        if len(filtered_project) == 0:
            continue

        # If we've filtered down to 1 record, use it directly
        if len(filtered_project) == 1:
            best_match_idx = filtered_project.index[0]
            best_match_score = 100000  # Perfect match since it's the only option
        else:
            # Calculate fuzzy match scores between OutputTitle and Title
            best_match_idx = None
            best_match_score = 0
            for project_idx, project_row in filtered_project.iterrows():
                score = fuzz.token_sort_ratio(row['OutputTitle'].lower().strip(), project_row['Title'].lower().strip())
                if score > best_match_score:
                    best_match_idx = project_idx
                    best_match_score = score

        # Only update if the match score exceeds our threshold
        if relax_threshold | (best_match_score > match_threshold):
            # Update all Proj columns with values from project
            for project_col, df_col in column_mapping.items():
                updated_df.loc[idx, df_col] = filtered_project.loc[best_match_idx, project_col]
            updated_df.loc[idx, "best_match_score"] = best_match_score
    print(f"   Processed {progress_counter} rows")
    return updated_df

# Fuzzy matching using all avilable columns: rdc, year, and pi
# Define function to fuzzy match based on RDC, Year, and PI
def fuzzy_match_rdc_year_pi(pi_rdc_proj_data, project):
    # Make a copy of data before using fuzzy matching
    pre_fuzzy_data = pi_rdc_proj_data.copy()
    
    print("  Fuzzy matching project information based on RDC, years, and PI...")
    try:
        ryp_data = update_projects_with_fuzzy_match(pre_fuzzy_data, project)
        print("  Completed fuzzy matching project information based on RDC, years, and PI.\n")
    except Exception as e:
        print(f"Failed to fuzzy match project information based on RDC, years, and PI: {str(e)}")
        raise

    # return records after matching
    return ryp_data

# Define test function for fuzzy_match_rdc_year_pi()
def test_fuzzy_match_rdc_year_pi():
    # Create a test dataframe
    test_pi_rdc_proj_data = pd.DataFrame({
        'ProjID': [None],
        'OutputTitle': ['Economic Analysis of Census Data'],
        'ProjectRDC': ['Census RDC'],
        'ProjectYearStarted': [2020],
        'ProjectYearEnded': [2022],
        'ProjectPI': ['Dr. Smith']
    })
    
    # Create a test dataframe for project with one matching project
    test_project = pd.DataFrame({
        'Proj ID': ['P001'],
        'Title': ['Economic Analysis of Census Data'],  # Close match to OutputTitle
        'RDC': ['Census RDC'],                          # Exact match to ProjectRDC
        'Start Year': [2020],                           # Exact match to ProjectYearStarted
        'End Year': [2022],                             # Exact match to ProjectYearEnded
        'PI': ['Dr. Smith'],                            # Exact match to ProjectPI
        'Status': ['Active']
    })
    
    # Call the function with the test data
    result = fuzzy_match_rdc_year_pi(test_pi_rdc_proj_data, test_project)
    
    # Test that the ProjID was updated based on the fuzzy match
    assert result.loc[0, 'ProjID'] == 'P001', "Fuzzy matching failed to update ProjID"
    
    # Test that other project information was updated
    assert result.loc[0, 'ProjectStatus'] == 'Active', "Fuzzy matching failed to update ProjectStatus"
    
    print(" [Passed] - Test for function fuzzy_match_rdc_year_pi()")

# Fuzzy matching using RDC and authors with threshold
# Define function to fuzzy match based on RDC, and authors
def fuzzy_match_rdc_author(ryp_data, project):
    print("  Fuzzy matching project information based on RDC and authors...")
    try:
        rat_data = update_projects_with_fuzzy_match(
            ryp_data, project, match_threshold=80, use_year=False, use_pi=False,
            use_authors=True)
        print("  Completed fuzzy matching project information based on RDC and authors.\n")
    except Exception as e:
        print(f"Failed to fuzzy match project information based on RDC and authors: {str(e)}")
        raise

    # return records after matching
    return rat_data

# Define test function for fuzzy_match_rdc_author()
def test_fuzzy_match_rdc_author():
    # Create a test dataframe
    test_ryp_data = pd.DataFrame({
        'ProjID': [None],
        'OutputTitle': ['Analysis of Population Trends'],
        'ProjectRDC': ['Federal RDC'],
        'authors_set': [{'john smith', 'mary johnson'}],  # Set of authors
        'ProjectStatus': [None],
        'ProjectTitle': [None]
    })
    
    # Create a test dataframe for project with one matching project
    test_project = pd.DataFrame({
        'Proj ID': ['P002'],
        'Title': ['Population Analysis Project'],  # Somewhat similar to OutputTitle
        'RDC': ['Federal RDC'],                    # Exact match to ProjectRDC
        'PI': ['John Smith'],                      # PI matches one of the authors
        'Status': ['Completed'],
        'Start Year': [2019],
        'End Year': [2021]
    })
    
    # Call the function with the test data
    result = fuzzy_match_rdc_author(test_ryp_data, test_project)
    
    # Test that the ProjID was updated based on the fuzzy match
    assert result.loc[0, 'ProjID'] == 'P002', "Fuzzy matching on RDC and author failed to update ProjID"
    
    # Test that other project information was updated
    assert result.loc[0, 'ProjectStatus'] == 'Completed', "Fuzzy matching failed to update ProjectStatus"
    assert result.loc[0, 'ProjectTitle'] == 'Population Analysis Project', "Fuzzy matching failed to update ProjectTitle"
    
    print(" [Passed] - Test for function fuzzy_match_rdc_author()")

# Fuzzy matching using authors
# Define function to fuzzy match based on authors
def fuzzy_match_author(rat_data, project):
    print("  Fuzzy matching project information based on authors...")
    try:
        at_data = update_projects_with_fuzzy_match(
            rat_data, project, match_threshold=80,
            use_rdc=False, use_year=False, use_pi=False, use_authors=True)
        print("  Completed fuzzy matching project information based on authors.\n")
    except Exception as e:
        print(f"Failed to fuzzy match project information based on authors: {str(e)}")
        raise

    # return records after matching
    return at_data

# Define test function for fuzzy_match_author()
def test_fuzzy_match_author():
    # Create a test dataframe
    test_rat_data = pd.DataFrame({
        'ProjID': [None],
        'OutputTitle': ['Statistical Analysis of Census Data'],
        'authors_set': [{'jennifer wilson', 'robert lee'}],  # Set of authors
        'ProjectStatus': [None],
        'ProjectRDC': [None],  # No RDC information - testing author-only matching
        'ProjectTitle': [None]
    })
    
    # Create a test dataframe for project with one matching project
    test_project = pd.DataFrame({
        'Proj ID': ['P004'],
        'Title': ['Census Data Analytics'],        # Similar to OutputTitle
        'PI': ['Robert Lee'],                     # PI matches one of the authors
        'Status': ['In Progress'],
        'RDC': ['Boston RDC'],
        'Start Year': [2021],
        'End Year': [2024]
    })
    
    # Call the function with the test data
    result = fuzzy_match_author(test_rat_data, test_project)
    
    # Test that the ProjID was updated based on the fuzzy match
    assert result.loc[0, 'ProjID'] == 'P004', "Fuzzy matching on author only failed to update ProjID"
    
    # Test that other project information was updated
    assert result.loc[0, 'ProjectStatus'] == 'In Progress', "Fuzzy matching failed to update ProjectStatus"
    assert result.loc[0, 'ProjectRDC'] == 'Boston RDC', "Fuzzy matching failed to update ProjectRDC"
    assert result.loc[0, 'ProjectTitle'] == 'Census Data Analytics', "Fuzzy matching failed to update ProjectTitle"
    
    print(" [Passed] - Test for function fuzzy_match_author()")

# Fuzzy matching using just titles with threshold
# Define function to fuzzy match based on titles with threshold
def fuzzy_match_title_with_threshold(at_data, project):
    print("  Fuzzy matching project information based on titles...")
    try:
        t_data = update_projects_with_fuzzy_match(
            at_data, project, match_threshold=80,
            use_rdc=False, use_year=False, use_pi=False)
        print("  Completed fuzzy matching project information based on titles.\n")
    except Exception as e:
        print(f"Failed to fuzzy match project information based on titles: {str(e)}")
        raise

    # return records after matching
    return t_data

# Define test function for fuzzy_match_title_with_threshold()
def test_fuzzy_match_title_with_threshold():
    # Create a test dataframe
    test_at_data = pd.DataFrame({
        'ProjID': [None],
        'OutputTitle': ['Economic Impact of Trade Policies'],
        'ProjectStatus': [None],
        'ProjectRDC': [None],
        'ProjectYearStarted': [None],
        'ProjectYearEnded': [None],
        'ProjectPI': [None]
    })
    
    # Create a test dataframe
    test_project = pd.DataFrame({
        'Proj ID': ['P003'],
        'Title': ['Economic Impacts of International Trade Policies'],  # Similar title (>80% match)
        'Status': ['Active'],
        'RDC': ['Census RDC'],
        'Start Year': [2018],
        'End Year': [2023],
        'PI': ['Dr. Williams']
    })
    
    # Call the function with the test data
    result = fuzzy_match_title_with_threshold(test_at_data, test_project)
    
    # Test that the ProjID was updated based on the fuzzy match of titles
    assert result.loc[0, 'ProjID'] == 'P003', "Fuzzy matching on titles failed to update ProjID"
    
    # Test that other project information was updated
    assert result.loc[0, 'ProjectStatus'] == 'Active', "Fuzzy matching failed to update ProjectStatus"
    assert result.loc[0, 'ProjectRDC'] == 'Census RDC', "Fuzzy matching failed to update ProjectRDC"
    assert result.loc[0, 'ProjectYearStarted'] == 2018, "Fuzzy matching failed to update ProjectYearStarted"
    assert result.loc[0, 'ProjectYearEnded'] == 2023, "Fuzzy matching failed to update ProjectYearEnded"
    assert result.loc[0, 'ProjectPI'] == 'Dr. Williams', "Fuzzy matching failed to update ProjectPI"
    
    print(" [Passed] - Test for function fuzzy_match_title_with_threshold()")

# Fuzzy matching using just titles without threshold
# Define function to fuzzy match based on titles without threshold
def fuzzy_match_title_without_threshold(t_data, project):
    print("  Fuzzy matching project information based on titles without threshold...")
    try:
        nt_data = update_projects_with_fuzzy_match(
            t_data, project, match_threshold=80,
            use_rdc=False, use_year=False, use_pi=False, relax_threshold=True)
        print("  Completed fuzzy matching project information based on titles without threshold.\n")
    except Exception as e:
        print(f"Failed to fuzzy match project information based on titles without threshold: {str(e)}")
        raise

    # return records after matching
    return nt_data

# Define test function for clean_rdc_evidence()
def test_fuzzy_match_title_without_threshold():
    # Create a test dataframe
    test_t_data = pd.DataFrame({
        'ProjID': [None],
        'OutputTitle': ['Analysis of Labor Market Dynamics'],
        'ProjectStatus': [None],
        'ProjectRDC': [None],
        'ProjectYearStarted': [None],
        'ProjectYearEnded': [None],
        'ProjectPI': [None]
    })
    
    # Create a test dataframe for project with one matching project
    # Note: Title has a lower similarity match (would be below normal threshold)
    test_project = pd.DataFrame({
        'Proj ID': ['P005'],
        'Title': ['Effects of Minimum Wage on Labor Supply'],  # Less similar title (<80% match)
        'Status': ['Completed'],
        'RDC': ['Chicago RDC'],
        'Start Year': [2017],
        'End Year': [2022],
        'PI': ['Dr. Thompson']
    })
    
    # Call the function with the test data
    result = fuzzy_match_title_without_threshold(test_t_data, test_project)
    
    # Test that the ProjID was updated based on the fuzzy match of titles, even with low similarity
    # This works because relax_threshold=True is being used
    assert result.loc[0, 'ProjID'] == 'P005', "Fuzzy matching with relaxed threshold failed to update ProjID"
    
    # Test that other project information was updated
    assert result.loc[0, 'ProjectStatus'] == 'Completed', "Fuzzy matching failed to update ProjectStatus"
    assert result.loc[0, 'ProjectRDC'] == 'Chicago RDC', "Fuzzy matching failed to update ProjectRDC"
    assert result.loc[0, 'ProjectYearStarted'] == 2017, "Fuzzy matching failed to update ProjectYearStarted"
    assert result.loc[0, 'ProjectYearEnded'] == 2022, "Fuzzy matching failed to update ProjectYearEnded"
    assert result.loc[0, 'ProjectPI'] == 'Dr. Thompson', "Fuzzy matching failed to update ProjectPI"
    
    print(" [Passed] - Test for function fuzzy_match_title_without_threshold()")
    
# Define function to save the final processed data
def save_output(nt_data):
    # Save the output data as csv files and pkl file
    print("Saving project populated data...")
    nt_data.to_csv('Part_1/populated_data.csv', index=False)
    nt_data.to_pickle('Part_1/populated_data.pkl')
    print("Completed saving project populated data.\n")

if __name__ == "__main__":
    print("Testing functions...")
    # Test function lowercase_columns_copy()
    test_lowercase_columns_copy()
    # Test function add_group_idx()
    test_add_group_idx()
    # Test function prepare_group_1() to test_prepare_group_8()
    test_prepare_group_1()
    test_prepare_group_2()
    test_prepare_group_3()
    test_prepare_group_4()
    test_prepare_group_5()
    test_prepare_group_6()
    test_prepare_group_7()
    test_prepare_group_8()
    # Test function prepare_project_data()
    test_prepare_project_data()
    # Test function for data cleaning
    test_clean_doi()
    test_clean_source_url()
    test_clean_authors_researcher()
    test_clean_acknowledgement_evidence()
    test_clean_dataset_evidence()
    test_clean_disclosure_evidence()
    test_clean_rdc_evidence()
    test_clean_without_projid()
    test_clean_with_projid()
    # Test function to deduplicate
    test_deduplicate_data()
    # Test function to exact matching
    test_match_on_pi()
    test_match_on_pi_rdc()
    # Test function to fuzzy matching
    test_fuzzy_match_rdc_year_pi()
    test_fuzzy_match_rdc_author()
    test_fuzzy_match_author()
    test_fuzzy_match_title_with_threshold()
    test_fuzzy_match_title_without_threshold()
    print("Completed testing functions.\n")

    # Read in all group output data and all_metadata
    (data1, data2, data3, data4, data5, data6, data7, data8, all_metadata) = read_data()

    # Prepare all group output data and extract unique project information from all metadata
    clean_data1 = prepare_group_1(data1)
    clean_data2 = prepare_group_2(data2)
    clean_data3 = prepare_group_3(data3)
    clean_data4 = prepare_group_4(data4)
    clean_data5 = prepare_group_5(data5)
    clean_data6 = prepare_group_6(data6)
    clean_data7 = prepare_group_7(data7)
    clean_data8 = prepare_group_8(data8)
    project = prepare_project_data(all_metadata)

    # Integrate all group output data by concatenating them together
    combined_data = integrate_groups_data(clean_data1, clean_data2, clean_data3, clean_data4, 
                                          clean_data5,clean_data6, clean_data7, clean_data8)

    # Cleaning the combined data
    print("Cleaning combined data...")
    # Clean DOI column
    combined_data = clean_doi(combined_data)
    # Clean source and url columns
    combined_data = clean_source_url(combined_data)
    # Clean authors and researcher column
    combined_data = clean_authors_researcher(combined_data)
    # Clean acknowledgement evidence column
    combined_data = clean_acknowledgement_evidence(combined_data)
    # Clean dataset evidence column
    combined_data = clean_dataset_evidence(combined_data)
    # Clean disclosure evidence column
    combined_data = clean_disclosure_evidence(combined_data)
    # Clean RDC evidence column
    combined_data = clean_rdc_evidence(combined_data)
    # Clean records without Project ID
    combined_data = clean_without_projid(combined_data, project)
    # Clean records with Project ID
    corrected_proj_data = clean_with_projid(combined_data, project)
    print("Completed cleaning combined data.\n")

    # Deduplicate data
    deduplicated_data = deduplicate_data(corrected_proj_data)

    # Match project information
    print("Matching project information...")
    # Macth project based on PI
    pi_proj_data = match_on_pi(deduplicated_data, project)
    # Macth project based on PI and RDC
    pi_rdc_proj_data = match_on_pi_rdc(pi_proj_data, project)

    # Fuzzy matching
    print(" Fuzzy matching project information...")
    # Fuzzy matching using all avilable columns: rdc, year, and pi
    ryp_data = fuzzy_match_rdc_year_pi(pi_rdc_proj_data, project)
    # Fuzzy matching using RDC and authors with threshold
    rat_data = fuzzy_match_rdc_author(ryp_data, project)
    # Fuzzy matching using authors
    at_data = fuzzy_match_author(rat_data, project)
    # Fuzzy matching using just titles with threshold
    t_data = fuzzy_match_title_with_threshold(at_data, project)
    # Fuzzy matching using just titles without threshold
    nt_data = fuzzy_match_title_without_threshold(t_data, project)
    print(" Completed fuzzy matching project information.")
    print("Completed matching project information.\n")

    # Save the final output
    save_output(nt_data)



    





    



