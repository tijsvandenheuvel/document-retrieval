from opensearchpy import OpenSearch

# OpenSearch configuration
INDEX_NAME = "documents"
def load_credentials(file_path):
    credentials = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                credentials[key] = value
    except Exception as e:
        print(f"An error occurred while reading credentials: {e}")
    return credentials

def configure_opensearch_client(credentials):
    host = credentials.get('host', 'localhost')
    port = int(credentials.get('port', 9200))
    auth = (credentials.get('username'), credentials.get('password'))
    
    client = OpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_auth=auth
    )
    return client

credentials = load_credentials('credentials.txt')
opensearch_client = configure_opensearch_client(credentials)

def search_documents(query):
    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["content"]
            }
        }
    }

    response = opensearch_client.search(index=INDEX_NAME, body=search_body)
    results = response["hits"]["hits"]
    print(f"Found {len(results)} result(s) for query '{query}':\n")
    
    for result in results:
        file_path = result["_source"]["file_path"]
        snippet = result["_source"]["content"][:200]  # Get a short snippet of the content
        score = result["_score"]
        print(f"File Path: {file_path}")
        print(f"Score: {score}")
        print(f"Snippet: {snippet}...\n")
        print("-" * 50)

# Example query
user_query = input("Enter your search query: ")
search_documents(user_query)