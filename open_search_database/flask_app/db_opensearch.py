from opensearchpy import OpenSearch
import os

INDEX_NAME = 'documents'

opensearch_client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    #http_auth=('admin', 'admin'),  # Replace with your OpenSearch credentials
    #use_ssl=False,
    #verify_certs=False
)

def parse_response(response, search_type):
    results = [
        {
            "title": hit["_source"]["file_path"].split('/')[-1],
            "file_path": hit["_source"]["file_path"],
            "content": hit["_source"]["content"][:200],
            "score": hit["_score"],
            "search_type": search_type
        } for hit in response["hits"]["hits"]
    ]
    return results

def search_by_keyword(query, search_type):
    query_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["content"]
            }
        }
    }
    response = opensearch_client.search(index=INDEX_NAME, body=query_body)
    return parse_response(response, search_type)

def search_by_vector(query_vector, search_type):
    query_body = {
        "query": {
            "knn": {
                "content_vector": {
                    "vector": query_vector,
                    "k": 10
                }
            }
        }
    }
    response = opensearch_client.search(index=INDEX_NAME, body=query_body)
    return parse_response(response, search_type)
    

# def search_documents(query, search_type):
#     if search_type == 'keyword':
#         return search_by_keyword(query)
#     elif search_type == 'vector':
#         # Convert the query to a vector using your preferred method (e.g., SentenceTransformer)
#         query_vector = convert_query_to_vector(query)
#         return search_by_vector(query_vector)
#     else:
#         raise ValueError("Invalid search type. Choose 'keyword' or 'vector'.")

def fetch_all_documents():
    # Fetch all documents from OpenSearch with scrolling
    documents = []
    response = opensearch_client.search(
        index=INDEX_NAME,
        body={"query": {"match_all": {}}},
        scroll='2m',  # Scroll context to fetch large data sets
        size=100  # Number of documents per request
    )
    scroll_id = response.get('_scroll_id')
    documents.extend(response['hits']['hits'])

    # Continue scrolling until no more documents are returned
    while response['hits']['hits']:
        response = opensearch_client.scroll(scroll_id=scroll_id, scroll='2m')
        scroll_id = response.get('_scroll_id')
        documents.extend(response['hits']['hits'])
        
    return documents

def process_documents(documents):
    # Group documents by folder
        folder_map = {}
        unique_id = 0
        for doc in documents:
            file_path = doc["_source"]["file_path"]
            folder = file_path.split("documents/")[-1]
            folder = "/".join(folder.split("/")[:-1])
            # folder = os.path.dirname(file_path.replace("documents/", ""))
            unique_id += 1  # Increment unique ID for each document
            file_data = {
                "unique_id": unique_id,  # Assign unique ID
                "title": os.path.basename(file_path),  # Get file name
                "file_path": file_path,
                "content": doc["_source"]["content"][:200]  # Limit snippet size
            }
            folder_map.setdefault(folder, []).append(file_data)

        # Convert folder_map to a list of dictionaries for rendering
        grouped_results = [
            {"folder": folder, "documents": files, "count": len(files)}
            for folder, files in sorted(folder_map.items())
        ]
        
        return grouped_results