#!/bin/bash

rm -rf doc_retrieval_env

python3 -m venv doc_retrieval_env

source doc_retrieval_env/bin/activate

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

pip install opensearch-py watchdog PyPDF2 python-docx flask pandas openpyxl 

pip install llama-index llama-index-readers-elasticsearch llama-index-vector-stores-opensearch llama-index-embeddings-ollama

deactivate