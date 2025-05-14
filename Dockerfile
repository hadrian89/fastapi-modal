FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./app ./app

# Set the entrypoint
CMD ["uvicorn", "app.main-local:app", "--host", "0.0.0.0", "--port", "8000"]

# docker build -t fastapi-app-local-modal .
# docker run -p 8000:8000 fastapi-app-local-modal