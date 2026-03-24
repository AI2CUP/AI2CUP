# ☕ AI2CUP - AI-Powered Ethiopian Coffee Trade Platform

> **MVP / Demo-Ready** - Predict fair prices, verify bean quality, and connect with trading partners using artificial intelligence.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-orange)

---

## 📋 Features

| Feature | Description |
|---------|-------------|
| **📈 Price Prediction** | ML-powered coffee price prediction based on region, month, altitude, rainfall, and variety |
| **🔬 Quality Detection** | Upload a coffee bean image and get instant quality grade (High / Medium / Low) |
| **🏪 Marketplace** | Browse sellers and buyers with smart matching |

---

## 🗂 Project Structure

```
AI2CUP/
├── backend/
│   ├── main.py                  # FastAPI entry point
│   ├── requirements.txt         # Python dependencies
│   ├── data/
│   │   ├── generate_dataset.py  # Synthetic dataset generator
│   │   └── coffee_prices.csv    # Generated dataset (auto-created)
│   ├── ml/
│   │   ├── price_model.py       # Linear Regression price model
│   │   ├── quality_detector.py  # Image quality analysis (simulated)
│   │   ├── matcher.py           # Buyer/Seller matching engine
│   │   └── trained_model.joblib # Trained model (auto-created)
│   └── routes/
│       ├── price.py             # /predict-price endpoint
│       ├── quality.py           # /analyze-quality endpoint
│       └── match.py             # /match endpoints
├── frontend/
│   ├── index.html               # Main UI
│   ├── script.js                # Frontend logic & API calls
│   └── styles.css               # Premium dark theme
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+** installed
- **pip** package manager

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

The server will automatically:
- ✅ Generate the synthetic coffee price dataset
- ✅ Train the ML model
- ✅ Start serving the API and frontend

### 3. Open the App

Visit **http://localhost:8000** in your browser.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/predict-price` | Predict coffee price |
| `POST` | `/api/analyze-quality` | Analyze coffee image quality |
| `GET` | `/api/match` | Get all marketplace listings |
| `POST` | `/api/match/find` | Find matching counterparties |
| `GET` | `/api/health` | Health check |
| `GET` | `/docs` | Interactive API docs (Swagger) |

### Example: Predict Price

```bash
curl -X POST http://localhost:8000/api/predict-price \
  -H "Content-Type: application/json" \
  -d '{"region": "Yirgacheffe", "month": 10, "altitude": 1900, "rainfall": 150, "variety": "Heirloom"}'
```

### Example: Analyze Quality

```bash
curl -X POST http://localhost:8000/api/analyze-quality \
  -F "file=@coffee_beans.jpg"
```

---

## 🧠 ML Models

### Price Prediction
- **Algorithm**: Linear Regression (scikit-learn)
- **Features**: Region, Month, Altitude, Rainfall, Variety
- **Dataset**: 1000 synthetic records based on Ethiopian coffee patterns
- **Pipeline**: OneHotEncoder → Linear Regression

### Quality Detection (MVP)
- **Approach**: Image property analysis + simulated scoring
- **Analyzes**: Brightness, color warmth, uniformity
- **Output**: Quality grade (High/Medium/Low) + confidence score
- **Production**: Replace with fine-tuned CNN (ResNet/EfficientNet)

---

## 🛠 Tech Stack

- **Backend**: Python, FastAPI, Uvicorn
- **ML**: scikit-learn, pandas, numpy, joblib
- **Image**: Pillow (PIL)
- **Frontend**: HTML5, Vanilla CSS, Vanilla JavaScript
- **Design**: Dark theme, glassmorphism, responsive

---

## 📝 Notes

- This is an **MVP for demonstration** - not production-ready
- Quality detection uses **simulated analysis** (replace with real CNN for production)
- Dataset is **synthetically generated** (replace with real data)
- CORS is set to allow all origins (restrict in production)

---

## 📜 License

© 2026 AI2CUP - All rights reserved.

Built with ❤️ for Ethiopian coffee farmers and traders.
