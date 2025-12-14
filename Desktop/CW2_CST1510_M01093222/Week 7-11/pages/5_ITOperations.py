import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Ensure the project root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.data.tickets import get_all_tickets, get_tickets_by_priority

# Page guard
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.set_page_config(
    page_title="IT Operations",
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
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Dashboard", key="it_dashboard"):
            st.switch_page("pages/1_Dashboard.py")
    with col2:
        if st.button("Logout →", key="it_logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = "user"
            st.switch_page("Home.py")
    
    st.title(" IT Operations Tickets")
    st.divider()
    
    tickets = get_all_tickets()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Tickets", len(tickets))
    
    with col2:
        if len(tickets) > 0:
            high_priority = len(tickets[tickets['priority'].str.lower() == 'high'])
            st.metric("High Priority", high_priority)
        else:
            st.metric("High Priority", 0)
    
    with col3:
        if len(tickets) > 0:
            open_tickets = len(tickets[tickets['status'].str.lower() == 'open'])
            st.metric("Open Tickets", open_tickets)
        else:
            st.metric("Open Tickets", 0)
    
    st.divider()
    
    if len(tickets) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            if 'priority' in tickets.columns:
                priority_counts = tickets['priority'].value_counts().reset_index()
                priority_counts.columns = ['Priority', 'Count']
                fig = px.bar(priority_counts, x='Priority', y='Count', title='Tickets by Priority')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'status' in tickets.columns:
                status_counts = tickets['status'].value_counts().reset_index()
                status_counts.columns = ['Status', 'Count']
                fig = px.pie(status_counts, values='Count', names='Status', title='Tickets by Status')
                st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        st.dataframe(tickets, use_container_width=True)
    else:
        st.info("No tickets found")

if __name__ == "__main__":
    main()