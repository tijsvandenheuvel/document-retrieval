# document-retrieval

## setup

### 1. Download the repository

On [this page](https://github.com/tijsvandenheuvel/document-retrieval)

click the green ` < > Code ▾ ` Button

click Download ZIP

Extract the zip file

### 2. Install python (on mac)

#### 2.1 Check if it is allready installed

In the Terminal, run this command:

`python3 --version`

#### 2.2 Install the [Homebrew package manager](https://brew.sh/)

In the Terminal, run this command: 

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`


#### 2.3 Install python

In the Terminal, run this command:

`brew install python`

check installation with

`python3 --version`

### 3. Setup environment

#### 3.1 navigate to project

Open the project in the Terminal

You can navigate to the project folder using the `cd` command.

You can also right-click the folder and click `New Terminal at Folder`

#### 3.2 Create a virtual environment

We create a virtual environment to keep the project dependencies separate from the rest of the system.

In the Terminal, run this command:

`python3 -m venv doc_retrieval_env`

To activate the virtual environment, run this command:

`source doc_retrieval_env/bin/activate`

Note: You can deacticate the virtual environment with the command:

`deactivate`

#### 3.3 Install dependencies

run this command:

`pip3 install llama_index docx2txt`

#### 3.4 add documents to the documents folder

Note: This version only works with `.pdf` and `.docx` files.

### 4. Run the code

#### 4.1 LlamaIndex version

for the llamaindex version you need an openAI API key, which you can get on the [platform.openai.com](https://platform.openai.com/api-keys) website

This could also work with other LLMs but this will have to be set up differently.

run this command:

`python3 document_retrieval_llamaindex.py`

#### 4.2 from scratch version

This is based on the tutorial [A beginner's guide to building a Retrieval Augmented Generation (RAG) application from scratch](https://learnbybuilding.ai/tutorials/rag-from-scratch)

run this command:

`python3 document_retrieval_from_scratch.py`