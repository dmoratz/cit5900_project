import pandas as pd
import requests
import time
import os

print("Must uncomment final lines for script to execute!")

def reconstruct_abstract(inverted_index):
    """
    Reconstructs the abstract text from an inverted index.
    The inverted index is a dict mapping words to lists of positions.
    """
    if not isinstance(inverted_index, dict) or not inverted_index:
        return None
    
    # Determine the total number of words by finding the highest position.
    max_index = max(pos for positions in inverted_index.values() for pos in positions)
    words = [None] * (max_index + 1)
    
    # Place each word at its corresponding positions.
    for word, positions in inverted_index.items():
        for pos in positions:
            words[pos] = word
            
    # Join the words to form the full abstract text.
    return " ".join(word for word in words if word is not None)

def fetch_openalex_data_by_doi(doi):
    """
    Fetch OpenAlex work data using DOI.
    """
    doi = doi.strip().replace("https://doi.org/", "").replace("http://doi.org/", "")
    url = f"https://api.openalex.org/works?filter=doi:{doi}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if results:
            return results[0]
        else:
            return None
    except Exception as e:
        print(f"Error fetching OpenAlex data for DOI {doi}: {e}")
        return None

def fetch_openalex_data_by_title(title):
    """
    Fetch OpenAlex work data using the paper title.
    """
    url = f"https://api.openalex.org/works?search={title}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if results:
            return results[0]
        else:
            return None
    except Exception as e:
        print(f"Error searching OpenAlex for title '{title}': {e}")
        return None

def process_openalex_data(work):
    """
    Given an OpenAlex work object, extract the abstract (if available)
    and keywords from the 'concepts' field.
    """
    # Reconstruct abstract from inverted index if available.
    inv_index = work.get("abstract_inverted_index")
    if inv_index:
        abstract = reconstruct_abstract(inv_index)
    else:
        abstract = "No abstract available"
    
    # Extract keywords from the concepts list.
    cited_by_count = work.get("cited_by_count", "No data")
    concepts = work.get("concepts", [])
    if concepts:
        # Each concept has a "display_name"; join them into a comma-separated string.
        concepts_str = ", ".join([concept.get("display_name", "") for concept in concepts])
    else:
        concepts_str = "No keywords available"
    
    # Extract topics
    topics = work.get("topics", [])
    if topics:
      topic_names = [t.get("display_name", "") for t in topics if t.get("display_name", "")]
      topics_str = "; ".join(topic_names)
    else:
      topics_str = "No topics available"
    
    return abstract, concepts_str, cited_by_count, topics_str

def get_abstract_and_keywords(row):
    """
    Attempt to retrieve the abstract and keywords using DOI (via OpenAlex first,
    then falling back to title search).
    """
    doi = row.get("DOI")
    title = row.get("OutputTitle")
    
    work = None
    if pd.notna(doi) and doi.strip() and doi.strip().startswith("10."):
        work = fetch_openalex_data_by_doi(doi)
    
    # Fallback to title search if DOI retrieval failed.
    if not work:
        work = fetch_openalex_data_by_title(title)
    
    if work:
        return process_openalex_data(work)
    else:
        return "No work found", "No topics found", "No data", "No keywords found"

def process_csv(output_csv):
    """
    Reads the CSV, retrieves abstracts and keywords using OpenAlex, and
    writes a new CSV with added 'abstracts' and 'keywords_openalex' columns.
    """
    
    abstract_list = []
    concepts_list = []
    cited_by_count_list = list()
    topics_list = []
    
    for index, row in df.iterrows():
        print(f"Processing row {index+1}: {row.get('OutputTitle')}")
        abstract, concepts_str, cited_by_count, topics_str = get_abstract_and_keywords(row)
        abstract_list.append(abstract)
        concepts_list.append(concepts_str)
        cited_by_count_list.append(cited_by_count)
        topics_list.append(topics_str)
        time.sleep(1)  # Delay to avoid rate limits
        
    df["abstracts"] = abstract_list
    df["concepts_openalex"] = concepts_list
    df["cited_by_count"] = cited_by_count_list
    df["keywords_openalex"] = topics_list
    df.to_csv(output_csv, index=False)
    print(f"Processed CSV saved as {output_csv}")

# Must be uncommented for file to run!

#if __name__ == "__main__":
#    script_dir = os.path.dirname(os.path.realpath(__file__))
#    file_path = os.path.join(script_dir, "cleaned_biblio.csv")
#    df = pd.read_csv(file_path, encoding='utf-8')
#    output_csv = "cleaned_abstracts_project3.csv"
#    process_csv(output_csv)