from flask import Flask, request, render_template, jsonify, send_file
from opensearchpy import OpenSearch
import os
import subprocess

app = Flask(__name__)

INDEX_NAME = 'documents'

# Initialize OpenSearch client
opensearch_client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    #http_auth=('admin', 'admin'),  # Replace with your OpenSearch credentials
    #use_ssl=False,
    #verify_certs=False
)

# Route to render the HTML page
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route('/documents')
def show_documents():
    # Query for all documents
    response = opensearch_client.search(
        index=INDEX_NAME,
        body={
            "query": {
                "match_all": {}
            }
        }
    )

    documents = response['hits']['hits']
    results = [
            {"title": hit["_source"]["file_path"].split('/')[-1],
             "file_path": hit["_source"]["file_path"], 
             "content": hit["_source"]["content"][:200], 
             "score": hit["_score"]
             } for hit in documents]
    return render_template('documents.html', documents=results)


# Route to handle search queries
@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")  # Get query from form data
    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400
    
    # Define the OpenSearch query
    query_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["content"]  # Adjust field names as per your index
            }
        }
    }
    
    # Perform search
    try:
        response = opensearch_client.search(
            index=INDEX_NAME,
            body=query_body
        )
        # Extract results
        hits = response["hits"]["hits"]
        results = [
            {"title": hit["_source"]["file_path"].split('/')[-1],
             "file_path": hit["_source"]["file_path"], 
             "content": hit["_source"]["content"][:200], 
             "score": hit["_score"]
             } for hit in hits]
        return render_template("index.html", query=query, results=results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# open local files

DOCUMENTS_DIR = "../documents/"

@app.route("/open/<path:file_path>", methods=["GET"])
def open_file(file_path):
    # Construct full path
    
    full_path = os.path.join(DOCUMENTS_DIR, file_path)
    
    #full_path = file_path
    
    print(full_path)
    if not os.path.exists(full_path):
        return "File not found", 404

    # Open the file with the default application
    try:
        if os.uname().sysname == "Darwin":  # macOS
            subprocess.run(["open", full_path])
        elif os.name == "nt":  # Windows
            os.startfile(full_path)
        else:  # Linux or others
            subprocess.run(["xdg-open", full_path])
        return f"Opening file: {file_path}"
    except Exception as e:
        return f"Error opening file: {e}", 500
    
# download file

@app.route("/download/<path:file_path>", methods=["GET"])
def download_file(file_path):
    # Construct full path
    full_path = os.path.join(DOCUMENTS_DIR, file_path)
    if not os.path.exists(full_path):
        return "File not found", 404

    # Send file for download
    return send_file(full_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)