import os
import speech_recognition as sr  # Converts voice commands to text
import pyttsx3  # Reads out text output to voice
import webbrowser
import google.generativeai as genai  # Google Generative AI client

import io

from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env file

api_key = os.getenv('GOOGLE_API_KEY')

# Configure Google Generative AI client with your API key
genai.configure(api_key=api_key)

# Define the model to use
model_name = "gemini-1.5-flash"  
def Reply(question):
    try:
        # Create a GenerativeModel object with the specified model
        model = genai.GenerativeModel(model_name=model_name)
        
        # Generate content based on the prompt
        response = model.generate_content([{"text": question}])
        # Assuming the response structure has a 'text' attribute
        answer = response.text
        return answer
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't process that."

# Text to speech initialization
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening .......')
        r.pause_threshold = 1  # Wait for 1 sec before considering the end of a phrase
        audio = r.listen(source)
    try:
        print('Recognizing ....')
        query = r.recognize_google(audio, language='en-in')
        print("User Said: {} \n".format(query))
    except Exception as e:
        print("Say that again .....")
        return "None"
    return query

if __name__ == '__main__':
    speak("Hello, how are you?")
    
    while True:
        query = takeCommand().lower()
        if query == 'none':
            continue

        # Get the reply from the Gemini model
        ans = Reply(query)
        print(ans)
        speak(ans)

        # Specific Browser Related Tasks
        if "open youtube" in query:
            webbrowser.open('https://www.youtube.com')
        if "open google" in query:
            webbrowser.open('https://www.google.com')
        if "GOODbye" in query:
            speak("Goodbye!")
            break
