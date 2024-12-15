from flask import Flask, request, render_template, jsonify, send_file
import os
import subprocess
import json
from db_sqlite import initialize_database, insert_search_history, fetch_search_history, fetch_history_entry, close_db, clear_search_history, get_search_history, fetch_logs
from db_opensearch import search_by_keyword, search_by_vector, fetch_all_documents, process_documents, generate_embeddings
from scenario_script import load_results, get_queries
from llamaindex import search_by_llamaindex, initialize_llamaindex_BGE, initialize_llamaindex_LABSE

app = Flask(__name__)

# url format helper
@app.template_filter('escape_single_quotes')
def escape_single_quotes(value):
    if isinstance(value, str):
        return value.replace("'", "\\'")
    return value

# SQLite query history database 
initialize_database()

query_engine1 = None
query_engine2 = None

def initialize_models():
    pass
    # global query_engine1, query_engine2
    # if query_engine1 is None:
    #     query_engine1 = initialize_llamaindex_BGE()
    # if query_engine2 is None:
    #     query_engine2 = initialize_llamaindex_LABSE()

@app.route('/initialize-models', methods=['POST'])
def initialize_models_route():
    try:
        initialize_models()
        return jsonify({"message": "Models initialized successfully!"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to initialize models: {str(e)}"}), 500


@app.teardown_appcontext
def close_database_connection(exception):
    close_db()
        
@app.route('/clear-search-history', methods=['GET'])
def clear_db_route():        
    success = clear_search_history()
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

@app.route('/logs', methods=['GET'])
def get_logs():
    data = fetch_logs()
    if data is not None:
        return jsonify(data), 200
    else:
        return jsonify({"message": "Failed to retrieve data."}), 500

@app.route("/", methods=["GET"])
def home():
    history = fetch_search_history()
    return render_template("index.html", history=history, json_loads=json.loads)

@app.route("/gpt", methods=["GET"])
def gptindex():
    history = fetch_search_history()
    return render_template("gptindex.html", history=history, json_loads=json.loads)

@app.route('/documents', methods=["GET"])
def show_documents():
    try:
        documents = fetch_all_documents()
        results = process_documents(documents)
        total_documents = len(documents)

        return render_template('documents.html', folders=results, total_documents=total_documents)

    except KeyError as e:
        # Handle missing keys in OpenSearch responses
        error_message = f"Missing key in OpenSearch response: {e}"
        return jsonify({"error": error_message}), 500

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/scenario', methods=["GET"])
def run_scenario():
    results = get_queries()
    return render_template('scenario.html', results=results, json_loads=json.loads)
    
@app.route('/get-results', methods=["POST"])
def get_results():
    results = load_results()
    return render_template('scenario.html', results=results, json_loads=json.loads)

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')  # Get the search query
    search_type = request.form.get('search_type')  # Get the search type (keyword or vector)

    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    try:
        results = []
        
        if search_type == 'keyword':
            results = search_by_keyword(query, search_type)
        elif search_type == 'vector':
            query_vector = generate_embeddings(query)  # Generate embedding for the query
            results = search_by_vector(query_vector, search_type)
        elif search_type == 'llamaindex_bge':
            results = search_by_llamaindex(query, query_engine1, search_type)
        elif search_type == 'llamaindex_labse':
            results = search_by_llamaindex(query, query_engine2, search_type)
        else:
            return jsonify({"error": "Invalid search type"}), 400

        # Save search to history
        result_titles = [result["title"] for result in results]
        
        insert_search_history(query, results, result_titles, search_type)

        # Update history
        history = fetch_search_history()

        return render_template("index.html", query=query, results=results, history=history, json_loads=json.loads)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# New endpoint to fetch results from history
@app.route("/history/<int:history_id>", methods=["GET"])
def history_results(history_id):
    entry = fetch_history_entry(history_id)
    if entry:
        query, serialized_results = entry
        results = json.loads(serialized_results)
        history = fetch_search_history()
        return render_template("index.html", query=query, results=results, history=history, json_loads=json.loads)
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


# code to automatically open the page on startup

# import webbrowser
# from threading import Timer
# def open_browser():
#     webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    # Timer(1, open_browser).start()
    app.run(debug=True)