# since this is a mega project, I'll install alot of packages
# and I'll install them in a virtual environment

import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import sys 
import keys # this will store my API keys
from google import genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


recognizer = sr.Recognizer()
engine = pyttsx3.init()

# import the Spotify API client   
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=keys.spotify_client_id,
    client_secret=keys.spotify_client_secret
))

# API key from newsapi.org get your own 

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[1].id)   #Female voice for Sydney cause uk

def say(text):
    engine.say(text)
    engine.runAndWait()


def aiProcess(command): # from client2.py
    client = genai.Client(api_key=keys.api_key_gemini)
    system_role = (
    "You are Sydney, a friendly, intelligent, and slightly witty female virtual assistant. "
    "You help users with tasks like answering questions, giving updates, or playing music. "
    "Speak in a natural, conversational tone suitable for a voice assistant. "
    "Keep your responses clear and concise — under 100 words unless the user specifically asks for a detailed or extended answer. "
    "Avoid technical jargon unless requested. Stay polite, calm, and helpful at all times. "
    "Only respond to the user's query below:")
    user_role = command
    response = client.models.generate_content(model="gemini-2.0-flash",
        contents= system_role + user_role)
    return response.text

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com/")
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com/")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/in/siddhantghosh/")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")
    elif "open spotify" in c.lower():
        webbrowser.open("https://open.spotify.com/?nd=1&flow_ctx=c3ced48b-a253-4651-ba4e-3c284c13d2c2%3A1722993184")
    # elif c.lower().startswith("play"):
    #     song = c.lower().split(" ")[1]
    #     link = musicLibrary.music[song]
    #     webbrowser.open(link)
    elif c.lower().startswith("play"):
        query = c.lower().replace("play", "").strip()

        # Check if user said "by [artist]"
        if " by " in query:
            song, artist = query.split(" by ", 1)
            song = song.strip()
            artist = artist.strip()
            search_query = f"track:{song} artist:{artist}"
        else:
            search_query = query

        results = sp.search(q=search_query, limit=1, type='track')

        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_name = track['name']
            track_artist = track['artists'][0]['name']
            url = track['external_urls']['spotify']
            say(f"Playing {track_name} by {track_artist}")
            webbrowser.open(url)
        else:
            say("I couldn't find that song on Spotify.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={keys.newsapi}")

        if r.status_code == 200:
            # parse the JSON response
            data = r.json()
            # extract the articles
            articles = data.get('articles', [])

            # announce the headlines
            for article in articles:
                say(article['title'])
    
    elif "stop" in c.lower():
        a = sys.exit()

    else:
        # Imma let Gemini handle the request
        output = aiProcess(c)
        say(output)

        

if __name__ == "__main__":
    say("Initializing Sydney. . ...")
    while True:

        # listen for the wake word "Sidney"
        # obtain audio from the microphone
        r = sr.Recognizer()
        
        print("recognising...") # since it takes time to recognise I put this for UX
       

        # recognize speech using Google cause Sphinx is just not it:(
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source)#, timeout = 3, phrase_time_limit=1) 
            word = r.recognize_google(audio)
            # print(word)
            if(word.lower() == "sidney" or word.lower() == "sydney"):
                say("yes")
                # listen for my command
                with sr.Microphone() as source:
                    print("Sydney Active..")
                    audio = r.listen(source)#, timeout= 3, phrase_time_limit=1)
                    command = r.recognize_google(audio)
                    # print(command)
                    processCommand(command)
                    command = r.recognize_google(audio)

        except sr.UnknownValueError:
            print("I'm sorry, I could not understand audio")
        except sr.RequestError as e:
            print("Sidney error; {0}".format(e))
        except sr.WaitTimeoutError as w:
            print(" ")