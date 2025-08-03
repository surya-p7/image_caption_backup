
import pytest
from fastapi.testclient import TestClient
from main import app, HTTPException
import io
from PIL import Image

client = TestClient(app)

def test_read_root():
    """Test that the homepage loads correctly."""
    response = client.get("/")
    assert response.status_code == 200
    assert "AI Image Captioning" in response.text

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_upload_image():
    """Test the image upload and captioning endpoint."""
    # Create a dummy image in memory
    buffer = io.BytesIO()
    image = Image.new('RGB', (100, 100), 'blue')
    image.save(buffer, format='PNG')
    buffer.seek(0)

    # When the API key is valid, we expect a successful response
    # Note: This test makes a live API call to Gemini
    response = client.post(
        "/upload-image/",
        files={"file": ("test.png", buffer, "image/png")}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "original_caption" in data
    assert "improved_caption" in data
    assert "provider" in data and data["provider"] == "gemini"

    # Check that the caption is not a demo/error message
    assert "demo" not in data["original_caption"].lower()
    assert "error" not in data["original_caption"].lower()

def test_upload_invalid_file_type():
    """Test uploading a file that is not an image."""
    # Create a dummy text file
    buffer = io.BytesIO(b"this is not an image")
    response = client.post(
        "/upload-image/",
        files={"file": ("test.txt", buffer, "text/plain")}
    )
    assert response.status_code == 400
    assert "File must be an image" in response.text

def test_bad_api_key(monkeypatch):
    """Test the server's response when the Gemini API key is invalid."""
    # Simulate an API error by mocking the content generation method
    async def mock_generate_content(*args, **kwargs):
        raise HTTPException(status_code=500, detail="Gemini API call failed: The API key is invalid")

    monkeypatch.setattr("main.GeminiService._generate_content", mock_generate_content)

    # Create a dummy image for the request
    buffer = io.BytesIO()
    Image.new('RGB', (10, 10)).save(buffer, 'PNG')
    buffer.seek(0)

    response = client.post(
        "/upload-image/",
        files={"file": ("test.png", buffer, "image/png")}
    )

    assert response.status_code == 500
    data = response.json()
    assert "Gemini API call failed" in data["detail"]