import os
import time
from opensearchpy import OpenSearch
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from db_sqlite import initialize_database, log_event_to_db
from db_opensearch import generate_embeddings
from urllib.request import urlopen
from io import BytesIO

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
        http_auth=auth,
        # use_ssl=True,
        # verify_certs=False,
        # ssl_show_warn=False
    )
    return client

credentials = load_credentials('credentials.txt')
opensearch_client = configure_opensearch_client(credentials)

index_body = {
    "settings": {
        "index": {
            "knn": True  # Enable k-NN for the index
        }
    },
    "mappings": {
        "properties": {
            "content": {
                "type": "text"
            },
            "content_vector": {
                "type": "knn_vector",
                "dimension": 384  # Match embedding dimension of the model
            },
            "file_path": {
                "type": "keyword"
            }
        }
    }
}

# ACHTUNG ACHTUNG: DELETING THE INDEX !!!
opensearch_client.indices.delete(index=INDEX_NAME)

if not opensearch_client.indices.exists(index=INDEX_NAME):
    opensearch_client.indices.create(index=INDEX_NAME, body=index_body)
    
# SQLite configuration
db_conn = initialize_database()

# Text extraction functions
def extract_text_from_pdf(file_path):
    try:
        # First attempt: Directly read the file
        reader = PdfReader(file_path)
        text = "".join(page.extract_text() or "" for page in reader.pages)
        return text
    except Exception as e:
        print(f"Direct read failed for {file_path}: {e}")

    try:
        # Second attempt: Read the file as a URL stream
        full_file_path = os.path.abspath(file_path)
        pdf_url = f"file://{full_file_path}"
        pdf_file = urlopen(pdf_url).read()
        pdf_bytes_stream = BytesIO(pdf_file)
        reader = PdfReader(pdf_bytes_stream)
        text = "".join(page.extract_text() or "" for page in reader.pages)
        return text
    except Exception as e:
        print(f"URL stream read failed for {file_path}: {e}")
        return ""

def extract_text_from_word(file_path):
    try:
        doc = DocxDocument(file_path)
        text = "\n".join(para.text for para in doc.paragraphs)
        return text
    except Exception as e:
        print(f"Error extracting text from Word document {file_path}: {e}")
        return ""

# Indexing function
def index_document(file_path):
    
    if file_path.endswith(".pdf"):
        content = extract_text_from_pdf(file_path)
        vector = generate_embeddings(content)
    elif file_path.endswith(".docx"):
        content = extract_text_from_word(file_path)
        vector = generate_embeddings(content)
    else:
        print(f"Unsupported file type: {file_path}")
        content = ""
        vector = []

    # Index the document in OpenSearch
    document = {
        "content": content,
        "content_vector": vector,
        "file_path": file_path
    }
    doc_id = file_path
    opensearch_client.index(index=INDEX_NAME, id=doc_id, body=document)
    print(f"indexed document: {file_path}")
    
def delete_document(file_path):
        try:
            opensearch_client.delete(
                index=INDEX_NAME,
                id=file_path  # Assuming the file path is used as the document ID
            )
            print(f"Deleted document: {file_path}")
        except Exception as e:
            print(f"Error deleting document: {e}")
            
def check_and_index_existing_documents(directory):
    """
    Check if all documents in the folder are indexed.
    Index any documents that are not already indexed.
    """
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                # Check if document is already indexed
                response = opensearch_client.get(index=INDEX_NAME, id=file_path, ignore=404)
                if response.get('found', False):
                    print(f"Document already indexed: {file_path}")
                else:
                    log_event_to_db("created", file_path)
                    index_document(file_path)
            except Exception as e:
                print(f"Error checking/indexing document {file_path}: {e}")


# Watchdog event handler
class DocumentHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        log_event_to_db("modified", event.src_path)
        index_document(event.src_path)

    def on_created(self, event):
        self.on_modified(event)  # Treat creation as an indexing event
        log_event_to_db("created", event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        log_event_to_db("deleted", event.src_path)
        delete_document(event.src_path)
            
def monitor_folder(directory):
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    # Check and index existing documents in the folder
    check_and_index_existing_documents(directory)
    
    event_handler = DocumentHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    print(f"Monitoring directory: {directory}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    # finally:
    #     close_db()
    observer.join()

monitor_folder("../documents")