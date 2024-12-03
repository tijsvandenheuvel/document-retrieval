# %% [markdown]
# # Llamaindex create index

# %%
from db_opensearch import opensearch_client
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import time
from datetime import datetime
from pympler import asizeof
from llama_index.core.node_parser import SimpleNodeParser

# %% [markdown]
# ## helper functions

# %%
def fetch_documents_from_opensearch(client, index_name, num_of_docs):
    search_body = {
        "query": {"match_all": {}},  # Fetch all documents
        "_source": ["content", "content_vector", "file_path"]
    }
    response = client.search(index=index_name, body=search_body, size=num_of_docs)

    documents = []
    for hit in response['hits']['hits']:
        source = hit['_source']
        documents.append({
            "content": source["content"],
            "vector": source["content_vector"],  # Vector embeddings
            "metadata": {"file_path": source.get("file_path", "")}  # Add any metadata needed
        })
        
    return documents

def format_bytes(size):
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
        
def format_seconds(seconds):
    days = int(seconds // 86400)
    seconds %= 86400
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds %= 60

    result = []
    if days > 0:
        result.append(f"{days} days")
    if hours > 0:
        result.append(f"{hours} hours")
    if minutes > 0:
        result.append(f"{minutes} minutes")
    result.append(f"{seconds:.2f} seconds")

    return ", ".join(result)

# %% [markdown]
# ## config llamindex

# %%
chunk_size = 4096
Settings.chunk_size = chunk_size

Settings.llm = None

model_name="dunzhang/stella_en_1.5B_v5"
Settings.embed_model = HuggingFaceEmbedding(
    model_name=model_name
)

print(f"Embedding model: {model_name}")
print(f"Chunk size: {chunk_size}")

# %% [markdown]
# ## fetch documents

# %%
documents = fetch_documents_from_opensearch(opensearch_client, "documents", 10000)
    
print(f"Documents: {len(documents)}")

# %%
llama_documents = [
        Document(
            text=doc["content"],
            metadata=doc["metadata"]
        )
        for doc in documents
    ]
print(len(llama_documents))

node_parser = SimpleNodeParser()
nodes = node_parser.get_nodes_from_documents(llama_documents)

print(len(nodes))

# %% [markdown]
# ## build index in batches

# %%
batch_size = 5000
index = None

print(f"Start indexing at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

total_start_time = time.time()
for i in range(0, len(nodes), batch_size):
    start_time = time.time()
    batch = nodes[i:i + batch_size]
    size_in_bytes = asizeof.asizeof(batch)
    print(f"Batch {i//batch_size + 1} - start time: {datetime.now().strftime('%H:%M:%S')} - size: {format_bytes(size_in_bytes)}")
    
    if i == 0:
        index = VectorStoreIndex(batch)
    else:
        index.insert_nodes(batch)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Batch {i//batch_size + 1} - Indexing time: {format_seconds(elapsed_time)}")
   
end_time = time.time()
elapsed_time = end_time - total_start_time
print(f"Stop indexing at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Total indexing time: {format_seconds(elapsed_time)}")

# %% [markdown]
# ## Test query

# %%
query_engine = index.as_query_engine(
    response_mode="no_text",
    similarity_top_k=10
    )

# %%
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

def print_results(query, results):
    print(f"query: {query}")
    for idx, doc in enumerate(results, start=1):
        print(f"Document {idx}: {doc['title']}")
        # print(f"Content: {doc['content'][:200]}")
        print(f"File path: {doc['file_path']}")
        print(f"Score: {doc['score']}")
        print()

# %%
query = "What is the impact of the GDPR on me?"
response = query_engine.query(query)
results = format_response(response)
print_results(query, results)


# %% [markdown]
# ## write to file

# %%
print("writing index to file")
storage_file = "llamaindex_stella"
index.storage_context.persist(storage_file)


