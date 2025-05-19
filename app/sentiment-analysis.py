from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import torch.nn.functional as F

app = FastAPI()

# Load sentiment-analysis model from local directory
# MODEL_PATH = "./app/models/distilbert-base-uncased-finetuned-sst-2-english/models--distilbert-base-uncased-finetuned-sst-2-english/snapshots/714eb0fa89d2f80546fda750413ed43d93601a13"
MODEL_PATH = "./app/models/yeniguno/bert-uncased-intent-classification/models--yeniguno--bert-uncased-intent-classification/snapshots/8caf4318fa58f70fe355088687e912622ae83c51"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, local_files_only=True)
# end to previous model

class TextInput(BaseModel):
    text: str
    
@app.get("/")
def root():
    return {"message": "Hugging Face Model Running with FastAPI"}

@app.post("/predict")
async def predict(input: TextInput):
    classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    result = classifier(input.text)
    return result

@app.post("/text-classification")
async def classification(input: TextInput):
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
    result = classifier(input.text)
    return result

@app.post("/confidence")
async def predict_sentiment(input: TextInput):
    # Set to eval mode
    model.eval()
    # Tokenize
    inputs = tokenizer(input.text, return_tensors="pt")

    # Forward pass
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=1)

    # Get prediction
    predicted_class_id = torch.argmax(probs, dim=1).item()
    confidence = probs[0][predicted_class_id].item()

    # Optional: Get class names (from config or define manually if known)
    id2label = model.config.id2label
    label = id2label[predicted_class_id]

    return {
        "label": label,
        "confidence": round(confidence, 4),
        "class_id": predicted_class_id
    }
    
# uvicorn app.sentiment-analysis:app --reload --port 8000  