import streamlit as st
import os
import datetime
import wikipedia
from groq import Groq
from dotenv import load_dotenv

# Load local env
# Load .env for local environment
load_dotenv()

# Get API key
# Get API key (works locally + Streamlit Cloud)
api_key = os.getenv("GROQ_API_KEY")

# If running on Streamlit Cloud
if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        st.error("❌ GROQ API key not found.")
        st.error("❌ GROQ API key not found. Add it to .env or Streamlit secrets.")
        st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

# Streamlit UI setup
st.set_page_config(page_title="Jarvis AI", page_icon="🤖")

st.title("🤖 Jarvis AI Assistant")
st.write("Your personal AI assistant powered by Groq")

# Session memory
# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# LLM function
# Function to ask Groq
def ask_llm(prompt):

    if not prompt.strip():
        return "Please ask something."

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are Jarvis, an intelligent AI assistant."
                    "content": "You are Jarvis, a helpful AI assistant."
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
        return f"⚠️ AI Error: {str(e)}"


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
            return "Sorry, I couldn't find anything on Wikipedia."

    return None


# Chat input
prompt = st.chat_input("Ask Jarvis anything...")
prompt = st.chat_input("Ask Jarvis something...")

if prompt:

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    # Check commands
    command_response = handle_commands(prompt)

    if command_response:
        response = command_response
    else:
        response = ask_llm(prompt)

    # Save AI response
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    with st.chat_message("assistant"):
        st.write(response)


# Sidebar
st.sidebar.title("⚡ Tools")
# Sidebar tools
st.sidebar.title("⚡ Jarvis Tools")

# Clear chat
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Wikipedia quick search
st.sidebar.subheader("Wikipedia Search")

topic = st.sidebar.text_input("Topic")
topic = st.sidebar.text_input("Enter topic")

if st.sidebar.button("Search") and topic:

    try:
        result = wikipedia.summary(topic, sentences=3)
        st.sidebar.write(result)
    except:
        st.sidebar.write("No results found")
