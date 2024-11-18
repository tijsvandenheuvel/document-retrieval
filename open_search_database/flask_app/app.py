from flask import Flask, request, render_template, jsonify, send_file, g
from opensearchpy import OpenSearch
import os
import subprocess
import sqlite3
import json

app = Flask(__name__)

# SQLite history database 

DATABASE = 'search_history.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            result TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()
        
@app.route('/clear-database', methods=['GET'])
def clear_db_route():
    def clear_database():
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            # Get all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]
                # Skip SQLite's internal tables like sqlite_sequence
                if table_name.startswith("sqlite_"):
                    continue
                cursor.execute(f"DELETE FROM {table_name};")
                conn.commit()
            
            conn.close()
            return True
        except Exception as e:
            print(f"Error clearing database: {e}")
            return False
        
    success = clear_database()
    if success:
        return jsonify({"message": "Database cleared successfully!"}), 200
    else:
        return jsonify({"message": "Failed to clear the database."}), 500

@app.route('/search-history', methods=['GET'])
def get_all_rows_route():
    def get_search_history():
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            # Fetch rows from the search_history table
            query = "SELECT id, query, result, timestamp FROM search_history;"
            cursor.execute(query)
            rows = cursor.fetchall()

            # Get column names
            columns = [desc[0] for desc in cursor.description]

            # Convert rows to list of dictionaries
            search_history = [dict(zip(columns, row)) for row in rows]

            conn.close()
            return search_history
        except Exception as e:
            print(f"Error retrieving search history: {e}")
            return None

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
    
    # get query history
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, query, result, timestamp FROM search_history ORDER BY timestamp DESC LIMIT 10')
    history = cursor.fetchall()
    
    return render_template("index.html", history=history)

@app.route('/documents')
def show_documents():
    if not opensearch_client.indices.exists(index=INDEX_NAME):
        results=[]
    else:
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
                # "score": hit["_score"]
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
        
        # Store the query and its results into SQLite
        serialized_results = json.dumps(results)  # Store full results as JSON
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO search_history (query, result) VALUES (?, ?)', (query, serialized_results))
        db.commit()
        
        # update history
        history = cursor.execute('SELECT id, query, result, timestamp FROM search_history ORDER BY timestamp DESC LIMIT 10').fetchall()

        return render_template("index.html", query=query, results=results, history=history)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# New endpoint to fetch results from history
@app.route("/history/<int:history_id>", methods=["GET"])
def history_results(history_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT query, result FROM search_history WHERE id = ?', (history_id,))
    entry = cursor.fetchone()

    if entry:
        query, serialized_results = entry
        results = json.loads(serialized_results)
        history = cursor.execute('SELECT id, query, result, timestamp FROM search_history ORDER BY timestamp DESC LIMIT 10').fetchall()
        return render_template("index.html", query=query, results=results, history=history)
    
    return jsonify({"error": "History entry not found"}), 404
    
# open local files

DOCUMENTS_DIR = "../documents/"

@app.route("/open/<path:file_path>", methods=["GET"])
def open_file(file_path):
    
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