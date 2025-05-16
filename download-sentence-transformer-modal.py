from sentence_transformers import SentenceTransformer
import os

model_name = "all-MiniLM-L6-v2"
cache_path = f"./app/models/{model_name}"

# Create dir if not exists
os.makedirs(cache_path, exist_ok=True)

# Load model and save to local cache_path
model = SentenceTransformer(model_name)
model.save(cache_path)  # This saves everything needed locally
