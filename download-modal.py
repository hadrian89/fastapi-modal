from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = "distilbert-base-uncased-finetuned-sst-2-english"
cache_path = "./app/models/" + model_name

tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_path)
model = AutoModelForSequenceClassification.from_pretrained(model_name, cache_dir=cache_path)
