#!/bin/bash

# Activate the virtual environment
source doc_retrieval_env/bin/activate

cd flask_app

# Run the monitor_folder script
python3 monitor_folder.py

# Deactivate the virtual environment after the script finishes
deactivate
