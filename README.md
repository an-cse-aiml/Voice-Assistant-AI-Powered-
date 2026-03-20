# 🎙️ AI Voice Assistant

## 📌 Overview

This project is an AI-powered voice assistant built using Python. It listens to user voice commands, converts speech into text, processes the query using a generative AI model, and responds with natural-sounding speech. The assistant can perform basic tasks and answer general queries interactively.

---

## 🚀 Features

* 🎤 Voice command recognition
* 🔊 Text-to-speech response
* 🤖 AI-generated intelligent replies
* ⏰ Built-in commands (time, exit, etc.)
* 🎯 Wake word activation ("Hey Bro")
* 💬 Real-time interaction

---

## 🛠️ Tech Stack

* Python
* SpeechRecognition
* pyttsx3
* Google Generative AI (Gemini)
* PyAudio

---

## 📂 Project Structure

voice-assistant/
│── voice_assistant.py
│── README.md
│── requirements.txt

---

## ▶️ Installation & Setup

### 1. Clone the repository

git clone https://github.com/an-cse-aiml/Voice-Assistant-AI-Powered-

### 2. Navigate to the folder

cd voice-assistant

### 3. Install dependencies

pip install -r requirements.txt

### 4. Set API Key

Get your API key from Google AI Studio and set it as an environment variable:

**Windows:**
setx GOOGLE_API_KEY "your_api_key"

**Mac/Linux:**
export GOOGLE_API_KEY="your_api_key"

---

## ▶️ Run the Application

python voice_assistant.py

---

## 🎯 Usage

* Say the wake word: **"Hey Bro"**
* Ask your question or give a command
* The assistant will respond with voice output

---

## 📊 Example Commands

* What is the time?
* Tell me a joke
* Explain artificial intelligence

---

## ⚠️ Requirements

* Microphone-enabled device
* Internet connection
* Python 3.x

---

## 🔮 Future Improvements

* Add graphical user interface (GUI)
* Improve wake word detection
* Add more built-in commands
* Multi-language support

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork and improve this project.

---

## 📜 License

This project is open-source and available under the MIT License.
