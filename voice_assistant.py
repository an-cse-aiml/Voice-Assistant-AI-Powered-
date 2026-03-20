# Voice Assistant (Alexa-type Model)
# This script listens for voice commands, converts them to text,
# gets an intelligent response from a generative AI model, and speaks the answer.

# --- Prerequisites ---
# Before running, you need to install the required libraries.
# Open your terminal or command prompt and run the following commands:
# pip install SpeechRecognition
# pip install pyttsx3
# pip install google-generativeai
# pip install pyaudio

# For Linux, you might also need to install PortAudio development libraries:
# sudo apt-get install portaudio19-dev

# For Windows/macOS, PyAudio should install correctly with pip.

import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import os
import datetime

# --- Configuration ---

# IMPORTANT: Configure your Google AI API Key.
# 1. Go to Google AI Studio: https://aistudio.google.com/
# 2. Create a new API key.
# 3. It's best practice to set this as an environment variable for security.
#    - On Windows: setx GOOGLE_API_KEY "YOUR_API_KEY"
#    - On macOS/Linux: export GOOGLE_API_KEY="YOUR_API_KEY"
#    After setting it, you need to restart your terminal/IDE for it to take effect.
try:
    api_key = os.environ["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    print("API Key not found. Please set the GOOGLE_API_KEY environment variable.")
    exit()


# --- Core Components ---

class VoiceAssistant:
    """
    Manages the voice assistant's functionalities: listening, speaking,
    and processing commands.
    """
    def __init__(self):
        # Initialize Speech Recognition
        self.recognizer = sr.Recognizer()
        # Initialize Text-to-Speech Engine
        # Explicitly using the 'sapi5' driver can improve compatibility on Windows.
        # If on macOS or Linux, you may need to remove driverName='sapi5'.
        self.engine = pyttsx3.init()   # auto-select best driver
        self.configure_voice()

        # Configure the Generative Model
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Set the wake word for the assistant
        self.wake_word = "hey bro"

    def configure_voice(self):
        """Configures the voice properties for the TTS engine."""
        voices = self.engine.getProperty('voices')
        # --- DIAGNOSTIC --- Let's see what voices are available
        print("--- Available Voices ---")
        for voice in voices:
            print(voice)
        print("------------------------")

        voices = self.engine.getProperty('voices')
        print("\n--- Installed Voices ---")
        for i, voice in enumerate(voices):
            print(f"{i}: {voice.name} ({voice.id})")
        print("------------------------\n")

        # You can change the index to select a different voice if available
        # For example, voices[1] is often a female voice on Windows
        # We are changing this from voices[0] to voices[1] as a fix.
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
        else:
            self.engine.setProperty('voice', voices[0].id)

        self.engine.setProperty('rate', 150) # Speed of speech
        self.engine.setProperty('volume', 1.0) # Volume (0.0 to 1.0)

    def speak(self, text):
        """Converts text to speech and prints what is being said."""
        print(f"Assistant: {text}")
        try:
            engine = pyttsx3.init('sapi5')   # new engine instance each time
            engine.setProperty('rate', 180)
            engine.setProperty('volume', 1.0)
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)

            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print("⚠️ Speech failed:", e)
            
    def listen(self):
        """Listens for audio input from the microphone and converts it to text."""
        with sr.Microphone() as source:
            print("Listening...")
            # Adjust for ambient noise to improve accuracy
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing...")
            # Use Google's speech recognition engine
            command = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

    def process_command(self, command):
        """Processes the recognized command and provides a response."""
        # Simple, hard-coded commands that don't need AI
        if "goodbye" in command or "exit" in command:
            self.speak("Goodbye!")
            return False # Signal to exit the main loop

        if "what is the time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}")
            return True

        # For everything else, query the generative model
        try:
            print("Thinking...")
            # Create a prompt for the model
            prompt = f"You are a helpful assistant. Please provide a concise response to the following query: '{command}'"
            response = self.model.generate_content(prompt)
            
            # Check if the response has text before speaking
            if response and response.text:
                self.speak(response.text)
            else:
                self.speak("I'm sorry, I couldn't generate a response for that.")

        except Exception as e:
            print(f"An error occurred while communicating with the AI model: {e}")
            self.speak("Sorry, I'm having trouble connecting to my brain right now.")
        
        return True # Continue the loop

    def run(self):
        """The main loop for the voice assistant."""
        self.speak("Hello! I'm your voice assistant. Say my wake word to give me a command.")
        
        while True:
            # First, listen for the wake word
            print(f"\nSay '{self.wake_word}' to activate me.")
            command = self.listen()

            if command and self.wake_word in command:
                self.speak("Yes? How can I help?")
                # Listen for the actual command after wake word is detected
                user_command = self.listen()
                if user_command:
                    if not self.process_command(user_command):
                        break # Exit loop if process_command returns False
            elif command is None:
                # If listening failed, just loop again
                continue


# --- Main Execution ---
if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
