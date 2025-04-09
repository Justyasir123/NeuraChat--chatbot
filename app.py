import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found. Please check your .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

# Page Config
st.set_page_config(page_title="NeuraChat", page_icon="🤖")

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #001f3f;
        color: #d3d3d3;
    }
    h1, h4, label, .css-10trblm {
        color: #d3d3d3 !important;
        text-align: center;
    }
    .chat-bubble {
        background-color: #003366;
        color: #d3d3d3;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        font-size: 16px;
    }
    .chat-bubble-user {
        background-color: #004080;
        color: #d3d3d3;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        font-size: 16px;
    }
    .stTextInput > div > div > input {
        background-color: #ccffcc;
        color: black !important;
        border: 1px solid #ffffff;
    }
    .stButton > button {
        background-color: #ccffcc;
        color: black !important;
        border: none;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Caption
st.markdown("<h1>🤖 NeuraChat</h1>", unsafe_allow_html=True)
st.markdown("<h4>Smart Conversations, Anytime.</h4>", unsafe_allow_html=True)

# Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat Form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", placeholder="Type your message here...")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    # Build prompt from history
    prompt = ""
    for chat in st.session_state.chat_history:
        prompt += f"User: {chat['user']}\nBot: {chat['bot']}\n"
    prompt += f"User: {user_input}\nBot:"

    try:
        response = model.generate_content(prompt)
        bot_response = response.text.strip() if response.text else "Sorry, no response."

        # Update chat history
        st.session_state.chat_history.append({
            "user": user_input,
            "bot": bot_response
        })

    except Exception as e:
        st.error(f"Error: {e}")

# Display Chat
st.markdown("---")
for chat in st.session_state.chat_history:
    st.markdown(f"<div class='chat-bubble-user'><strong>You:</strong> {chat['user']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-bubble'><strong>NeuraChat:</strong> {chat['bot']}</div>", unsafe_allow_html=True)

# Clear Chat Button
if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
