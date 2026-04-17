def test_predict_price_success(client):
    """Test successful price prediction."""
    payload = {
        "region": "Yirgacheffe",
        "month": 3,
        "altitude": 1900,
        "rainfall": 120,
        "variety": "Heirloom",
        "processing": "Washed",
        "ecx_grade": 2
    }
    
    response = client.post("/api/v1/price/predict", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "predicted_price_etb" in data
    assert "predicted_price_usd" in data
    assert data["currency_primary"] == "ETB"
    assert data["unit"] == "per kg"
    assert "Grade 2" in data["ecx_grade_label"]

def test_predict_price_validation_error(client):
    """Test price prediction input validation (Pydantic schema)."""
    # Missing required 'region' and 'month'
    payload = {
        "altitude": 1900
    }
    
    response = client.post("/api/v1/price/predict", json=payload)
    assert response.status_code == 422 # FastAPI validation error
