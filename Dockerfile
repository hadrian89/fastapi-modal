FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy and install requirements
# Copy requirement files and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
# Copy only the script needed to download the model
# COPY download-sentence-transformer-modal.py .
COPY download-sentiment-analysis-modal.py .

# Run model download inside Docker image
# RUN python download-sentence-transformer-modal.py
RUN python download-sentiment-analysis-modal.py

# Copy the rest of the application code AFTER model download
COPY ./app ./app

# Expose port
# EXPOSE 8000

# Set the entrypoint
# CMD ["uvicorn", "app.sentence-transformer:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "app.sentiment-analysis:app", "--host", "0.0.0.0", "--port", "8000"]

# docker build -t fastapi-app-local-modal .
# docker run -p 8000:8000 fastapi-app-local-modal