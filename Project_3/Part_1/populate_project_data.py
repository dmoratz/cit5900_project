# Import libraries
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz

if __name__ == "__main__":
    # Load in outputs of each group
    print("Reading in output data of all groups...")
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
        print("Passed test for function lowercase_columns_copy()")

    print("Testing function lowercase_columns_copy()...")
    # Test function lowercase_columns_copy()
    test_lowercase_columns_copy()
    print("Completed testing function lowercase_columns_copy().\n")

    # Define helper function to add column idx and group in a df
    # so that it could help to easily locate the record later
    def add_group_idx(df, group_number):
        print(" Adding group and index columns...")
        try:
            # Add group and index columns
            df["group"] = group_number
            df["idx"] = df.index
            print(" Completed adding group and index columns...")
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
        print("Passed test for function test_add_group_idx()")

    print("Testing function add_group_idx()...")
    # Test function add_group_idx()
    test_add_group_idx()
    print("Completed testing function add_group_idx().\n")

    # ----- Prepare Group 1 Output Data -----
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

    # ----- Prepare Group 2 Output Data -----
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

    # ----- Prepare Group 3 Output Data -----
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

    # ----- Prepare Group 4 Output Data -----
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

    # ----- Prepare Group 5 Output Data -----
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

    # ----- Prepare Group 6 Output Data -----
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

    # ----- Prepare Group 7 Output Data -----
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

    # ----- Prepare Group 8 Output Data -----
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

    # ----- Prepare All_Metadata Data -----
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

    # ---------- Data Integration ----------
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

    # ---------- Data Cleaning ----------
    print("Cleaning combined data...")

    # ----- Clean DOI column -----
    # There are some incomplete DOI values
    # Complete incomplete DOI
    try:
        combined_data.loc[~combined_data["doi"].str.contains("http", na=True), "doi"] = (
            "https://doi.org/" + combined_data.loc[~combined_data["doi"].str.contains("http", na=True), "doi"].str.strip()
        )
        # Check if there is no incomplete doi left after the change
        assert len(combined_data[~combined_data["doi"].str.contains("http", na=True)]) == 0
        print(" Completed cleaning doi column.")
    except Exception as e:
        print(f"Error cleaning DOI column: {str(e)}")
        raise

    # ----- Clean source and url column -----
    try:
        # url only exists when source is arXiv, other sources don't have urls
        # Drop column source and rename url column
        combined_data = combined_data.drop(columns="source")
        combined_data = combined_data.rename(columns={'url': 'arxiv_url'})
        print(" Completed cleaning source and url column.")
    except Exception as e:
        print(f"Error cleaning source and URL columns: {str(e)}")
        raise

    # ----- Clean authors and researcher column -----
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

    # ----- Clean acknowledgement evidence column -----
    try:
        # Update acknowledgments column based on fsrdc_acknowledgments_evidence
        # two columns existed in two separate data files
        combined_data.loc[combined_data["fsrdc_acknowledgments_evidence"].notna(), "acknowledgments"] = True
        print(" Completed cleaning acknowledgement evidence column.")
    except Exception as e:
        print(f"Error cleaning acknowledgement evidence column: {str(e)}")
        raise

    # ----- Clean dataset evidence column -----
    try:
        # Update dataset_mentions column based on other related column
        combined_data.loc[combined_data["dataset mentions"].notna(), "dataset_mentions"] = True
        combined_data.loc[combined_data["fsrdc_data_sources_evidence"].notna(), "dataset_mentions"] = True
        combined_data.loc[combined_data["matched_dataset_terms"].notna(), "dataset_mentions"] = True
        print(" Completed cleaning dataset evidence column.")
    except Exception as e:
        print(f"Error cleaning dataset evidence column: {str(e)}")
        raise

    # ----- Clean disclosure evidence column -----
    try:
        # Update disclosure_review column based on other related columns
        combined_data.loc[combined_data["fsrdc_disclosure_evidence"].notna(), "disclosure_review"] = True
        print(" Completed cleaning disclosure evidence column.")
    except Exception as e:
        print(f"Error cleaning disclosure evidence column: {str(e)}")
        raise

    # ----- Clean rdc evidence column -----
    try:
        # Update disclosure_review column based on other related columns
        combined_data.loc[combined_data["fsrdc_rdc_locations_evidence"].notna(), "rdc_mentions"] = True
        print(" Completed cleaning rdc column.")
    except Exception as e:
        print(f"Error cleaning RDC column: {str(e)}")
        raise

    # All records have valid Project ID
    # ----- Clean records without Project ID -----
    # All records have valid RDC values, start and end year at the same time, and project PI
    # Define list of project columns
    proj_cols = ['ProjID', 'ProjectStatus', 'ProjectTitle', 'ProjectRDC',
                'ProjectYearStarted', 'ProjectYearEnded', 'ProjectPI']

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

    # ----- Clean records with Project ID -----
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
    print("Completed cleaning combined data.\n")

    # ---------- Deduplication ----------
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

    # ---------- Matching Project Information ----------
    # Save a copy of depulicated data
    pre_match_data = deduplicated_data.copy()

    print("Matching project information...")
    # ----- Match based on PI -----
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

    # ----- Match based on PI and RDC -----
    # If certain PI only has one project in certain RDC, then the output belongs to that project
    try:
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

    # ----- Fuzzy matching -----
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

    # Make a copy of data before using fuzzy matching
    pre_fuzzy_data = pi_rdc_proj_data.copy()

    print(" Fuzzy matching project information...")
    # Fuzzy matching using all avilable columns: rdc, year, pi
    print("  Fuzzy matching project information based on RDC, years, and PI...")
    try:
        ryp_data = update_projects_with_fuzzy_match(pre_fuzzy_data, project)
        print("  Completed fuzzy matching project information based on RDC, years, and PI.\n")
    except Exception as e:
        print(f"Failed to fuzzy match project information based on RDC, years, and PI: {str(e)}")
        raise

    # Fuzzy matching using RDC and authors with author threshold
    print("  Fuzzy matching project information based on RDC and authors...")
    try:
        rat_data = update_projects_with_fuzzy_match(
            ryp_data, project, match_threshold=80, use_year=False, use_pi=False,
            use_authors=True)
        print("  Completed fuzzy matching project information based on RDC and authors.\n")
    except Exception as e:
        print(f"Failed to fuzzy match project information based on RDC and authors: {str(e)}")
        raise

    # Fuzzy matching using authors
    print("  Fuzzy matching project information based on authors...")
    try:
        at_data = update_projects_with_fuzzy_match(
            rat_data, project, match_threshold=80,
            use_rdc=False, use_year=False, use_pi=False, use_authors=True)
        print("  Completed fuzzy matching project information based on authors.\n")
    except Exception as e:
        print(f"Failed to fuzzy match project information based on authors: {str(e)}")
        raise

    # Fuzzy matching using just titles with threshold
    print("  Fuzzy matching project information based on titles...")
    try:
        t_data = update_projects_with_fuzzy_match(
            at_data, project, match_threshold=80,
            use_rdc=False, use_year=False, use_pi=False)
        print("  Completed fuzzy matching project information based on titles.\n")
    except Exception as e:
        print(f"Failed to fuzzy match project information based on titles: {str(e)}")
        raise

    # Fuzzy matching using just titles without threshold
    print("  Fuzzy matching project information based on titles without threshold...")
    try:
        nt_data = update_projects_with_fuzzy_match(
            t_data, project, match_threshold=80,
            use_rdc=False, use_year=False, use_pi=False, relax_threshold=True)
        print("  Completed fuzzy matching project information based on titles without threshold.\n")
    except Exception as e:
        print(f"Failed to fuzzy match project information based on titles without threshold: {str(e)}")
        raise
    print("Completed matching project information.\n")

    # Save the output data as csv files and pkl file
    print("Saving project populated data...")
    nt_data.to_csv('Part_1/populated_data.csv', index=False)
    nt_data.to_pickle('Part_1/populated_data.pkl')
    print("Completed saving project populated data.\n")







    



