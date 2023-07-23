import os
from flask import Flask, render_template, request, jsonify,url_for
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
import openai
import requests
from gtts import gTTS
import asyncio
import string
import random


#load the api keys from the the .env file
load_dotenv()
#
hugging_face = os.getenv('hugging_face')
open_ai_key = os.getenv('open_ai_key')
#
openai.api_key = open_ai_key

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'webm'}


def get_anwer_openai(quastion):
    completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages = [{"role": "system", "content" : "I want you to act like a helpful agriculture chatbot and help farmers with their query"},
                            {"role": "user", "content" : "Give a Brif Of Agriculture Seasons in India"},
                            {"role":"system","content":"In India, the agricultural season consists of three major seasons: the Kharif (monsoon), the Rabi (winter), and the Zaid (summer) seasons. Each season has its own specific crops and farming practices.\n\n1. Kharif Season (Monsoon Season):\nThe Kharif season typically starts in June and lasts until September. This season is characterized by the onset of the monsoon rains, which are crucial for agricultural activities in several parts of the country. Major crops grown during this season include rice, maize, jowar (sorghum), bajra (pearl millet), cotton, groundnut, turmeric, and sugarcane. These crops thrive in the rainy conditions and are often referred to as rain-fed crops.\n\n2. Rabi Season (Winter Season):\nThe Rabi season usually spans from October to March. This season is characterized by cooler temperatures and lesser or no rainfall. Crops grown during the Rabi season are generally sown in October and harvested in March-April. The major Rabi crops include wheat, barley, mustard, peas, gram (chickpeas), linseed, and coriander. These crops rely mostly on irrigation and are well-suited for the drier winter conditions.\n\n3. Zaid Season (Summer Season):\nThe Zaid season occurs between March and June and is a transitional period between Rabi and Kharif seasons. This season is marked by warmer temperatures and relatively less rainfall. The Zaid crops are grown during this time and include vegetables like cucumber, watermelon, muskmelon, bottle gourd, bitter gourd, and leafy greens such as spinach and amaranth. These crops are generally irrigated and have a shorter growing period compared to Kharif and Rabi crops.\n\nThese three agricultural seasons play a significant role in India's agricultural economy and provide stability to food production throughout the year. Farmers adapt their farming practices and crop selection accordingly to make the best use of the prevailing climatic conditions in each season."},
                            {"role":"user","content":quastion}
                ]
            )
    
    return completion['choices'][0]['message']['content']


###





def text_to_audio(text,filrname):
    tts = gTTS(text)
    tts.save(f'static/audio/{filrname}.mp3')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if 'audio' in request.files:
        audio = request.files['audio']
        if audio and allowed_file(audio.filename):
            filename = secure_filename(audio.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            audio.save(filepath)
            transcription = process_audio(filepath)
            return jsonify({'text': transcription})

    text = request.form.get('text')
    if text:
        response = process_text(text)
        return {'text': response['text'],'voice': url_for('static', filename='audio/' + response['voice'])}

    return jsonify({'text': 'Invalid request'})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_audio(filepath):
    # Placeholder function for processing audio (speech-to-text transcription)
    # Replace this with your own implementation using libraries like SpeechRecognition or DeepSpeech
    #return 'hello This is a placeholder transcription for audio'
    API_URL = "https://api-inference.huggingface.co/models/jonatasgrosman/wav2vec2-large-xlsr-53-english"
    headers = {"Authorization": hugging_face}
    with open(filepath, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    data = response.json()
    return data['text']
    

def process_text(text):
    # Placeholder function for processing user's text input
    # Replace this with your own implementation
    return_text = get_anwer_openai(text)
    #asyncio.run(text_to_audio(return_text))
    # generating random strings
    res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=8))
    text_to_audio(return_text,res)
    return {"text":return_text,"voice": f"{res}.mp3"}


if __name__ == '__main__':
    app.run(debug=True)

