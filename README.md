# 🎯 Event Recommendation System with Explainable AI

## 🚀 Features
- Personalized event recommendations
- Explainable AI (XAI) using feature contributions
- Hybrid filtering approach
- Modern React UI

## 🧠 Tech Stack
- Frontend: React + Tailwind
- Backend: Flask (Python)
- ML: Scikit-learn + SHAP

## 📊 How It Works
- Uses user preferences (interest, location, budget)
- Generates feature-based scores
- Provides explanation for each recommendation

## ▶️ Run Locally
1️⃣ Clone Repository

```bash
git clone https://github.com/OmKuthe/XAI
cd XAI

2️⃣ Backend Setup
cd ml-service
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate (Mac/Linux)
pip install -r requirements.txt
python app.py

Backend runs on:
http://127.0.0.1:5000

3️⃣ Frontend Setup
cd frontend
npm install
npm run dev

```