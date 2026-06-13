# LLM Agri Bot API Documentation

This document provides comprehensive details for the LLM Agri Bot API endpoints. The API allows you to interact with the chatbot via text and voice, returning agriculture-related responses powered by OpenAI and HuggingFace models.

## Base URL

All API endpoints are relative to the base URL of the deployed Flask application. For local development, the base URL is:

```
http://127.0.0.1:5000
```

## Authentication

All API requests require an API key and a HuggingFace token, which are configured on the server side via environment variables. Client requests do not need to pass these keys; they are stored securely in the backend.

## Endpoints

### 1. Text Chat

Send a text message and receive a response.

**Endpoint:** `POST /chat`

**Request Body (JSON):**

| Field    | Type   | Required | Description                                      |
|----------|--------|----------|--------------------------------------------------|
| `message`| string | Yes      | The user's text query related to agriculture.    |

**Example Request:**

```bash
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the best time to plant wheat in India?"}'
```

**Success Response (200 OK):**

```json
{
  "response": "The best time to plant wheat in India is during the Rabi season, typically from October to December. The crop requires cool temperatures during the growing period and warm temperatures at harvest.",
  "confidence": 0.94
}
```

**Error Responses:**

- **400 Bad Request:** If `message` is missing or empty.
  ```json
  {
    "error": "Message field is required and cannot be empty."
  }
  ```
- **500 Internal Server Error:** If the OpenAI API call fails.
  ```json
  {
    "error": "Failed to generate response due to server error."
  }
  ```

---

### 2. Voice Input

Upload an audio file containing speech, and receive a text transcript along with an AI-generated response.

**Endpoint:** `POST /voice`

**Request (multipart/form-data):**

| Field   | Type | Required | Description                                   |
|---------|------|----------|-----------------------------------------------|
| `audio` | File | Yes      | Audio file (WAV, MP3, or OGG) with speech.    |

**Example Request:**

```bash
curl -X POST http://127.0.0.1:5000/voice \
  -F "audio=@question.wav"
```

**Success Response (200 OK):**

```json
{
  "transcription": "What is the best time to plant wheat in India?",
  "response": "The best time to plant wheat in India is during the Rabi season, typically from October to December.",
  "audio_response": "/static/responses/response_12345.wav"
}
```

The `audio_response` field is a relative URL to a WAV file containing a spoken version of the response (synthesized using a text-to-speech model).

**Error Responses:**

- **400 Bad Request:** No audio file provided or unsupported format.
  ```json
  {
    "error": "Audio file is required. Supported formats: WAV, MP3, OGG."
  }
  ```
- **500 Internal Server Error:** If HuggingFace STT/TTS or OpenAI fails.
  ```json
  {
    "error": "Voice processing failed. Please try again later."
  }
  ```

---

### 3. Health Check

Verify that the API is running and healthy.

**Endpoint:** `GET /health`

**Example Request:**

```bash
curl http://127.0.0.1:5000/health
```

**Success Response (200 OK):**

```json
{
  "status": "healthy",
  "models": {
    "text": "OpenAI GPT-3.5",
    "stt": "Wav2Vec2-Large-960h",
    "tts": "Tacotron2"
  }
}
```

---

## Rate Limiting

Requests are limited to 60 per minute per IP address. Exceeding this limit will result in a **429 Too Many Requests** response:

```json
{
  "error": "Rate limit exceeded. Please wait and try again."
}
```

## Error Codes Summary

| Status Code | Meaning                    |
|-------------|----------------------------|
| 200         | Success                    |
| 400         | Bad Request (invalid input)| 
| 429         | Rate limit exceeded        |
| 500         | Internal server error      |

## FAQ

**Q: Can I use this API without an OpenAI key?**  
A: No, the server requires a valid OpenAI API key configured in the environment variable `OPENAI_API_KEY`.

**Q: Are there any costs for using the API?**  
A: Usage of the API incurs costs from OpenAI and HuggingFace based on your own keys. The bot itself is free and open-source.

**Q: How long are audio responses stored?**  
A: Generated audio files are stored temporarily for 15 minutes and then deleted automatically.

**Q: Is the API suitable for production use?**  
A: This API is provided as-is for demonstration purposes. For production, consider adding authentication, HTTPS, and scaling the backend.