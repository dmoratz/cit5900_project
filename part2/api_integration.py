import requests
import time
import pandas as pd
import os

print("This file will only run if you uncomment out the code at the bottom!")

# Determine the directory of the current .py file
script_dir = os.path.dirname(os.path.realpath(__file__))

def reconstruct_abstract(inverted_index):
    """
    Reconstructs the abstract text from an inverted index.
    The inverted index is a dict mapping words to lists of positions.
    """
    if not isinstance(inverted_index, dict) or not inverted_index:
        return "No abstract available"
    max_index = max(pos for positions in inverted_index.values() for pos in positions)
    words = [None] * (max_index + 1)
    for word, positions in inverted_index.items():
        for pos in positions:
            words[pos] = word
    return " ".join(w for w in words if w is not None)

def get_author_id(author_name):
    """
    Given a researcher name, query the OpenAlex Authors API to return the canonical author ID.
    """
    url = "https://api.openalex.org/authors"
    params = {"search": author_name, "per_page": 1}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if results:
            # Returns a URL like "https://openalex.org/A1969200700"
            return results[0].get("id")
        else:
            return None
    except Exception as e:
        print(f"Error fetching author ID for '{author_name}': {e}")
        return None
    
def query_openalex_by_researcher_datasets(author_id, dataset_terms, per_page=50, max_pages=3):
    """
    For a given author (by canonical ID) and a list of dataset terms, build a combined filter
    that uses the OR operator for the dataset terms (with each term wrapped in quotation marks)
    and query the OpenAlex Works API.
    """
    base_url = "https://api.openalex.org/works"
    # Wrap each dataset term in quotes and join using OR.
    or_query = " OR ".join([f'"{term}"' for term in dataset_terms])
    filter_str = f"default.search:({or_query}),authorships.author.id:{author_id}"

    works = []
    for page in range(1, max_pages + 1):
        params = {
            "page": page,
            "filter": filter_str,
            "sort": "relevance_score:desc",
            "per_page": per_page
        }
        # Construct the full query URL for printing.
        query_url = f"{base_url}?page={page}&filter={filter_str}&sort=relevance_score:desc&per_page={per_page}"
        print(f"API Request: {query_url}")
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            page_results = data.get("results", [])
            if not page_results:
                break
            works.extend(page_results)
            time.sleep(1)  # Pause to respect rate limits.
        except Exception as e:
            print(f"Error querying for datasets '{or_query}' and author '{author_id}': {e}")
            break
    return works

def check_individual_dataset_matches(work, dataset_terms):
    """
    Given a work record and a list of dataset terms, check which of these terms are found
    in the combined text of the title and the reconstructed abstract.
    Returns a list of matched dataset terms.
    """
    # Ensure title is a string even if None
    title = work.get("title") or ""
    inv_index = work.get("abstract_inverted_index")
    abstract = reconstruct_abstract(inv_index) if inv_index else ""
    combined_text = (title + " " + abstract).lower()
    matches = [term for term in dataset_terms if term.lower() in combined_text]
    return matches

def process_work(work):
    """
    Extract the required fields from an OpenAlex work record.
    Adds the publication_date (if available), source display name, and type_crossref.
    """
    title = work.get("title", "")
    doi = work.get("doi", "")
    inv_index = work.get("abstract_inverted_index")
    abstract = reconstruct_abstract(inv_index) if inv_index else "No abstract available"
    year = work.get("publication_year", "")
    # Extract full publication date if available.
    publication_date = work.get("publication_date", "")
    cited_by_count = work.get("cited_by_count", "")

    # Process authors and affiliations.
    authors_list = []
    affiliations_list = []
    for authorship in work.get("authorships", []):
        author_name = authorship.get("author", {}).get("display_name", "")
        if author_name:
            authors_list.append(author_name)
        institutions = authorship.get("institutions", [])
        inst_names = [inst.get("display_name", "") for inst in institutions if inst.get("display_name", "")]
        if inst_names:
            affiliations_list.append("; ".join(inst_names))
    authors_str = "; ".join(authors_list)
    affiliations_str = "; ".join(affiliations_list)

    # Extract topics
    topics = work.get("topics", [])
    topic_names = [t.get("display_name", "") for t in topics if t.get("display_name", "")]
    topics_str = "; ".join(topic_names)

    # Extract host venue details: source display name and type_crossref.
    host_venue = work.get("primary_location", {})  or {}
    source = host_venue.get("source", {})  or {}
    source_display_name = source.get("display_name",
                                     "")  if isinstance(source, dict) else ""
    type_crossref = work.get("type", "")  if work else ""

    return {
        "title": title,
        "doi": doi,
        "abstract": abstract,
        "year": year,
        "publication_date": publication_date,
        "cited_by_count": cited_by_count,
        "authors": authors_str,
        "affiliations": affiliations_str,
        "topics": topics_str,
        "source_display_name": source_display_name,
        "type_crossref": type_crossref
    }

def chunk_list(lst, chunk_size):
    """Yield successive chunks of size chunk_size from list lst."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def main():
    # Read the CSV that has two columns: "researcher" and "dataset".
    df = pd.read_csv("../part1/dataset_data.csv")
    # Group by researcher and collect the unique dataset terms for each researcher.
    grouped = df.groupby("researcher")["dataset"].apply(lambda terms: list(set(terms))).reset_index()

    results = []
    # Cache for author IDs to avoid repeated lookups.
    author_cache = {}

    # Loop over each researcher.
    for idx, row in grouped.iterrows():
        researcher = row["researcher"]
        dataset_terms = row["dataset"]  # List of dataset terms for this researcher.
        print(f"Processing researcher '{researcher}' with {len(dataset_terms)} dataset terms.")

        # Retrieve the canonical author ID (or use cached value if available).
        if researcher in author_cache:
            author_id = author_cache[researcher]
        else:
            author_id = get_author_id(researcher)
            author_cache[researcher] = author_id

        if not author_id:
            print(f"  No OpenAlex ID found for researcher '{researcher}'. Skipping.")
            continue

        # Split the dataset terms into chunks of at most 4.
        for chunk in chunk_list(dataset_terms, 4):
            print(f"  Querying chunk: {chunk}")
            works = query_openalex_by_researcher_datasets(author_id, chunk)
            print(f"    Found {len(works)} works for chunk: {chunk}")
            for work in works:
                matched_terms = check_individual_dataset_matches(work, chunk)
                if matched_terms:
                    record = process_work(work)
                    record["researcher"] = researcher
                    record["author_id"] = author_id
                    record["queried_dataset_terms"] = "; ".join(chunk)
                    record["matched_dataset_terms"] = "; ".join(matched_terms)
                    results.append(record)
            time.sleep(1)  # Pause between chunks.
        time.sleep(2)  # Pause between researchers.

    # Save the results to a CSV file.
    output_df = pd.DataFrame(results)

    # Build the output file path in the same directory
    output_file = os.path.join(script_dir, "openalex_researcher_datasets_matches.csv")

    output_df.to_csv(output_file, index=False)
    print(f"Saved {len(output_df)} matching records to {output_file}")

# Run the file
# Currently commented out to prevent file running- it takes 10 hours to process!
# So uncomment these lines if you'd like the file to run
#if __name__ == "__main__":
#    main()