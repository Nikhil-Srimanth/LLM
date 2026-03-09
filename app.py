import streamlit as st
import os
import datetime
import wikipedia
from groq import Groq
from dotenv import load_dotenv

# Load local env
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

# If running on Streamlit Cloud
if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        st.error("❌ GROQ API key not found.")
        st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

st.set_page_config(page_title="Jarvis AI", page_icon="🤖")

st.title("🤖 Jarvis AI Assistant")

# Session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# LLM function
def ask_llm(prompt):

    if not prompt.strip():
        return "Please ask something."

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "You are Jarvis, an intelligent AI assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Error from AI service: {str(e)}"


# Command handler
def handle_commands(prompt):

    prompt = prompt.lower()

    if "time" in prompt:
        return f"The current time is {datetime.datetime.now().strftime('%H:%M')}"

    if "wikipedia" in prompt:
        topic = prompt.replace("wikipedia", "")

        try:
            return wikipedia.summary(topic, sentences=2)
        except:
            return "I couldn't find information on Wikipedia."

    return None


# Chat input
prompt = st.chat_input("Ask Jarvis anything...")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    command_response = handle_commands(prompt)

    if command_response:
        response = command_response
    else:
        response = ask_llm(prompt)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    with st.chat_message("assistant"):
        st.write(response)


# Sidebar
st.sidebar.title("⚡ Tools")

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Wikipedia quick search
st.sidebar.subheader("Wikipedia Search")

topic = st.sidebar.text_input("Topic")

if st.sidebar.button("Search") and topic:
    try:
        result = wikipedia.summary(topic, sentences=3)
        st.sidebar.write(result)
    except:
        st.sidebar.write("No results found")
