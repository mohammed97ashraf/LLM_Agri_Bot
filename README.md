# LLM Agri Bot – Custom Chatbot with OpenAI & HuggingFace

A personalized chatbot for agriculture queries that integrates OpenAI GPT for text and HuggingFace for voice interactions.

## Features
- **Text chat** – Ask any agriculture-related question.
- **Voice input** – Speak naturally and get responses.
- **Smart responses** – Powered by OpenAI’s language models.

## Architecture
- **Backend**: Flask (Python)
- **Text Model**: OpenAI GPT-3.5/4 via API
- **Voice Processing**: HuggingFace Transformers (e.g., Wav2Vec2 for STT)
- **Frontend**: HTML/CSS/JS (see `Sample_image/voicechat_web.png`)

## Prerequisites
- Python 3.8+
- OpenAI API key ([get one](https://platform.openai.com/api-keys))
- HuggingFace API token ([get one](https://huggingface.co/settings/tokens))

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/mohammed97ashraf/LLM_Agri_Bot.git
   cd LLM_Agri_Bot
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory (never commit this file):
   ```env
   OPENAI_API_KEY=sk-your-openai-key
   HUGGINGFACE_API_KEY=hf_your_huggingface_token
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Open your browser and go to `http://127.0.0.1:5000`.

3. Type your question (e.g., "What crops grow best in loamy soil?") or click the microphone icon to speak.

### Example Interactions
- **User**: What is the ideal pH for tomato plants?
  **Bot**: The ideal soil pH for tomatoes is between 6.0 and 6.8.
- **User** (voice): How to control aphids organically?
  **Bot**: Use neem oil spray or introduce ladybugs into your garden.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'flask'` | Run `pip install -r requirements.txt` |
| `No module named 'flask_cors'` | Run `pip install flask-cors` and add it to requirements.txt |
| CORS errors in browser | Ensure Flask-CORS is installed and app is configured with `CORS(app)` |
| API key errors | Verify `.env` file exists with correct keys |
| Voice not working | Voice feature is under development; check back soon |

## Project Structure
```
LLM_Agri_Bot/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not committed)
├── Sample_image/       # Screenshots and design assets
├── README.md           # This file
├── CONTRIBUTING.md     # Contribution guidelines
└── CHANGELOG.md        # Version history
```

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute.

## License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- OpenAI for language models
- HuggingFace for voice processing models
- Flask community

## Future Improvements
- Complete voice input feature with real STT model integration
- Add WebSocket support for real-time streaming
- Implement user authentication
- Expand agriculture knowledge base with retrieval-augmented generation (RAG)
- Add support for multiple languages