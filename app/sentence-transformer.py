from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
from sentence_transformers import SentenceTransformer

app = FastAPI()

# Load sentiment-analysis model from local directory
MODEL_PATH = "./app/models/all-MiniLM-L6-v2"
classifier = SentenceTransformer(MODEL_PATH)
# end to previous model

class TextInput(BaseModel):
    text: str

class TextInputTransformer(BaseModel):
    sentences: List[str]

@app.get("/")
def root():
    return {"message": "Hugging Face Model Running with FastAPI"}

@app.post("/predict")
async def predict(input: TextInput):
    result = classifier(input.text)
    return result

@app.post("/embed")
async def get_embeddings(input_data: TextInputTransformer):
    embeddings = classifier.encode(input_data.sentences, convert_to_numpy=True)
    return {"embeddings": embeddings.tolist()}

# uvicorn app.main-local:app --reload --port 8000  