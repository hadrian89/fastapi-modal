from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

app = FastAPI()

# Load model from local directory
MODEL_PATH = "./app/models/distilbert-base-uncased-finetuned-sst-2-english/models--distilbert-base-uncased-finetuned-sst-2-english/snapshots/714eb0fa89d2f80546fda750413ed43d93601a13"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, local_files_only=True)
classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

class TextInput(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Hugging Face Model Running with FastAPI"}

@app.post("/predict")
async def predict(input: TextInput):
    result = classifier(input.text)
    return result

# uvicorn app.main-local:app --reload --port 8000  