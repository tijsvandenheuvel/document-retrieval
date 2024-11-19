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

### 4.1 LlamaIndex version

for the llamaindex version you need an openAI API key, which you can get on the [platform.openai.com](https://platform.openai.com/api-keys) website

This could also work with other LLMs but this will have to be set up differently.

##### 4.1.1 install dependencies

run this command once:

`pip install llama_index docx2txt`

##### 4.1.2 run script

run this command:

`python3 llamaindex_document_retrieval_llamaindex.py`