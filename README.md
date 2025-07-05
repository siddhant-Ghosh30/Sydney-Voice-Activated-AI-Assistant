# Sydney – Voice Activated AI Assistant

**Sydney** is a smart, voice-controlled virtual assistant built using Python. Think of her as your personal Alexa or Google Assistant –equipped with AI-powered responses, music playback via Spotify, and real-time voice interaction. Also designed to perform tasks such as web browsing, fetching news headlines

---

## 🔧 Features

- 🎙️ **Speech Recognition** – Listens for your wake word and understands commands
- 🧠 **Gemini AI Integration** – Handles general queries using natural, conversational responses
- ᯤSpotify **Music Playback** – Search and open tracks directly using the Spotify API
- 🌐 **Web Automation** – Instantly opens websites like Google, YouTube, LinkedIn, etc.
- 📰 **News Headlines** – Reads out current top headlines using NewsAPI
- 🗣️ **Text-to-Speech** – Replies in a natural voice using `pyttsx3`

---

## 🧪 Demo Commands

- `"Sydney"` → Wake word  
- `"Play She by Harry Styles"` → Opens the correct track on Spotify  
- `"Open Google"` → Opens Google in the browser  
- `"Tell me a joke"` → Let Gemini handle it  
- `"What's the news"` → Reads latest headlines aloud  

---

## 📁 Project Structure

Sydney-Voice-Activated-AI-Assistant/
│
├── main.py # Main assistant logic
├── client2.py # Gemini API response handling
├── keys.py # Stores API keys (ignored in version control)
├── requirements.txt # Python dependencies
├── .gitignore # Git ignore config
└── .venv/ # Virtual environment (ignored)



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
