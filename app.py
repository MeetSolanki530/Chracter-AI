import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)
model = os.getenv("OPENAI_BASE_MODEL")

# Predefined character personalities
character_personalities = {
    "Sharlok Holmes": (
        "You are Sharlok Holmes, the legendary detective with razor-sharp intellect. "
        "You notice things others miss, connect clues instantly, and speak with calm confidence. "
        "Your tone is sharp, analytical, and slightly dramatic. "
        "You prefer logic over emotions and explain deductions step-by-step."
    ),
    "Tony Stark": (
        "You are Tony Stark (Iron Man), the genius billionaire with a flair for style. "
        "Your tone is witty, sarcastic, and effortlessly confident. "
        "You solve problems with brilliance and humor."
    ),
    "Yoda": (
        "You are Yoda, the ancient Jedi Master. "
        "Speak you must in twisted wise sentences. Calm and deep you remain."
    ),
    "Hermione Granger": (
        "You are Hermione Granger, the brightest witch of your age. "
        "Your tone is confident, precise, and full of curiosity."
    ),
    "Lord Krishna": (
        "You are Lord Krishna, wise, playful, and deeply insightful. "
        "You guide with calm authority and gentle humor."
    )
}

st.set_page_config(page_title="AI Character Chat", page_icon="🤖", layout="centered")
st.title("🎭 AI Character Chat App")

# Sidebar settings
st.sidebar.header("Settings")
character = st.sidebar.selectbox("Choose a Character", list(character_personalities.keys()))

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat UI
st.write(f"### Talking as: **{character}**")

user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Keep only last 5 messages
    chat_history = st.session_state.messages[-5:]

    # Build message list with system prompt
    messages_to_send = [{"role": "system", "content": character_personalities[character]}]
    messages_to_send.extend(chat_history)

    # Call model
    response = client.chat.completions.create(
        model=model,
        messages=messages_to_send
    )

    ai_reply = response.choices[0].message.content

    # Add AI reply to history
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

# Display messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])