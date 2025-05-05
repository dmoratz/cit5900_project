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

def format_author_list(authors_str):
    """
    Convert 'Jane Doe; John Smith' to 'Doe, Jane; Smith, John'
    """
    authors = [a.strip() for a in authors_str.split(";") if a.strip()]
    formatted = []
    for name in authors:
        parts = name.split()
        if len(parts) >= 2:
            last = parts[-1]
            first = " ".join(parts[:-1])
            formatted.append(f"{last}, {first}")
        else:
            formatted.append(name)  # leave as-is if it's a single word
    return "; ".join(formatted)

def reconstruct_bibliography(authors, title, source, year, volume, issue, page_range, doi=""):
    """
    Constructs a basic citation-style bibliography string.
    """
    authors_str = format_author_list(authors) if authors else "Unknown Author"
    title_str = f'"{title}"' if title else "Untitled"
    source_str = source if source else "No Source"
    volume_issue = f"{volume}({issue})" if volume and issue else volume or ""
    pages = f", pp. {page_range}" if page_range != "-" else ""
    doi_part = f". https://doi.org/{doi}" if doi else ""
    
    parts = [
        authors_str + ".",
        f"{year}." if year else "",
        title_str + ".",
        source_str + ("," if volume_issue or pages else "."),
        volume_issue + pages + "." if volume_issue or pages else "",
        doi_part
    ]
    
    # Remove empty components and join with spaces
    return " ".join(part.strip() for part in parts if part.strip())
    
def search_openalex_by_doi(doi):
    '''
    LEGACY CODE
    Searches OpenAlex by DOI
    '''
    doi = doi.strip().replace("https://doi.org/", "").replace("http://doi.org/", "")
    url = f"https://api.openalex.org/works?filter=doi:{doi}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        results = response.json().get("results", [])
        return results[0] if results else None
    except Exception as e:
        print(f"DOI lookup failed for {doi}: {e}")
        return None

def search_openalex_by_title(title):
    '''
    LEGACY CODE
    Searches OpenAlex by Title. Only used if DOI is unavailable
    '''
    url = f"https://api.openalex.org/works?search={title}&per_page=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        results = response.json().get("results", [])
        return results[0] if results else None
    except Exception as e:
        print(f"Title lookup failed for '{title}': {e}")
        return None
    
def chunk_terms_by_char_limit(terms, max_length=1000):
    """
    Splits a list of terms into chunks so that the OR-joined query string
    (each term quoted) is less than or equal to max_length characters.
    """
    chunks = []
    current_chunk = []
    current_length = 0

    for term in terms:
        quoted_term = f'"{term}"'
        add_length = len(quoted_term) + (4 if current_chunk else 0)  # includes " OR "
        if current_length + add_length > max_length:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = [term]
            current_length = len(quoted_term)
        else:
            current_chunk.append(term)
            current_length += add_length

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def search_openalex_fulltext_term_check(doi, title, dataset_terms):
    """
    Uses OpenAlex fulltext search to check if any dataset terms appear
    in the full text for a given DOI or title. If so, return the work
    """
    if not doi and not title:
        return []

    # Prepare the OR query
    or_query = " OR ".join([f'"{term}"' for term in dataset_terms])
    base_url = "https://api.openalex.org/works"

    # Set chunks for dataset term searches
    chunks = chunk_terms_by_char_limit(dataset_terms, max_length=1000)

    for chunk in chunks:
        or_query = " OR ".join([f'"{term}"' for term in chunk])

        if doi:
            clean_doi = doi.strip().replace("https://doi.org/", "").replace("http://doi.org/", "")
            filter_str = f'default.search:({or_query}),doi:{clean_doi}'
            params = {"filter": filter_str, "per_page": 1}
        else:
            params = {
                "search": title,
                "filter": f'default.search:({or_query})',
                "per_page": 1
            }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            if results:
                return results[0]
        except Exception as e:
            print(f"Error querying OpenAlex for {doi or title}: {e}")
            continue

def check_individual_dataset_matches(work, dataset_terms):
    """
    LEGACY CODE
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

    # Extract host venue details: source display name and type_crossref, bibliography, etc
    host_venue = work.get("primary_location", {})  or {}
    source = host_venue.get("source", {})  or {}
    source_display_name = source.get("display_name",
                                     "")  if isinstance(source, dict) else ""
    type_crossref = work.get("type", "")  if work else ""
    # Get Bibliography information
    biblio = work.get("biblio") if work else ""
    
    # Line for debugging:
    # print("Debug Biblio", biblio)
    
    volume = biblio.get("volume", "")
    issue = biblio.get("issue", "")

    # Construct pages
    first_page = biblio.get("first_page","")
    last_page = biblio.get("last_page","")
    if first_page and last_page:
        page_range = f"{first_page}-{last_page}"
    elif first_page:
        page_range = first_page
    elif last_page:
        page_range = last_page
    else:
        page_range = ""
    
    output_status = "published" if type_crossref else ""
    publication_date = work.get("publication_date") if work else ""
    publication_month = publication_date.split("-")[1] if publication_date else ""

     # Bibliographic reconstruction
    bibliography = reconstruct_bibliography(
        authors_str,
        title,
        source_display_name,
        year,
        volume,
        issue,
        page_range,
        doi=doi
    )

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
        "OutputVenue": source_display_name,
        "OutputType": type_crossref,
        "OutputStatus": output_status,
        "OutputMonth": publication_month,
        "OutputBibliography": bibliography,
        "OutputVolume": volume,
        "OutputNumber": issue,
        "OutputPages": page_range
    }

def main():
    '''
    Function to run the processing
    '''
    # Load the main data
    data = pd.read_csv(os.path.join(script_dir, "data_to_scrape.csv"))

    # Load dataset terms
    dataset_terms = pd.read_csv(os.path.join(script_dir, "new_dataset_terms.csv"), header=None)[0].dropna().str.lower().tolist()


    # Storage for new columns
    results = []

    # Loop over each work.
    for idx, row in data.iterrows():
        doi = str(row.get("doi", "")).strip()
        title = str(row.get("OutputTitle", "")).strip()
        work = None

        print(f"Processing row {idx + 1}: '{title}'")

        work = search_openalex_fulltext_term_check(doi, title, dataset_terms)

        if work:
            # Process the work
            record = process_work(work)
            record["matched_dataset_terms"] = "true"

            # Merge with original row (preserving all original columns)
            merged = row.to_dict()
            merged.update(record)
            results.append(merged)
    time.sleep(1)  # Pause between works

    # Save the results to a CSV file.
    output_df = pd.DataFrame(results)

    # Build the output file path in the same directory
    output_file = os.path.join(script_dir, "output_matches_new.csv")

    output_df.to_csv(output_file, index=False)
    print(f"Saved {len(output_df)} matching records to {output_file}")

# Run the file
# Currently commented out to prevent file running- it takes 10 hours to process!
# So uncomment these lines if you'd like the file to run
if __name__ == "__main__":
    main()

input("Press Enter to exit...")