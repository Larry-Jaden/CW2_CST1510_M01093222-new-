import streamlit as st

# PAGE CONFIG
st.set_page_config(
    page_title="Multi-Domain Intelligence Platform",
    page_icon="🏠",
    layout="wide"
)

# AUTH CHECK
if "current_user" not in st.session_state:
    st.warning(" Please log in to continue.")
    st.switch_page("pages/1_Login.py")
    st.stop()

# HEADER
st.title("🏠 Multi-Domain Intelligence Platform")

st.markdown(
    f"""
    **Logged in as:** `{st.session_state['current_user']}`  
    **Role:** `{st.session_state.get('current_role', 'N/A')}`
    """
)

st.divider()

# DASHBOARD NAVIGATION
st.subheader(" Domains")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button(" Cybersecurity"):
        st.switch_page("pages/2_Cybersecurity.py")

with col2:
    if st.button(" Data Science"):
        st.switch_page("pages/3_Data_Science.py")

with col3:
    if st.button(" IT Operations"):
        st.switch_page("pages/4_IT_Operations.py")

with col4:
    if st.button("🤖 AI Assistant"):
        st.switch_page("pages/5_ _AI_Assistant.py")

st.divider()

# LOGOUT
if st.button(" Logout"):
    st.session_state.clear()
    st.success("You have been logged out.")
    st.switch_page("pages/1_Login.py")
