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
| `openai.error.AuthenticationError` | Check your `OPENAI_API_KEY` in `.env` – make sure it’s valid |
| HuggingFace voice input not working | Ensure your `HUGGINGFACE_API_KEY` has the correct permissions and audio device is accessible |
| `ImportError: cannot import name '...'` | Update dependencies: `pip install --upgrade -r requirements.txt` |

## Security
- **Never hardcode API keys** – always use environment variables or `.env` files.
- The `.env` file is ignored by Git if you have a `.gitignore`. If not, add one immediately.

## License
[Add your license here]

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).