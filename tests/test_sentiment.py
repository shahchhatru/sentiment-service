from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_positive_sentiment():
    response = client.post("/analyze", json={"text": "I love this!"})
    assert response.status_code == 200
    result = response.json()
    assert "result" in result
    assert isinstance(result["result"], list)
    assert any("label" in item for item in result["result"])

def test_negative_sentiment():
    response = client.post("/analyze", json={"text": "I hate this!"})
    assert response.status_code == 200
    result = response.json()
    assert "result" in result
    assert isinstance(result["result"], list)
    assert any("label" in item for item in result["result"])

def test_empty_text():
    response = client.post("/analyze", json={"text": ""})
    # Either make your app return a 400/422 or handle this test accordingly
    assert response.status_code == 200
    result = response.json()
    assert "result" in result
    assert isinstance(result["result"], list)
