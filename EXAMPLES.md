# LLM Agri Bot – Usage Examples

This document provides practical examples of interacting with the LLM Agri Bot for common agricultural tasks. Use these as a guide to get the most out of the chatbot.

## Prerequisites
Make sure you have completed the [Installation](README.md#installation) steps and have your API keys set up.

## 1. Text Chat Examples

### Example 1: Crop Disease Diagnosis
```
User: My tomato plants have yellow leaves with brown spots. What could be the problem?
Bot: Yellow leaves with brown spots on tomatoes could indicate early blight (Alternaria solani) or bacterial spot. Early blight typically starts on lower leaves and spreads upward. Bacterial spot causes water‑soaked lesions that turn brown. I recommend removing affected leaves, improving air circulation, and applying a copper‑based fungicide if symptoms persist. For a precise diagnosis, please provide a photo or describe the pattern of spots.
```

### Example 2: Soil Management
```
User: What is the ideal pH range for growing potatoes?
Bot: Potatoes prefer slightly acidic soil with a pH between 5.0 and 6.0. A pH below 4.8 may cause aluminum toxicity, while above 6.5 increases the risk of common scab. Test your soil and amend with sulfur to lower pH or lime to raise it. Also ensure good drainage and organic matter content.
```

### Example 3: Irrigation Scheduling
```
User: How often should I water wheat in a semi‑arid region?
Bot: Watering frequency depends on soil type, growth stage, and weather. For wheat in a semi‑arid region: during germination, keep the top 2 inches moist; after tillering, water every 7–10 days to maintain soil moisture at 50–60% field capacity. Use drip irrigation to conserve water. Avoid over‑watering, which can cause root rot. Check local evapotranspiration data for precise scheduling.
```

### Example 4: Fertilizer Recommendation
```
User: My corn field shows nitrogen deficiency – pale green leaves and stunted growth. What should I apply?
Bot: Corn with nitrogen deficiency needs immediate side‑dressing with urea (46‑0‑0) at 50–100 kg/ha, depending on soil test results. Apply when plants are knee‑high and water immediately to incorporate. Follow up with a balanced NPK (e.g., 20‑10‑10) after 2 weeks. Avoid excessive nitrogen to prevent lodging.
```

## 2. Voice Interaction Examples

### Example 5: Using Voice Input for Hands‑Free Queries
1. Click the microphone button on the web interface.
2. Speak clearly: *“What is the best pesticide for aphids on okra?”*
3. The bot will process your speech via HuggingFace’s Wav2Vec2 and return a text response.

### Example 6: Multilingual Voice Query
If your system is configured with a multilingual model, try:
- *“¿Cómo controlar el mildiú polvoso en las uvas?”* (Spanish)
- *“कपास में गुलाबी सुंडी का उपचार क्या है?”* (Hindi)

The bot will attempt to transcribe and respond in the same language.

## 3. Integration with External Tools

### Example 7: Using the Bot as a REST API
Start the Flask backend, then send a POST request:
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How to manage weeds in onion fields?"}'
```
Response:
```json
{
  "response": "Weed management in onions: use pre‑emergence herbicides like pendimethalin, followed by hand‑weeding or inter‑cultivation. Mulching with straw can also suppress weeds. Avoid deep tillage that brings weed seeds to the surface."
}
```

### Example 8: Sending Voice Data via API
```bash
curl -X POST http://localhost:5000/voice \
  -F "audio=@recording.wav" \
  -F "language=en"
```
Returns the transcribed text and the bot’s answer.

## 4. Customization Examples

### Example 9: Adding a New Crop Knowledge Base
Edit `crop_data.json` (if present) to include:
```json
{
  "crop": "quinoa",
  "scientific_name": "Chenopodium quinoa",
  "growing_season": "cool season",
  "water_needs": "moderate",
  "common_pests": ["aphids", "leaf miners"]
}
```
Then restart the bot. The model will incorporate this information into its responses.

### Example 10: Changing the Prompt Tone
In the backend code, modify the system prompt:
```python
system_prompt = "You are a helpful agricultural advisor. Provide concise, actionable advice."
```
Save and restart. The bot will now give shorter answers.

## Troubleshooting
- **No response from voice**: Ensure your microphone is enabled and the HuggingFace token is valid.
- **Irrelevant answers**: Refine your query or adjust the OpenAI temperature parameter.
- **API rate limits**: Check your OpenAI/HuggingFace usage dashboard and upgrade your plan if needed.

For further help, open an issue on the repository or refer to the [CONTRIBUTING.md](CONTRIBUTING.md) guide.