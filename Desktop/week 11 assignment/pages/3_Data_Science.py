import streamlit as st

if "current_user" not in st.session_state:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("pages/1_Login.py")
    st.stop()

st.set_page_config(page_title="Data Science", layout="wide")
st.title(" Data Science")
st.write(f"Logged in as: **{st.session_state['current_user']}**")
st.divider()

st.header("Datasets")
st.info("Data Science datasets dashboard will be displayed here.")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Datasets", 0)
with col2:
    st.metric("Processed", 0)
with col3:
    st.metric("Pending", 0)

st.divider()
if st.button("← Back to Dashboard"):
    st.switch_page("Home.py")
