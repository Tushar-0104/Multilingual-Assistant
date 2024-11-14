import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gtts import gTTS

print("perfect!!")
load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY



def voice_input():
    r=sr.Recognizer()
    
    with sr.Microphone() as source:
        print("listening...")
        audio=r.listen(source)
    try:
        text=r.recognize_google(audio)
        print("you said: ", text)
        return text
    except sr.UnknownValueError:
        print("sorry, could not understand the audio")
    except sr.RequestError as e:
        print("could not request result from google speech recognition service: {0}".format(e))
    

def text_to_speech(text):
    tts=gTTS(text=text, lang="en")
    
    #save the speech from the given text in the mp3 format
    tts.save("speech.mp3")

# LLM function
def llm_model_object(user_text):
    # Set up API key for Google Generative AI
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Enhanced prompt for structured, detailed responses
    prompt = (
        "Please generate a detailed and well-structured response to the following query. "
        "Provide an in-depth explanation in clear, easy-to-read paragraphs. Use the following format: "
        "1. Begin with an introductory overview. "
        "2. Use clear headings for each main point. "
        "3. Include bullet points or numbered lists where applicable for readability. "
        "4. Ensure clarity and accuracy for technical terms and abbreviations, like 'ML' for 'Machine Learning', "
        "or 'AI' for 'Artificial Intelligence'. Pronounce technical terms correctly, as specified."
    )

    # Combine the prompt with the user's question
    full_prompt = f"{prompt}\n\nUser Query: {user_text}"
    
    # Use the Generative Model with the enhanced prompt
    model = genai.GenerativeModel('gemini-1.0-pro')
    response = model.generate_content(full_prompt)
    
    # Clean up the output
    result = response.text.replace('*', '')  
    return result
