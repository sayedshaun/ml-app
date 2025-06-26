# An Application of Machine Learning
This repository contains an application that uses machine learning models to provide insights about text data. The models are based on the transformers library and are served using a FastAPI and litserve backend. 

## Available Models
- Named Entity Recognition
- Sentiment Analysis
- Question Answering

## Setup
This project requires `python=3.10`

Open terminal and run the command
```bash
git clone https://github.com/sayedshaun/ml-app.git
cd ml-app
code .
```

Active virtual environment and install requirements
```bash
pip install -r requirements.txt
```

## Usage

Create `.env` file and store all of the bellow information
```bash
# urls
DATABASE_URL=sqlite:///sqlite.db
NER_ENDPOINT=http://localhost:8001/ner
QA_ENDPOINT=http://localhost:8001/qa
SENTIMENT_ENDPOINT=http://localhost:8001/sentiment
FRONTEND_URL=http://localhost:3000

# auth
SECRET_KEY=fbbc4ebe47fc6098a1cb13473a26ed77619ec8eb91be520bcdc861c5063cd4f4
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Run ml server
```bash
cd ml && python main.py --port 8000
```

Run backend server
```bash
cd backend && uvicorn main.py --port 8001
```

## Disclaimer
The models used in this project are sourced from the Hugging Face Hub. I do not claim ownership of these models. Any of them can be replaced with alternative models available on Hugging Face as needed. The application is intended to be used for educational purposes and is not intended to be used in production.