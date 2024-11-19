#### 3.2 Create a virtual environment

We create a virtual environment to keep the project dependencies separate from the rest of the system.

In the Terminal, run this command:

`python3 -m venv doc_retrieval_env`

To activate the virtual environment, run this command:

`source doc_retrieval_env/bin/activate`

Note: You can deacticate the virtual environment with the command:

`deactivate`

#### 3.3 add documents to the documents folder

Note: This version only works with `.pdf` and `.docx` files.

### 4. Run the code

#### 4.2 from scratch version

This is based on the tutorial [A beginner's guide to building a Retrieval Augmented Generation (RAG) application from scratch](https://learnbybuilding.ai/tutorials/rag-from-scratch)

##### 4.2.1 install dependencies

run this command once:

`pip install PyPDF2 python-docx`

##### 4.2.2 run script

run this command:

`python3 simple_retrieval/document_retrieval_from_scratch.py`