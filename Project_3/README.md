# Project for CIT 5900

## Organization

### Part 1 - Cleaning and Processing Other Groups Data

This section cleans, processes and deduplicates the data from all groups. It engages in data enhancement by linking works to projects

### Part 2 - API Data Enhancement and Validation

This section enhances data by extracting relevant publication information, including abstracts and keywords. It also validates whether data is legitimately FSRDC by checking for dataset or FSRDC mentions amongst the full text of all potential publications.

### Part 3 - EDA and Broader Analysis

This section engages in our initial data exploration and our analysis, producing the figures and results used on our website


## Running the files

While each section has files that can be run independently, the entire project can be executed via main.py. Simply running main.py will execute all .py files in the project.

## Dependencies Required:
numpy, pandas, fuzzywuzzy, os, subprocess, requests, BeautifulSoup, re, time, networkx, ast, collections, matplotlib, community, itertools, simpy, random, bertopic, io, seaborn, nltk, string, statsmodels.formula.api, umap, hdbscan, unittest, python-louvain

### To run the API integration, the api_integration.py file needs to be opened and the final two lines need to be uncommented. Warning: this file takes 10 hours to process!

## To run Part 5, upload the files in the Part 5 folder to Google Colab. This includes visualization.ipynb, unique_outputs_webscraping.csv and unique_research_outputs.csv