#!/bin/bash

rm -rf doc_retrieval_env

python3 -m venv doc_retrieval_env

source doc_retrieval_env/bin/activate

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

pip install opensearch-py watchdog PyPDF2 python-docx flask pandas openpyxl 

pip install llama-index
# pip install llama-index-readers-elasticsearch 
# pip install llama-index-vector-stores-opensearch 
# pip install llama-index-embeddings-ollama
pip install llama-index-core
pip install llama-index-embeddings-huggingface

pip install llama-index-llms-ollama

deactivate