from db_opensearch import opensearch_client
from llama_index.core import VectorStoreIndex, Document, Settings, StorageContext, load_index_from_storage, ServiceContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.text_splitter import SentenceSplitter
import os

def initialize_llamaindex_LABSE():
    Settings.llm = None
    
    model_name="sentence-transformers/LaBSE"
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=model_name
    )
    
    chunk_size = 512
    Settings.chunk_size = chunk_size

    storage_file = "llamaindex_labse"
    
    if os.path.exists(f"./{storage_file}"):
        print("llamaindex: loading labse index from storage")
        
        # index= VectorStoreIndex.load_from_disk(storage_file, service_context=service_context_1)
        storage_context = StorageContext.from_defaults(persist_dir=f"./{storage_file}")
        index = load_index_from_storage(storage_context)
        
    else:
        print("llamaindex: Can't find storage")
        index = None
        
    query_engine = index.as_query_engine(
        response_mode="no_text",
        similarity_top_k=20
        )

    return query_engine

def initialize_llamaindex_BGE():
    Settings.llm = None
    
    model_name="BAAI/bge-small-en-v1.5"
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=model_name
    )
    
    chunk_size = 4096
    Settings.chunk_size = chunk_size
    
    storage_file = "llamaindex_bge_small"
    
    if os.path.exists(f"./{storage_file}"):
        print("llamaindex: loading bge index from storage")
        # index= VectorStoreIndex.load_from_disk(storage_file, service_context=service_context_1)
        storage_context = StorageContext.from_defaults(persist_dir=f"./{storage_file}")
        index = load_index_from_storage(storage_context)
    else:
        print("llamaindex: Can't find storage")
        index = None
        
    query_engine = index.as_query_engine(
        response_mode="no_text",
        similarity_top_k=20
        )

    return query_engine

def format_response(response, search_type):
    source_nodes = response.source_nodes  # List of source nodes

    grouped_results = {}
    for node in source_nodes:
        file_path = node.metadata["file_path"]
        if file_path not in grouped_results:
            grouped_results[file_path] = {
                "title": file_path.split('/')[-1],
                "file_path": file_path,
                "content": node.text[:200],
                "score": node.score,
                "search_type": search_type
            }
        else:
            # Optionally, update with a higher score or merge content
            grouped_results[file_path]["score"] = max(grouped_results[file_path]["score"], node.score)
    return list(grouped_results.values())[:10]
    
def search_by_llamaindex(query, query_engine, search_type):
    
    if search_type == 'llamaindex_bge':
        chunk_size = 4096
        model_name="BAAI/bge-small-en-v1.5"
    elif search_type == 'llamaindex_labse':
        chunk_size = 512
        model_name="sentence-transformers/LaBSE"

    Settings.embed_model = HuggingFaceEmbedding(
        model_name=model_name
    )
    Settings.chunk_size = chunk_size

    response = query_engine.query(query)
    return format_response(response, search_type)
    
def print_results(query, results):
    print(f"query: {query}")
    # Print the retrieved documents
    for idx, doc in enumerate(results, start=1):
        print(f"Document {idx}: {doc['title']}")
        # print(f"Content: {doc['content'][:200]}")
        # print(f"File path: {doc['file_path']}")
        # print(f"Score: {doc['score']}")
        print()

# TESTING

# query_engine1 = initialize_llamaindex_BGE()
# query_engine2 = initialize_llamaindex_LABSE()
    
# query = "privacy"
# results = search_by_llamaindex(query, query_engine1, 'llamaindex_bge')
# print_results(query, results)
# results = search_by_llamaindex(query, query_engine2, 'llamaindex_labse')
# print_results(query, results)