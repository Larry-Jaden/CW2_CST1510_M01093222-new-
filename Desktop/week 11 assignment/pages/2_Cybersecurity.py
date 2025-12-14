import streamlit as st

if "current_user" not in st.session_state:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("pages/1_Login.py")
    st.stop()

st.set_page_config(page_title="Cybersecurity", layout="wide")
st.title(" Cybersecurity")
st.write(f"Logged in as: **{st.session_state['current_user']}**")
st.divider()

st.header("Security Incidents")
st.info("Security incidents management dashboard will be displayed here.")

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Incidents", 0)
with col2:
    st.metric("Critical Alerts", 0)

st.divider()
if st.button("← Back to Dashboard"):
    st.switch_page("Home.py")
