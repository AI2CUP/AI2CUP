def test_health_check(client):
    """Test the /api/v1/health endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "models" in data
    assert "price" in data["models"]
    assert "quality" in data["models"]
