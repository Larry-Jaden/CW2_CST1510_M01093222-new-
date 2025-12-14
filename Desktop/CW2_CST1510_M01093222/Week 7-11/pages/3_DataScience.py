import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Ensure the project root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.data.datasets import get_all_datasets, get_datasets_by_category

# Page guard
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.set_page_config(
    page_title="Data Science",
    layout="wide"
)

# Top navigation
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("← Dashboard", key="ds_dashboard"):
        st.switch_page("pages/1_Dashboard.py")
with col2:
    if st.button("Logout →", key="ds_logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = "user"
        st.switch_page("Home.py")

def main():
    st.title(" Data Science Datasets")
    st.divider()
    
    datasets = get_all_datasets()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Datasets", len(datasets))
    
    with col2:
        if 'size' in datasets.columns:
            total_size = datasets['size'].sum() / (1024 * 1024)  # Convert to MB
            st.metric("Total Size (MB)", f"{total_size:.1f}")
        else:
            st.metric("Total Size", "N/A")
    
    with col3:
        if len(datasets) > 0 and 'size' in datasets.columns:
            avg_size = total_size / len(datasets)
            st.metric("Avg Size (MB)", f"{avg_size:.1f}")
        else:
            st.metric("Avg Size", "N/A")
    
    st.divider()
    
    if len(datasets) > 0:
        st.dataframe(datasets)
        
        st.divider()
        
        if 'size' in datasets.columns:
            try:
                datasets_copy = datasets.copy()
                datasets_copy['size'] = pd.to_numeric(datasets_copy['size'], errors='coerce')
                top_datasets = datasets_copy.dropna(subset=['size']).nlargest(10, 'size')
                
                if len(top_datasets) > 0:
                    fig = px.bar(top_datasets, y='name', x='size', orientation='h', 
                                title='Top 10 Datasets by Size', labels={'size': 'Size (bytes)', 'name': 'Dataset'})
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not generate size chart: {e}")
    else:
        st.info("No datasets found")

if __name__ == "__main__":
    main()