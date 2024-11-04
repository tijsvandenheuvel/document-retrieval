import os
import time
from opensearchpy import OpenSearch
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyPDF2 import PdfReader
from docx import Document as DocxDocument

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

# Ensure index exists
if not opensearch_client.indices.exists(index=INDEX_NAME):
    opensearch_client.indices.create(index=INDEX_NAME, body={
        "mappings": {
            "properties": {
                "content": {"type": "text"},
                "file_path": {"type": "keyword"},
            }
        }
    })

# Text extraction functions
def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = "".join(page.extract_text() for page in reader.pages)
        return text
    except Exception as e:
        print(f"Error extracting text from PDF {file_path}: {e}")
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
    elif file_path.endswith(".docx"):
        content = extract_text_from_word(file_path)
    else:
        print(f"Unsupported file type: {file_path}")
        return

    # Index the document in OpenSearch
    document = {
        "content": content,
        "file_path": file_path
    }
    opensearch_client.index(index=INDEX_NAME, body=document)

# Watchdog event handler
class DocumentHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and (event.src_path.endswith(".pdf") or event.src_path.endswith(".docx")):
            print(f"Indexing modified document: {event.src_path}")
            index_document(event.src_path)

    def on_created(self, event):
        if not event.is_directory and (event.src_path.endswith(".pdf") or event.src_path.endswith(".docx")):
            print(f"Indexing new document: {event.src_path}")
            index_document(event.src_path)

# Monitor folder for new or modified documents
def monitor_folder(directory):       
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
    observer.join()

# Start monitoring (replace 'path/to/your/folder' with your folder path)
monitor_folder("documents")