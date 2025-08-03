import os
import io
import base64
import random
from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

# --- FastAPI App Initialization ---
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# --- Gemini Service ---
class GeminiService:
    def __init__(self):
        try:
            # Configure the API key and initialize the model once
            api_key=os.getenv("GEMINI_API_KEY")
            # self.model = genai.GenerativeModel('gemini-pro-vision')
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables")
                
            # Configure the API key and initialize the model
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.demo_mode = False
            print("Gemini Service configured successfully.")
        except Exception as e:
            print(f"FATAL: Failed to configure Gemini or load model: {e}")
            self.demo_mode = True

    async def _generate_content(self, prompt: str, image_bytes: bytes) -> str:
        """A unified method to generate content from a prompt and image."""
        if self.demo_mode:
            return "Demo mode is active due to an API configuration error."

        try:
            image = Image.open(io.BytesIO(image_bytes))
            response = self.model.generate_content([prompt, image])
            return response.text.strip()
        except Exception as e:
            error_message = f"Gemini API call failed: {e}"
            print(error_message)
            raise HTTPException(status_code=500, detail=error_message)

    async def caption_image(self, image_bytes: bytes, language: str = "en") -> str:
        prompt = f"Generate a short, descriptive caption in {language} for this image."
        return await self._generate_content(prompt, image_bytes)

    async def improve_caption(self, caption: str, image_bytes: bytes) -> str:
        prompt = f"Refine this caption to be more descriptive and engaging: '{caption}'"
        return await self._generate_content(prompt, image_bytes)

    async def summarize_image(self, image_bytes: bytes, language: str = "en") -> str:
        prompt = f"Describe this image in one paragraph in {language}."
        return await self._generate_content(prompt, image_bytes)

# --- Image Captioning Service ---
class ImageCaptioningService:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.demo_mode = self.gemini_service.demo_mode

    async def caption_image(self, image_bytes: bytes, language: str = "en") -> str:
        if self.demo_mode:
            return "This is a demo caption. The API key may be missing or invalid."
        return await self.gemini_service.caption_image(image_bytes, language)

    async def improve_caption(self, caption: str, image_bytes: bytes) -> str:
        if self.demo_mode:
            return f"Refined: {caption}. This is a demo improvement."
        return await self.gemini_service.improve_caption(caption, image_bytes)

    async def summarize_image(self, image_bytes: bytes, language: str = "en") -> str:
        if self.demo_mode:
            return "This is a demo summary. The API key may be missing or invalid."
        return await self.gemini_service.summarize_image(image_bytes, language)

# --- App Setup ---
captioning_service = ImageCaptioningService()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.post("/upload-image/")
async def upload_image(
    file: UploadFile = File(...),
    language: str = Form("en"),
    include_summary: bool = Form(False)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        image_bytes = await file.read()
        try:
            Image.open(io.BytesIO(image_bytes)).verify()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image file: {e}")

        initial_caption = await captioning_service.caption_image(image_bytes, language)
        improved_caption = await captioning_service.improve_caption(initial_caption, image_bytes)
        
        summary = None
        if include_summary:
            summary = await captioning_service.summarize_image(image_bytes, language)

        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        return {
            "success": True,
            "original_caption": initial_caption,
            "improved_caption": improved_caption,
            "summary": summary,
            "image_base64": image_base64,
            "filename": file.filename,
            "provider": "gemini",
            "language": language
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"An unexpected error occurred in upload_image: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the image.")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
