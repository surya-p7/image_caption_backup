# 🤖 AI Image Captioning Application

A modern web application that uses AI to generate intelligent captions for uploaded images. The app supports multiple AI providers including OpenAI GPT-4 Vision and Google Gemini for both initial image captioning and caption enhancement.

## 🚀 Features

- **Image Upload**: Drag & drop or click to upload images
- **Multi-AI Support**: Choose between OpenAI GPT-4 Vision and Google Gemini
- **AI Captioning**: Both providers can generate initial image descriptions
- **Caption Enhancement**: Both providers can improve and refine captions
- **Modern UI**: Beautiful, responsive web interface with provider selection
- **Real-time Processing**: Fast API backend with async processing
- **Demo Mode**: Works without API keys using demo responses

## 📋 Prerequisites

- Python 3.8 or higher
- API keys for (optional - demo mode available):
  - [OpenAI](https://platform.openai.com/api-keys)
  - [Google Gemini](https://makersuite.google.com/app/apikey)

## 🛠️ Installation

1. **Clone or download this project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys** (optional):
   - Copy `env_example.txt` to `.env`
   - Add your API keys to the `.env` file:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   - Note: The app works in demo mode without API keys

## 🔑 Getting API Keys

### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an account or sign in
3. Go to [API Keys](https://platform.openai.com/api-keys)
4. Create a new API key
5. Copy the key to your `.env` file

### Google Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key to your `.env` file

## 🚀 Running the Application

1. **Start the server**:
   ```bash
   python main.py
   ```

2. **Open your browser** and go to:
   ```
   http://localhost:8000
   ```

3. **Upload an image** and watch the AI generate captions!

## 📁 Project Structure

```
GANUM/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── env_example.txt      # Example environment variables
├── README.md           # This file
├── templates/
│   └── index.html      # Web interface
├── static/             # Static files (CSS, JS)
└── uploads/            # Uploaded images (auto-created)
```

## 🔧 API Endpoints

- `GET /` - Main web interface
- `POST /upload-image/` - Upload and process image
- `GET /health` - Health check endpoint

## 💡 How It Works

1. **User Uploads Image**: The web interface accepts image uploads via drag & drop or file picker
2. **Provider Selection**: User chooses between OpenAI GPT-4 Vision or Google Gemini
3. **Image Validation**: Server validates file type and size
4. **AI Captioning**: Image is sent to the selected AI provider for initial caption
5. **Caption Enhancement**: Original caption is sent to the same provider for improvement
6. **Result Display**: Both captions are displayed to the user with the image and provider info

## 🎨 Customization

### Changing AI Providers
- **OpenAI Models**: Modify the `model` parameter in the OpenAI API calls in `main.py`
- **Gemini Models**: Change the model name in the `GeminiService` class. For image analysis, use `models/gemini-1.5-pro-vision` (supports images) or `models/gemini-2.0-flash-exp` (supports images)
- **Add New Providers**: Extend the `ImageCaptioningService` class to support additional AI providers

### UI Customization
- Edit `templates/index.html` to modify the web interface
- CSS styles are embedded in the HTML file for easy customization

## 🐛 Troubleshooting

### Common Issues

1. **"API key not configured" error**:
   - Make sure you've created a `.env` file with your API keys
   - Verify the API keys are correct and have proper permissions

2. **"Network error" when uploading**:
   - Check your internet connection
   - Verify the Hugging Face and OpenAI APIs are accessible

3. **Large file uploads fail**:
   - The app limits uploads to 10MB
   - Compress your images or use smaller files

4. **Slow processing**:
   - The first request may be slow as models load
   - Subsequent requests should be faster

### Debug Mode
To run with debug information:
```bash
uvicorn main:app --reload --log-level debug
```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application!

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify your API keys are correctly configured
3. Ensure all dependencies are installed
4. Check the console for error messages

---

**Happy Captioning! 🎉** 