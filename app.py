import streamlit as st
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import pywhatkit
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Text to speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        return command.lower()
    except:
        return ""

def ask_llm(prompt):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are Jarvis, an intelligent AI assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# Streamlit UI
st.set_page_config(page_title="Jarvis AI", page_icon="🤖")

st.title("🤖 Jarvis AI Assistant")
st.write("Your personal AI assistant powered by Groq")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Text input
user_input = st.text_input("Ask Jarvis something")

col1, col2 = st.columns(2)

with col1:
    if st.button("Send"):
        if user_input:
            response = ask_llm(user_input)

            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Jarvis", response))

            speak(response)

with col2:
    if st.button("🎤 Voice Command"):
        command = listen()

        if command != "":
            response = ask_llm(command)

            st.session_state.chat_history.append(("You", command))
            st.session_state.chat_history.append(("Jarvis", response))

            speak(response)

# Display chat
for role, message in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Jarvis:** {message}")

# Quick commands
st.subheader("⚡ Quick Commands")

if st.button("Current Time"):
    time = datetime.datetime.now().strftime("%H:%M")
    st.write(f"Current time: {time}")
    speak(f"The time is {time}")

if st.button("Open YouTube"):
    webbrowser.open("https://youtube.com")
    st.write("Opening YouTube")

if st.button("Search Wikipedia"):
    topic = st.text_input("Enter topic")
    if topic:
        result = wikipedia.summary(topic, sentences=2)
        st.write(result)
