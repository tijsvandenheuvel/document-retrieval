from db_opensearch import opensearch_client
from llama_index.core import VectorStoreIndex, Document, Settings, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.replicate import Replicate
from transformers import AutoTokenizer
import os


# Define global settings
# Settings(chunk_size_limit=4096)  # Set chunk size
Settings.chunk_size = 4096

# os.environ["REPLICATE_API_TOKEN"] = "YOUR_REPLICATE_API_TOKEN"

# setup the LLM
# llama2_7b_chat = "meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e"
# Settings.llm = Replicate(
#     model=llama2_7b_chat,
#     temperature=0.01,
#     additional_kwargs={"top_p": 1, "max_new_tokens": 300},
# )

Settings.llm = None

# set tokenizer to match LLM
Settings.tokenizer = AutoTokenizer.from_pretrained(
    "NousResearch/Llama-2-7b-chat-hf"
)

# set the embed model
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)


def fetch_documents_from_opensearch(client, index_name):
    search_body = {
        "query": {"match_all": {}},  # Fetch all documents
        "_source": ["content", "content_vector", "file_path"]
    }
    response = client.search(index=index_name, body=search_body, size=1000)  # Adjust size for more documents

    documents = []
    for hit in response['hits']['hits']:
        source = hit['_source']
        documents.append({
            "content": source["content"],
            "vector": source["content_vector"],  # Vector embeddings
            "metadata": {"file_path": source.get("file_path", "")}  # Add any metadata needed
        })
        
    return documents

def init_llamaIndex():
    
    # setup the documents
    documents = fetch_documents_from_opensearch(opensearch_client, "documents")
    
    llama_documents = [
        Document(
            text=doc["content"],
            metadata=doc["metadata"]
        )
        for doc in documents
    ]
    
    # Build LlamaIndex
    index = VectorStoreIndex.from_documents(llama_documents)

    # Save the index for future use
    index.storage_context.persist("llamaindex_storage")
    
    # Query Example
    query_engine = index.as_query_engine()
    response = query_engine.query("Your query here")
    print(response)


def search_by_llamaindex(query, search_type):
    
    storage_context = StorageContext.from_defaults(persist_dir="./llamaindex_storage")
    index = load_index_from_storage(storage_context)
    
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response
    
#init_llamaIndex()
    
query = "give me a document about privacy"
search_type = "llamaindex"    
    
response = search_by_llamaindex(query, search_type)

print(response)