```python
import streamlit as st
import datetime
import wikipedia
import webbrowser
import requests
from groq import Groq

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Jarvis AI", page_icon="🤖", layout="wide")

st.title("🤖 Jarvis AI Assistant")
st.write("Your personal AI assistant powered by Groq")

# Conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Function to query LLM
def ask_llm(prompt):

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are Jarvis, an intelligent helpful AI assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# Command handler
def handle_commands(prompt):

    prompt = prompt.lower()

    # Time
    if "time" in prompt:
        return f"The current time is {datetime.datetime.now().strftime('%H:%M')}"

    # Wikipedia search
    if "wikipedia" in prompt:
        topic = prompt.replace("wikipedia", "")
        try:
            return wikipedia.summary(topic, sentences=2)
        except:
            return "Sorry, I couldn't find anything."

    # Open websites
    if "open youtube" in prompt:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"

    if "open google" in prompt:
        webbrowser.open("https://google.com")
        return "Opening Google"

    return None


# Chat input
prompt = st.chat_input("Ask Jarvis something...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    # Check commands
    command_response = handle_commands(prompt)

    if command_response:
        response = command_response
    else:
        response = ask_llm(prompt)

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.write(response)


# Sidebar tools
st.sidebar.title("⚡ Jarvis Tools")

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Wikipedia quick search
st.sidebar.subheader("Wikipedia Search")

topic = st.sidebar.text_input("Enter topic")

if st.sidebar.button("Search Wikipedia") and topic:
    try:
        result = wikipedia.summary(topic, sentences=3)
        st.sidebar.write(result)
    except:
        st.sidebar.write("No results found")

# File reader
st.sidebar.subheader("AI File Reader")

file = st.sidebar.file_uploader("Upload text file")

if file:

    text = file.read().decode("utf-8")

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "Summarize this document"},
            {"role": "user", "content": text}
        ]
    )

    summary = response.choices[0].message.content

    st.sidebar.write("### Summary")
    st.sidebar.write(summary)
```
