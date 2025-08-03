import requests
import base64
from PIL import Image
import io

def test_gemini_integration():
    """Test the Gemini integration with the main application"""
    
    # Load test image
    with open("BVRIT1.jpg", "rb") as f:
        image_bytes = f.read()
    
    # Convert to base64 for display
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    # Test with Gemini provider
    files = {'file': ('test.jpg', image_bytes, 'image/jpeg')}
    data = {'provider': 'gemini'}
    
    print("Testing Gemini integration...")
    print("Uploading image with Gemini provider...")
    
    try:
        response = requests.post('http://localhost:8000/upload-image/', files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success! Gemini integration working.")
            print(f"Provider: {result.get('provider', 'unknown')}")
            print(f"Original Caption: {result.get('original_caption', 'N/A')}")
            print(f"Enhanced Caption: {result.get('improved_caption', 'N/A')}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_gemini_integration() 