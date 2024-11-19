#!/bin/bash

rm -rf doc_retrieval_env

python3 -m venv doc_retrieval_env

source doc_retrieval_env/bin/activate

pip install -r requirements.txt

deactivate