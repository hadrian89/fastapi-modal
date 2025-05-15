# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for machine learning packages (optional, but necessary for torch or tensorflow)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pip and virtualenv
RUN pip install --upgrade pip
RUN pip install virtualenv

# Create and activate a virtual environment
RUN python3 -m venv /opt/venv

# Set the virtual environment as the default Python environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirement files and install dependencies in the virtual environment
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script needed to download the model
COPY download-modal.py .

# Run model download inside Docker image
RUN python download-modal.py

# Expose port 8000
EXPOSE 8000

# Copy the rest of the application code AFTER model download
COPY ./app ./app

# Set the entrypoint to run FastAPI app
CMD ["uvicorn", "app.main-local:app", "--host", "0.0.0.0", "--port", "8000"]

# To build the Docker image:
# docker build -t fastapi-app-local-modal .

# To run the container:
# docker run -p 8000:8000 fastapi-app-local-modal
