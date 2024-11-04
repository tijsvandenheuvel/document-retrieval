#!/bin/bash

# Activate the virtual environment
source ../doc_retrieval_env/bin/activate

# Run the monitor_folder script
python3 query_documents.py

# Deactivate the virtual environment after the script finishes
deactivate
