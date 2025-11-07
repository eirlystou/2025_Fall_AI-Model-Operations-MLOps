# Iris Species Prediction (FastAPI + Gradio)

This project predicts Iris flower species using a trained ML model. Backend uses FastAPI and Frontend uses Gradio UI.

## Tech Stack
- Python 3.x
- FastAPI backend
- Gradio frontend
- scikit-learn Logistic Regression model
- pickle model storage (.pkl)

## Project Structure
/project  
├─ api.py (FastAPI Backend)  
├─ app_gradio.py (Gradio Frontend)  
├─ train_model.py (train + save iris_model.pkl)  
├─ iris_model.pkl (trained model)  
└─ README.md

## Setup
pip install -r requirements.txt

## Train Model (optional)
python train_model.py

## Run Backend (FastAPI)
uvicorn api:app --reload  
http://127.0.0.1:8000/docs

## Run Frontend (Gradio)
python app_gradio.py  
http://127.0.0.1:7860

## API Endpoint
POST /predict

Request JSON Example:
{"sl":5.1,"sw":3.5,"pl":1.4,"pw":0.2}

Response Example:
{"prediction":0,"proba":[0.98,0.01,0.01]}
