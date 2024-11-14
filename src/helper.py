import streamlit as st
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gtts import gTTS
import time

print("Perfect!!")
load_dotenv()

# Load and check the Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing from environment variables.")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Voice input using sounddevice and speech_recognition
def voice_input():
    duration = 5  # Recording duration in seconds
    sample_rate = 16000  # Sample rate

    print("Listening...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait for the recording to complete
    wav.write("temp_audio.wav", sample_rate, audio_data)  # Save as a temporary .wav file

    # Recognize text from the audio file
    recognizer = sr.Recognizer()
    with sr.AudioFile("temp_audio.wav") as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service: {e}")

# Text to speech function
def text_to_speech(text):
    tts=gTTS(text=text, lang="en")
    
    #save the speech from the given text in the mp3 format
    tts.save("speech.mp3")

# LLM function
def llm_model_object(user_text):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.0-pro')
    response = model.generate_content(user_text)
    result = response.text.replace('*', '')  # Remove asterisks
    return result


