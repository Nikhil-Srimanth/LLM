import streamlit as st
import os
import datetime
import wikipedia
from groq import Groq
from dotenv import load_dotenv

# Load .env (for local running)
load_dotenv()

# Get API key (works locally + Streamlit Cloud)
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        st.error("API key not found. Add GROQ_API_KEY to .env or Streamlit secrets.")
        st.stop()

# Initialize Groq
client = Groq(api_key=api_key)

# Streamlit UI setup
st.set_page_config(page_title="Jarvis AI", page_icon="🤖")

st.title("🤖 Jarvis AI Assistant")
st.write("Your personal AI assistant powered by Groq")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# LLM function
def ask_llm(prompt):

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# Command system
def handle_commands(prompt):

    prompt = prompt.lower()

    if "time" in prompt:
        return f"The current time is {datetime.datetime.now().strftime('%H:%M')}"

    if "wikipedia" in prompt:
        topic = prompt.replace("wikipedia", "")
        try:
            return wikipedia.summary(topic, sentences=2)
        except:
            return "Sorry, I couldn't find information."

    return None


# Chat input
prompt = st.chat_input("Ask Jarvis something...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

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

if st.sidebar.button("Search") and topic:

    try:
        result = wikipedia.summary(topic, sentences=3)
        st.sidebar.write(result)
    except:
        st.sidebar.write("No results found")

