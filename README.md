# Welcome to FastAPI with integrated AI modal and deployable code

Welcome to the **FastAPI with integrated AI modal** repository! This repository contains python code to run AI modal from huggingface and help you to understand and explore **How to use custom Modal and deploy using FastAPI**, here you can find two python files main.py which Download and cache model during build and main-local.py which uses model saved in a local directory (./models) to avoid redownloading it in production.

## 🛠️ Prerequisites

Before you start, ensure you have the following installed:
- Python (>=3.10 recommended)
- Jupyter Notebook (optional)
- conda env manager (optional)
- pip package manager
- Git (to clone the repository)

---

## 📥 Setup Instructions

# bind mount a local Hugging Face model

1. Verify Python installation

```bash
python –version
```

2. Install the required packages available in the git repo in a file "requirements.txt. Install all the required packages using the below command.

```bash
pip install -r requirements.txt
```

3. run below command to download modal once, it will download modal and place in `app/modals` directory

```bash
python download-modal.py
```

4. run below command to start server

```bash
uvicorn app.main-local:app --reload --port 8000
```

or if you want to docker file then run below command

```bash
docker build -t fastapi-app-local-modal .
```

```bash
docker run -p 8000:8000 fastapi-app-local-modal
```

Note: If you want to use another modal then you have download it first, and update the path in python code and in docker file.