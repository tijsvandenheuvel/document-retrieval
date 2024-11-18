from flask import Flask, request, render_template, jsonify, send_file, url_for
from opensearchpy import OpenSearch
import os
import subprocess
import json
from search_history_db import init_db, insert_search_history, fetch_search_history, fetch_history_entry, get_db, close_db, clear_database, get_search_history
import jinja2

app = Flask(__name__)

# url format helper
@app.template_filter('escape_single_quotes')
def escape_single_quotes(value):
    if isinstance(value, str):
        return value.replace("'", "\\'")
    return value

# SQLite query history database 

init_db()

@app.teardown_appcontext
def close_database_connection(exception):
    close_db()
        
@app.route('/clear-database', methods=['GET'])
def clear_db_route():        
    success = clear_database()
    if success:
        return jsonify({"message": "Database cleared successfully!"}), 200
    else:
        return jsonify({"message": "Failed to clear the database."}), 500

@app.route('/search-history', methods=['GET'])
def get_all_rows_route():
    data = get_search_history()
    if data is not None:
        return jsonify(data), 200
    else:
        return jsonify({"message": "Failed to retrieve data."}), 500

# OpenSearch document database

INDEX_NAME = 'documents'

opensearch_client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    #http_auth=('admin', 'admin'),  # Replace with your OpenSearch credentials
    #use_ssl=False,
    #verify_certs=False
)

# Routes

@app.route("/", methods=["GET"])
def home():
    history = fetch_search_history()
    return render_template("index.html", history=history)

@app.route('/documents')
def show_documents():
    try:
        documents = []
        response = opensearch_client.search(
            index=INDEX_NAME,
            body={"query": {"match_all": {}}},
            scroll='2m',
            size=100
        )
        scroll_id = response['_scroll_id']
        documents.extend(response['hits']['hits'])

        while len(response['hits']['hits']):
            response = opensearch_client.scroll(scroll_id=scroll_id, scroll='2m')
            scroll_id = response['_scroll_id']
            documents.extend(response['hits']['hits'])
        
        # Group documents by folder
        folder_map = {}
        for doc in documents:
            file_path = doc["_source"]["file_path"]
            folder = file_path.split("documents/")[-1]
            folder = "/".join(folder.split("/")[:-1])  # Remove the file name part
            file_data = {
                "title": file_path.split("/")[-1],
                "file_path": file_path,
                "content": doc["_source"]["content"][:200]
            }
            folder_map.setdefault(folder, []).append(file_data)

        # Transform folder_map into a list of dictionaries
        grouped_results = [
            {
                "folder": folder,
                "documents": files,
                "count": len(files)
            }
            for folder, files in sorted(folder_map.items())
        ]
        
        total_documents = len(documents)

        return render_template('documents.html', folders=grouped_results, total_documents=total_documents)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
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
                "fields": ["content"]  # check the query against the content
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
        result_titles = [result["title"] for result in results]   
            
        # Save search to history
        insert_search_history(query, results, result_titles)

        # Update history
        history = fetch_search_history()
        
        return render_template("index.html", query=query, results=results, history=history)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# New endpoint to fetch results from history
@app.route("/history/<int:history_id>", methods=["GET"])
def history_results(history_id):
    entry = fetch_history_entry(history_id)
    if entry:
        query, serialized_results, serialized_titles = entry
        results = json.loads(serialized_results)
        # result_titles = json.loads(serialized_titles)
        history = fetch_search_history()
        return render_template("index.html", query=query, results=results, history=history)
    return jsonify({"error": "History entry not found"}), 404
    
# open local files

DOCUMENTS_DIR = "../documents/"

@app.route("/open/<path:file_path>", methods=["GET"])
def open_file(file_path):
    
    # TODO: handle directory structure, right now only the document title gets passed along
    
    # Construct full path
    full_path = os.path.join(DOCUMENTS_DIR, file_path)
    #print(full_path)
    
    if not os.path.exists(full_path):
        return jsonify({"success": False, "error": "File not found"}), 404

    # Open the file with the default application
    try:
        if os.uname().sysname == "Darwin":  # macOS
            subprocess.run(["open", full_path])
        elif os.name == "nt":  # Windows
            os.startfile(full_path)
        else:  # Linux or others
            subprocess.run(["xdg-open", full_path])
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
# download file

@app.route("/download/<path:file_path>", methods=["GET"])
def download_file(file_path):
    
    # Construct full path
    full_path = os.path.join(DOCUMENTS_DIR, file_path)
    #print(full_path)
    
    if not os.path.exists(full_path):
        return "File not found", 404

    # Send file for download
    return send_file(full_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)