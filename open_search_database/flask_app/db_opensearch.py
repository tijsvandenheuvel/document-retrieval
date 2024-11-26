from opensearchpy import OpenSearch

INDEX_NAME = 'documents'

opensearch_client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    #http_auth=('admin', 'admin'),  # Replace with your OpenSearch credentials
    #use_ssl=False,
    #verify_certs=False
)

def search_by_keyword(query):
    query_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["content"]
            }
        }
    }
    return opensearch_client.search(index=INDEX_NAME, body=query_body)

def search_by_vector(query_vector):
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
    return opensearch_client.search(index=INDEX_NAME, body=query_body)

def fetch_all_documents():
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