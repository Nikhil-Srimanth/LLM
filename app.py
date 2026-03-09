import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        st.error("API key not found")
        st.stop()

client = Groq(api_key=api_key)

# Page config
st.set_page_config(
    page_title="Jarvis AI",
    page_icon="🤖",
    layout="wide"
)

# Sidebar
st.sidebar.title("💬 ChatGPT Style Jarvis")

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("➕ New Chat"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.write("Powered by Groq")

# Main title
st.title("🤖 Jarvis AI Assistant")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User input
prompt = st.chat_input("Send a message...")

if prompt:

    # Store user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        full_response = ""

        try:
            completion = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=1024,
                stream=True
            )

            # Streaming response
            for chunk in completion:

                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"Error: {str(e)}"
            message_placeholder.markdown(full_response)

    # Save assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )

