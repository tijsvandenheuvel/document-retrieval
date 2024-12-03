from db_opensearch import opensearch_client
from llama_index.core import VectorStoreIndex, Document, Settings, ComposableGraph, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from llama_index.embeddings.ollama import OllamaEmbedding
# from llama_index.core.query_engine import RetrieverQueryEngine
# from llama_index.llms.ollama import Ollama
# from transformers import AutoTokenizer

# from llama_index.indices.composability import ComposableGraph
# import os
import time
from datetime import datetime

def fetch_documents_from_opensearch(client, index_name):
    search_body = {
        "query": {"match_all": {}},  # Fetch all documents
        "_source": ["content", "content_vector", "file_path"]
    }
    response = client.search(index=index_name, body=search_body, size=10000)

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
    
    # chunk_size = 8192
    chunk_size = 4096
    # chunk_size = 2048
    Settings.chunk_size = chunk_size
    # Settings.chunk_overlap = 50
    
    # optimization: use llm
    # no change?
    Settings.llm = None
    # Settings.llm = Ollama(model="llama3.2", request_timeout=60.0)

    # set tokenizer to match LLM
    # Settings.tokenizer = AutoTokenizer.from_pretrained(
    #     "NousResearch/Llama-2-7b-chat-hf"
    # )
    
    # optimization: use better embedding algorithm
    
    model_name="dunzhang/stella_en_1.5B_v5"
    # model_name="BAAI/bge-small-en-v1.5"
    # model_name="BAAI/bge-m3"
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=model_name
    )
    
    # model_name = "llama3.2"
    # Settings.embed_model = OllamaEmbedding(
    #     model_name=model_name,
    #     base_url="http://localhost:11434",
    #     ollama_additional_kwargs={"mirostat": 0},
    # )
    
    print(f"Embedding model: {model_name}")
    print(f"Chunk size: {chunk_size}")
    
    # start_time = time.time()

    documents = fetch_documents_from_opensearch(opensearch_client, "documents")
    
    print(f"Documents: {len(documents)}")
    
    # end_time = time.time()
    
    # print(f"Fetching documents time: {round(end_time - start_time, 5)} seconds")
    
    # documents = documents[:10]
    
    llama_documents = [
        Document(
            text=doc["content"],
            metadata=doc["metadata"]
        )
        for doc in documents
    ]
    
    batch_size = 500  # Process documents in batches
    indexes = []
    
    print(f"Batch size: {batch_size}")

    print(f"start indexing at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    for i in range(0, len(llama_documents), batch_size):
        start_time = time.time()
        batch = llama_documents[i:i + batch_size]
        index = VectorStoreIndex.from_documents(batch)
        indexes.append(index)
        end_time = time.time()
        print(f"Indexing time for batch {i//batch_size + 1}: {round(end_time - start_time, 2)} seconds")

    # Combine the indexes if needed
    final_index = ComposableGraph.from_indices(indexes)
    
    print("writing index to file")
    storage_file = "llamaindex_stella"
    final_index.storage_context.persist(storage_file)
    
    # Build LlamaIndex
    
    # start_time = time.time()
    
    # index = VectorStoreIndex.from_documents(llama_documents)
    
    # end_time = time.time()
    
    # print(f"Indexing time: {round(end_time - start_time, 2)} seconds")
        
    # start_time = time.time()
        
    # query_engine = index.as_query_engine(
    #     response_mode="no_text",
    #     similarity_top_k=10
    #     )
    
    # end_time = time.time()
    
    # print(f"Setup query engine time: {round(end_time - start_time, 5)} seconds")
    
    # optimization: use retriever engine
    # query_engine = RetrieverQueryEngine(
    #     retriever=index.as_retriever(
    #         # response_mode="no_text",
    #         similarity_top_k=10
    #         )
    #     )   
    
     # optimization: hybrid search

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
        # print(f"File path: {doc['file_path']}")
        # print(f"Score: {doc['score']}")
        print()



# TESTING


query_engine = initialize_llamaindex()

query = "privacy"
    
# results = search_by_llamaindex(query, query_engine)

# print_results(query, results)