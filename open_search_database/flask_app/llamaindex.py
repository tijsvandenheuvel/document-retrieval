from db_opensearch import opensearch_client
from llama_index.core import VectorStoreIndex, Document, Settings, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.replicate import Replicate
from transformers import AutoTokenizer
import os

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

def initialize_llamaindex():
    
    # settings 
    Settings.chunk_size = 8192
    Settings.llm = None

    # set tokenizer to match LLM
    Settings.tokenizer = AutoTokenizer.from_pretrained(
        "NousResearch/Llama-2-7b-chat-hf"
    )

    # set the embed model
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    # create index
    
    storage_file = "llamaindex_storage"
    
    if os.path.exists(f"./{storage_file}"):
        print("llamaindex: loading index from storage")
        storage_context = StorageContext.from_defaults(persist_dir=f"./{storage_file}")
        index = load_index_from_storage(storage_context)
    elif os.path.exists(f"./flask_app/{storage_file}"):
        print("llamaindex: loading index from storage")
        storage_context = StorageContext.from_defaults(persist_dir=f"./flask_app/{storage_file}")
        index = load_index_from_storage(storage_context)
    else:
        print("llamaindex: creating index from opensearch documents")

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
        
    query_engine = index.as_query_engine(
        response_mode="no_text",
        similarity_top_k=10
        )
    return query_engine

def format_response(response):
    source_nodes = response.source_nodes  # List of source nodes

    # print(source_nodes[0])

    results = [
        {
            "title": node.metadata["file_path"].split('/')[-1],
            "file_path": node.metadata["file_path"],
            "content": node.text[:200],
            "score": node.score,
            "search_type": 'llamaindex',
            # "metadata": node.metadata  # Extract metadata (e.g., file paths, tags)
        }
        for node in source_nodes
    ]
    
    return results
    
def search_by_llamaindex(query, query_engine):
    response = query_engine.query(query)
    return format_response(response)
    
def print_results(query, results):
    print(f"query: {query}")
    # Print the retrieved documents
    for idx, doc in enumerate(results, start=1):
        print(f"Document {idx}: {doc['title']}")
        # print(f"Content: {doc['content'][:200]}")
        print(f"File path: {doc['file_path']}")
        print(f"Score: {doc['score']}")
        print()
# TESTING

query_engine = initialize_llamaindex()
    
# query = "Can companies process judicial data to fight corruption?"
# query = "privacy"

query = "What is the impact of the GDPR on the M&A market in the US?"
# expected result = "2018-03-26_impact_of_the_european_general_data_protection_regulation_on_u.s._manda.pdf"
    
results = search_by_llamaindex(query, query_engine)

print_results(query, results)