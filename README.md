# Sydney – Voice Activated AI Assistant

**Sydney** is a smart, voice-activated virtual assistant built using Python — designed to bring the functionality of tools like Alexa or Google Assistant to your desktop. With real-time speech recognition and natural language responses powered by Google's Gemini AI, Sydney can perform a variety of tasks including playing music via Spotify, opening websites, fetching the latest news headlines, and providing weather updates or rain forecasts. The assistant intelligently detects your location using your IP address.

---

## 🔧 Features

- 🎙️ **Speech Recognition** – Listens for your wake word and understands commands
- 🧠 **Gemini AI Integration** – Handles general queries using natural, conversational responses
- ᯤSpotify **Music Playback** – Search and open tracks directly using the Spotify API (through spotipy)
- 🌐 **Web Automation** – Instantly opens websites like Google, YouTube, LinkedIn, etc.
- 📰 **News Headlines** – Reads out current top headlines using NewsAPI
- 🗣️ **Text-to-Speech** – Replies in a natural voice using `pyttsx3`
- ☁️🌦️**Weather Reporting** - reports weather and rain forecasts (using the OpenWeatherMap Weather API) with location auto-detected via IP (via ipinfo.io).

---

## 🧪 Demo Commands

- `"Sydney"` → Wake word  
- `"Play She by Harry Styles"` → Opens the correct track on Spotify  
- `"Open Google"` → Opens Google in the browser  
- `"Tell me a joke"` → Let Gemini handle it  
- `"What's the news"` → Reads latest headlines aloud
- `"Will it rain today?”` (auto detects city if not mentioned) → Gets relavant weather info

---

## 📁 Project Structure

Sydney-Voice-Activated-AI-Assistant/<br>
│<br>
├── main.py # Main assistant logic<br>
├── client2.py # Gemini API response handling<br>
├── keys.py # Stores API keys (ignored in version control)<br>
├── requirements.txt # Python dependencies<br>
├── .gitignore # Git ignore config<br>
└── .venv/ # Virtual environment (ignored)<br>



## 🔐 Setup Instructions

1. **Clone the repo**:
   ```
   git clone https://github.com/siddhant-Ghosh30/Sydney-Voice-Activated-AI-Assistant.git
   cd Sydney-Voice-Activated-AI-Assistant
### Create virtual environment:

python -m venv .venv
`.venv\Scripts\activate  # Windows `
 
### Install dependencies:

`pip install -r requirements.txt`

### Create a `keys.py` File
`newsapi = "YOUR_NEWSAPI_KEY"
api_key_gemini = "YOUR_GEMINI_API_KEY"
spotify_client_id = "YOUR_SPOTIFY_CLIENT_ID"
spotify_client_secret = "YOUR_SPOTIFY_CLIENT_SECRET"`

### Run the assistant:

`python main.py`
