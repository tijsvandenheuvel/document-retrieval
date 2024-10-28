import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage

# step 1: setup LLM
filename = 'apikey.txt'
def get_file_contents(filename):
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)
api_key = get_file_contents(filename)
os.environ["OPENAI_API_KEY"] = api_key

# step 2: setup index

directory_path = "documents"

if os.path.exists("./storage"):
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)
else:
    documents = SimpleDirectoryReader(directory_path).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist()

query_engine = index.as_query_engine()

# step 3: query

def search_documents(query):
    response = query_engine.query(query)
    return response

# Step 4: Run a sample query
# query = "Give me documents about security cameras"
query = input("Find a document: ")
result = search_documents(query)

# Display results
print("Search Results:")

print(result)