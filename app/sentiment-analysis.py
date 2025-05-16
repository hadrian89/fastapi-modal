from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import torch.nn.functional as F

app = FastAPI()

# Load sentiment-analysis model from local directory
MODEL_PATH = "./app/models/distilbert-base-uncased-finetuned-sst-2-english/models--distilbert-base-uncased-finetuned-sst-2-english/snapshots/714eb0fa89d2f80546fda750413ed43d93601a13"
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

@app.post("/confidence")
async def predict_sentiment(input: TextInput):
    # Map label IDs to names (like {0: "NEGATIVE", 1: "POSITIVE"})
    id2label = model.config.id2label
    inputs = tokenizer(input.text, return_tensors="pt")

    # Move inputs and model to CPU explicitly
    model.eval()
    with torch.no_grad():
        outputs = model(**{k: v.to("cpu") for k, v in inputs.items()})
        logits = outputs.logits

    probs = F.softmax(logits, dim=1)
    predicted_class_id = torch.argmax(probs, dim=1).item()
    confidence = probs[0][predicted_class_id].item()
    label = id2label[predicted_class_id]

    return {
        "label": label,
        "confidence": round(confidence, 4),
        "class_id": predicted_class_id
    }
    
# uvicorn app.main-local:app --reload --port 8000  