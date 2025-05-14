from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

app = FastAPI()

# Load model from Hugging Face Hub on runtime
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
classifier = pipeline("sentiment-analysis", model=model_name)
# Uncomment the following lines to use a different model
# model_name = "t5-small"
# nlp_pipeline = pipeline("translation_en_to_fr", model=model_name)

class TextInput(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Hugging Face Model Running with FastAPI"}

@app.post("/predict")
async def predict(input: TextInput):
    result = classifier(input.text)
    return result

# uvicorn app.main:app --reload --port 8000  