import speech_recognition as sr
import pyttsx3
import spacy
import datetime
import requests

# Initialize speech recognition, text-to-speech, and NLP components
recognizer = sr.Recognizer()
engine = pyttsx3.init()
nlp = spacy.load('en_core_web_sm')

def listen_for_command():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("Command:", command)
        process_command(command)
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError as e:
        print("Sorry, there was an issue with the speech recognition service.")

def speak(text):
    engine.say(text)
    engine.runAndWait()

def process_command(command):
    doc = nlp(command)
    intent = None

    # Extract the main verb (intent) from the command
    for token in doc:
        if token.pos_ == 'VERB':
            intent = token.lemma_
            break

    if intent:
        if intent == 'start':
            start_command()
        elif intent == 'stop':
            stop_command()
        elif intent == 'play':
            play_music_command()
        elif intent == 'weather':
            weather_command()
        elif intent == 'time':
            time_command()
        else:
            speak("Sorry, I cannot perform that command.")
    else:
        speak("Sorry, I cannot understand the command.")

def start_command():
    speak("I'm ready. How can I assist you?")

def stop_command():
    speak("Goodbye!")
    exit()

def play_music_command():
    # Code to interact with a music streaming service API and play music
    speak("Playing music.")

def weather_command():
    # Code to fetch weather information from a weather API
    api_key = 'YOUR_WEATHER_API_KEY'
    city = 'YOUR_CITY_NAME'
    url = f'https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'

    response = requests.get(url)
    data = response.json()

    if 'current' in data:
        temperature = data['current']['temp_c']
        condition = data['current']['condition']['text']
        speak(f"The current weather in {city} is {condition} with a temperature of {temperature} degrees Celsius.")
    else:
        speak("Sorry, I couldn't fetch the weather information.")

def time_command():
    current_time = datetime.datetime.now().strftime("%H:%M")
    speak(f"The current time is {current_time}.")

# Main program loop
while True:
    listen_for_command()
