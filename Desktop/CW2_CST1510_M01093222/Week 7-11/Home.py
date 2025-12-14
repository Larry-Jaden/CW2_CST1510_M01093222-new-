import streamlit as st
from pathlib import Path
import sys
import os

# Ensure the project root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Page configuration
st.set_page_config(
    page_title="Intelligence Platform",
    layout="wide"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'role' not in st.session_state:
    st.session_state.role = "user"
if 'users' not in st.session_state:
    st.session_state.users = {}

def show_login_form():
    """Login form from tutorial"""
    st.subheader("Login")
    
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Log in", key="login_button", use_container_width=True):
            if login_username in st.session_state.users:
                if st.session_state.users[login_username] == login_password:
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.session_state.role = "USER"
                    st.success(f"Login successful! Welcome, {login_username}")
                    st.switch_page("pages/1_Dashboard.py")
                else:
                    st.error("Invalid credentials")
            else:
                st.error("User not found")

def show_register_form():
    """Registration form from tutorial"""
    st.subheader("Register")
    
    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Create account", key="register_button", use_container_width=True):
            if not new_username or not new_password:
                st.warning("Please fill in all fields.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            elif new_username in st.session_state.users:
                st.error("Username already exists.")
            else:
                st.session_state.users[new_username] = new_password
                st.success("Account created! ")
                st.info("Go to Login tab to sign in.")

def main():
    st.title("🛡️ Multi-Domain Intelligence Platform")
    st.divider()
    
    # Create tabs
    tab_login, tab_register = st.tabs(["Login", "Register"])
    
    with tab_login:
        show_login_form()
    
    with tab_register:
        show_register_form()

if __name__ == "__main__":
    main()