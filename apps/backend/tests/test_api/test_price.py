def test_predict_price_success(client):
    """Test successful price prediction."""
    payload = {
        "coffee_type": "Yirgachefe",
        "month": 3,
        "processing": "Washed",
        "ecx_grade": 2,
        "exporter_type": "Commercial",
    }

    response = client.post("/api/v1/price/predict", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "predicted_price_usd" in data
    assert "predicted_price_etb" in data
    assert data["currency_primary"] == "USD"
    assert data["currency_secondary"] == "ETB"
    assert data["unit"] == "per kg"
    assert "Grade 2" in data["ecx_grade_label"]
    assert "HistGradientBoosting" in data["model_info"]
    assert data["predicted_price_usd"] > 0
    assert data["predicted_price_etb"] > 0


def test_predict_price_with_exporter_type(client):
    """Test prediction with exporter_type field."""
    payload = {
        "coffee_type": "Guji",
        "month": 1,
        "processing": "Washed",
        "ecx_grade": 1,
        "exporter_type": "V/Integration",
    }

    response = client.post("/api/v1/price/predict", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["predicted_price_usd"] > 0
    assert data["inputs"]["exporter_type"] == "V/Integration"


def test_predict_price_defaults(client):
    """Defaults for year, week, exporter_type."""
    payload = {
        "coffee_type": "Sidamo",
        "month": 6,
        "processing": "Natural",
        "ecx_grade": 3,
    }

    response = client.post("/api/v1/price/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["inputs"]["exporter_type"] == "Commercial"
    assert data["inputs"]["year"] == 2025
    assert data["inputs"]["week"] is None


def test_predict_price_validation_error(client):
    """Test price prediction input validation."""
    payload = {"coffee_type": "Yirgachefe"}

    response = client.post("/api/v1/price/predict", json=payload)
    assert response.status_code == 422
