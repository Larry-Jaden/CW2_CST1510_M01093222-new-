import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager

# PAGE CONFIGURATION
st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

st.title(" Login")
st.write("Welcome to the Multi-Domain Intelligence Platform")

# INITIALIZE SERVICES
db = DatabaseManager("database/platform.db")
auth = AuthManager(db)

# IF USER ALREADY LOGGED IN
if "current_user" in st.session_state:
    st.success(f"You are already logged in as **{st.session_state['current_user']}**")
    st.stop()

# LOGIN FORM UI
with st.form("login_form", clear_on_submit=False):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

# LOGIN LOGIC
if submitted:
    if not username or not password:
        st.error("Please enter both username and password.")
    else:
        user = auth.login_user(username, password)

        if user is None:
            st.error("❌ Invalid username or password")
        else:
            # Save user details in session
            st.session_state["current_user"] = user.get_username()
            st.session_state["current_role"] = user.get_role()

            st.success(f"✅ Login successful! Welcome, **{user.get_username()}**")

            st.switch_page("pages/2_Cybersecurity.py")
