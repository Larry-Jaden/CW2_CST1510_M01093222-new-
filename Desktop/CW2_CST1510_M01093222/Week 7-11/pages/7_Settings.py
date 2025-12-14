import sys
import os
import streamlit as st

# Ensure the project root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Page guard
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.set_page_config(
    page_title="Settings",
    layout="wide"
)

# Top navigation
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("← Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
with col2:
    if st.button("Logout →"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = "user"
        st.switch_page("Home.py")

def main():
    st.title(" Settings")
    st.divider()
    
    st.info("User settings page")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Logged in as:** {st.session_state.get('username', 'Unknown')}")
        st.write(f"**Role:** {st.session_state.get('role', 'user')}")
    
    with col2:
        st.write("**Account Settings**")
        if st.button("Update Profile"):
            st.info("Profile update feature coming soon")

if __name__ == "__main__":
    main()
