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

@pytest.mark.skip(reason="Skipping due to Gemini demo mode")
def test_upload_image():
    """Test the image upload and captioning endpoint."""
    # This test is skipped in demo mode to prevent API calls
    pass

@pytest.mark.skip(reason="Skipping due to Gemini demo mode")
def test_bad_api_key(monkeypatch):
    """Test the server's response when the Gemini API key is invalid."""
    # This test is skipped as we're using demo mode
    pass

def test_upload_invalid_file_type():
    """Test uploading a file that is not an image."""
    # Create a dummy text file
    response = client.post(
        "/upload-image/",
        files={"file": ("test.txt", io.BytesIO(b"not an image"), "text/plain")},
        data={"language": "en"}
    )
    assert response.status_code == 400
    assert "File must be an image" in response.text