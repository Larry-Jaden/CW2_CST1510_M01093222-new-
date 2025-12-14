import streamlit as st

if "current_user" not in st.session_state:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("pages/1_Login.py")
    st.stop()

st.set_page_config(page_title="AI Assistant", layout="wide")
st.title(" AI Assistant")
st.write(f"Logged in as: **{st.session_state['current_user']}**")
st.divider()

st.info("AI Assistant powered chatbot will be displayed here.")
st.write("This feature requires OpenAI API configuration.")

if st.button("← Back to Dashboard"):
    st.switch_page("Home.py")
