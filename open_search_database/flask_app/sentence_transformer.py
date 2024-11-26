from sentence_transformers import SentenceTransformer

# Initialize model
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(text):
    return model.encode(text).tolist()