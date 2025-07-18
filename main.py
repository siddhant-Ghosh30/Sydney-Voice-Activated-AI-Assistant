import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import sys 
import keys # this will store my API keys
from google import genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from google.genai import types
import pyaudio


# recognizer = sr.Recognizer()
# engine = pyttsx3.init()

client = genai.Client(api_key=keys.api_key_gemini)

# import the Spotify API client   
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=keys.spotify_client_id,
    client_secret=keys.spotify_client_secret
))

# Get city from IP
def get_city_from_ip():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        return data.get("city", "Bangalore")  # Default to Bangalore if city not found
    except:
        return "Bangalore"

# Weather handler function
def get_weather(city="Bangalore"):
    try:
        api_key = keys.openweather_api
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        full_url = f"{base_url}q={city}&appid={api_key}&units=metric"

        response = requests.get(full_url)
        data = response.json()

        if data["cod"] != "404":
            main = data["main"]
            weather_desc = data["weather"][0]["description"]
            temp = main["temp"]
            humidity = main["humidity"]

            # Optional: friendly prefixes
            prefix = ""
            if "rain" in weather_desc:
                prefix = "Don’t forget your umbrella! "
            elif "clear" in weather_desc:
                prefix = "Looks like a great day! "

            return (
                f"{prefix}The current weather in {city} is {weather_desc}. "
                f"The temperature is {temp} degrees Celsius with humidity at {humidity} percent."
            )
        else:
            return "I couldn't find that city. Please try again."
    except Exception:
        return "Something went wrong while getting the weather."
    
def will_it_rain(city="Bangalore"):
    try:
        api_key = keys.openweather_api
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != "200":
            return "I couldn't fetch the forecast for that city."

        for forecast in data["list"][:8]:  # next 24 hours
            weather = forecast["weather"][0]["main"].lower()
            if "rain" in weather or "drizzle" in weather:
                return f"Yes, rain is expected in {city} within the next 24 hours. Stay dry!"
        return f"No rain is expected in {city} for the next 24 hours."
    except Exception:
        return "I had trouble checking the forecast."


# Voice of Sydney
"""VOICE"""
# voices = engine.getProperty('voices')       #getting details of current voice
# engine.setProperty('voice', voices[1].id)   #Female voice for Sydney cause uk

# def say(text):
#     engine.say(text)
#     engine.runAndWait()

def say(text):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents= text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name="Sulafat"
                        )
                    )
                )
            )
        )

        audio_data = response.candidates[0].content.parts[0].inline_data.data

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=24000,
                        output=True)
        stream.write(audio_data)
        stream.stop_stream()
        stream.close()
        p.terminate()

    except Exception as e:
        print(f"❌ Gemini TTS failed: {e}")

        


def aiProcess(command): # from client2.py
    # client = genai.Client(api_key=keys.api_key_gemini)
    system_role = (
    "You are Sydney, a friendly, intelligent, and slightly witty female virtual assistant. "
    "You help users with tasks like answering questions, giving updates, or playing music. "
    "Speak in a natural, conversational but professional tone suitable for a voice assistant. "
    "Keep your responses clear and concise — under 100 words unless the user specifically asks for a detailed or extended answer. "
    "Avoid technical jargon unless requested. Stay polite, calm, and helpful at all times. "
    "Only respond to the user's query below:")
    user_role = command
    response = client.models.generate_content(model="gemini-2.5-flash",
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

    elif "weather" in c.lower() or "temperature" in c.lower():
        words = c.lower().split()
        if "in" in words:
            index = words.index("in")
            city = " ".join(words[index + 1:])
        else:
            city = get_city_from_ip()

        say(get_weather(city))

    elif "will it rain" in c.lower():
        words = c.lower().split()
        if "in" in words:
            index = words.index("in")
            city = " ".join(words[index + 1:])
        else:
            city = get_city_from_ip()

        say(will_it_rain(city))
    
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