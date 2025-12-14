import streamlit as st
from openai import OpenAI
from app.data.db import connect_database
from app.data.incidents import get_all_incidents
from app.data.datasets import get_all_datasets
from app.data.tickets import get_all_tickets
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page guard - check if logged in
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")

# Initialize client
if api_key:
    try:
        client = OpenAI(api_key=api_key)
        api_available = True
    except:
        api_available = False
else:
    api_available = False

st.title("🤖 AI Assistant")

# Back button
if st.button("← Back to Dashboard"):
    st.switch_page("pages/1_Dashboard.py")

st.divider()

# Check API availability
if not api_available:
    st.error("OpenAI API not available. Check your .env file and credits.")
    st.stop()

# Initialize messages in session state
if 'ai_messages' not in st.session_state:
    st.session_state.ai_messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Display previous messages
for message in st.session_state.ai_messages:
    if message["role"] != "system":  # Don't show system message
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Get user input
prompt = st.chat_input("Type your message here...")

if prompt:
    # Show user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Add to messages
    st.session_state.ai_messages.append({"role": "user", "content": prompt})
    
    # Get AI response
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.ai_messages
        )
        
        ai_msg = response.choices[0].message.content
        
        # Show AI response
        with st.chat_message("assistant"):
            st.write(ai_msg)
        
        # Add to messages
        st.session_state.ai_messages.append({"role": "assistant", "content": ai_msg})
        
    except Exception as e:
        st.error(f"API Error: {e}")