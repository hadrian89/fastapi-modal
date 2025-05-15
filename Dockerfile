FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirement files and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the script needed to download the model
COPY download-modal.py .

# Run model download inside Docker image
RUN python download-modal.py

# Copy the rest of the application code AFTER model download
COPY ./app ./app

# Set the entrypoint
CMD ["uvicorn", "app.main-local:app", "--host", "0.0.0.0", "--port", "8000"]

# docker build -t fastapi-app-local-modal .
# docker run -p 8000:8000 fastapi-app-local-modal