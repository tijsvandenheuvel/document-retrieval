from db_opensearch import opensearch_client
from llama_index.core import VectorStoreIndex, Document, Settings


# Define global settings
# Settings(chunk_size_limit=4096)  # Set chunk size
Settings.chunk_size = 4096


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
    
    documents = fetch_documents_from_opensearch(opensearch_client, "documents")
    
    llama_documents = [
        Document(
            text=doc["content"],
            metadata={
                **doc["metadata"],
                "embedding": doc["vector"]
            }
        )
        for doc in documents
    ]
    
    # TODO: error asks for openAI key, look into local embedding model 
    
    # Build LlamaIndex with custom ServiceContext
    index = VectorStoreIndex.from_documents(llama_documents)

    # Save the index for future use
    index.storage_context.persist("llamaindex_storage")
    
    # Query Example
    query_engine = index.as_query_engine()
    response = query_engine.query("Your query here")
    print(response)


def search_by_llamaindex(query, search_type):
    
    init_llamaIndex()
    
    return []
    
    # documents = SimpleDirectoryReader('documents').load_data_sources()
    # index = VectorStoreIndex.from_documents(documents)
    # query_engine = index.as_query_engine()
    # response = query_engine.query(query)
    # return response