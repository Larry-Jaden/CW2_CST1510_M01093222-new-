import sys
import os
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# Ensure the project root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.data.incidents import get_all_incidents, insert_incident

# Page guard
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.set_page_config(
    page_title="Cybersecurity",
    layout="wide"
)

# Top navigation
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("← Dashboard", key="cyber_dashboard"):
        st.switch_page("pages/1_Dashboard.py")
with col2:
    if st.button("Logout →", key="cyber_logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = "user"
        st.switch_page("Home.py")

def show_create_form():
    """Create a new incident - CREATE operation"""
    st.subheader("Create New Incident")
    
    with st.form("create_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            title = st.text_input("Incident Title", placeholder="e.g., Phishing Attack on Finance Dept")
        
        with col2:
            incident_type = st.selectbox(
                "Incident Type",
                ["Phishing", "SQL injection", "DDoS", "Malware", 
                 "Social Engineering", "Unauthorized Access", "Data Breach", "Other"]
            )
        
        with col3:
            severity = st.selectbox(
                "Severity",
                ["Low", "Medium", "High", "Critical"]
            )
        
        description = st.text_area("Description", placeholder="Provide details about the incident...")
        
        col4, col5 = st.columns(2)
        with col4:
            status = st.selectbox(
                "Status",
                ["Open", "In Progress", "Resolved", "Closed"]
            )
        
        with col5:
            date = st.date_input("Incident Date", value=datetime.now())
        
        # Form submission
        if st.form_submit_button("Create Incident"):
            if not title:
                st.error("Please enter an incident title")
            else:
                # Create incident data
                incident_data = {
                    'title': title,
                    'type': incident_type,
                    'severity': severity,
                    'description': description,
                    'status': status,
                    'date': date.strftime('%Y-%m-%d'),
                    'created_by': st.session_state.username,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # Insert into database
                try:
                    result = insert_incident(incident_data)
                    st.success(f"✅ Incident created successfully! ID: {result}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error creating incident: {e}")

def show_read_form():
    """View all incidents - READ operation"""
    st.subheader("View All Incidents")
    
    incidents = get_all_incidents()
    
    if len(incidents) > 0:
        # Filters
        col1, col2 = st.columns(2)
        
        with col1:
            severity_filter = st.selectbox(
                "Filter by Severity",
                ["All"] + list(incidents['severity'].unique()) if 'severity' in incidents.columns else ["All"],
                key="read_severity"
            )
        
        with col2:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All"] + list(incidents['status'].unique()) if 'status' in incidents.columns else ["All"],
                key="read_status"
            )
        
        # Apply filters
        filtered = incidents.copy()
        if severity_filter != "All" and 'severity' in filtered.columns:
            filtered = filtered[filtered['severity'] == severity_filter]
        if status_filter != "All" and 'status' in filtered.columns:
            filtered = filtered[filtered['status'] == status_filter]
        
        # Display results
        st.info(f"Showing {len(filtered)} of {len(incidents)} incidents")
        
        # Display in a table
        if not filtered.empty:
            display_cols = ['id', 'title', 'severity', 'status', 'date']
            display_cols = [col for col in display_cols if col in filtered.columns]
            
            st.dataframe(
                filtered[display_cols],
                use_container_width=True,
                hide_index=True
            )
            
            # Show detailed view for selected incident
            st.subheader("Incident Details")
            incident_options = [f"{row['id']}: {row['title']}" for _, row in filtered.iterrows()]
            selected = st.selectbox("Select Incident to View Details", incident_options, key="read_select")
            
            if selected:
                incident_id = int(selected.split(":")[0])
                incident = filtered[filtered['id'] == incident_id].iloc[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**ID:** {incident['id']}")
                    st.write(f"**Title:** {incident['title']}")
                    if 'severity' in incident:
                        st.write(f"**Severity:** {incident['severity']}")
                
                with col2:
                    if 'status' in incident:
                        st.write(f"**Status:** {incident['status']}")
                    if 'date' in incident:
                        st.write(f"**Date:** {incident['date']}")
                    if 'description' in incident:
                        st.write(f"**Description:** {incident['description']}")
        else:
            st.warning("No incidents match the selected filters")
    else:
        st.info("No incidents found in the database")

def show_update_form():
    """Update an existing incident - UPDATE operation"""
    st.subheader("Update Incident")
    
    incidents = get_all_incidents()
    
    if len(incidents) == 0:
        st.info("No incidents to update")
        return
    
    # Get list of incidents
    incident_options = [f"{row['id']}: {row['title']}" for _, row in incidents.iterrows()]
    selected = st.selectbox("Select Incident to Update", incident_options, key="update_select")
    
    if selected:
        incident_id = int(selected.split(":")[0])
        incident = incidents[incidents['id'] == incident_id].iloc[0]
        
        with st.form("update_form"):
            st.write(f"**Current Incident:** {incident['title']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                new_title = st.text_input("Title", value=incident['title'])
                new_type = st.selectbox(
                    "Type",
                    ["Phishing", "SQL injection", "DDoS", "Malware", 
                     "Social Engineering", "Unauthorized Access", "Data Breach", "Other"],
                    index=["Phishing", "SQL injection", "DDoS", "Malware", 
                           "Social Engineering", "Unauthorized Access", "Data Breach", "Other"].index(
                               incident['type'] if incident['type'] in ["Phishing", "SQL injection", "DDoS", "Malware", 
                                                                        "Social Engineering", "Unauthorized Access", "Data Breach", "Other"] 
                               else "Other"
                           )
                )
                new_severity = st.selectbox(
                    "Severity",
                    ["Low", "Medium", "High", "Critical"],
                    index=["Low", "Medium", "High", "Critical"].index(incident['severity'])
                )
            
            with col2:
                new_status = st.selectbox(
                    "Status",
                    ["Open", "In Progress", "Resolved", "Closed"],
                    index=["Open", "In Progress", "Resolved", "Closed"].index(incident['status'])
                )
                new_date = st.date_input(
                    "Date",
                    value=datetime.strptime(incident['date'], '%Y-%m-%d') if 'date' in incident else datetime.now()
                )
            
            new_description = st.text_area(
                "Description", 
                value=incident['description'] if 'description' in incident else "",
                placeholder="Update incident description..."
            )
            
            if st.form_submit_button("Update Incident"):
                # Prepare update data
                update_data = {
                    'title': new_title,
                    'type': new_type,
                    'severity': new_severity,
                    'status': new_status,
                    'date': new_date.strftime('%Y-%m-%d'),
                    'description': new_description,
                    'updated_by': st.session_state.username,
                    'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # Update in database
                try:
                    result = update_incident(incident_id, update_data)
                    st.success(f"✅ Incident {incident_id} updated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error updating incident: {e}")

def show_delete_form():
    """Delete an incident - DELETE operation"""
    st.subheader("Delete Incident")
    
    incidents = get_all_incidents()
    
    if len(incidents) == 0:
        st.info("No incidents to delete")
        return
    
    incident_options = [f"{row['id']}: {row['title']}" for _, row in incidents.iterrows()]
    selected = st.selectbox("Select Incident to Delete", incident_options, key="delete_select")
    
    if selected:
        incident_id = int(selected.split(":")[0])
        incident = incidents[incidents['id'] == incident_id].iloc[0]
        
        # Display incident details before deletion
        st.warning("⚠️ You are about to delete the following incident:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**ID:** {incident['id']}")
            st.write(f"**Title:** {incident['title']}")
            st.write(f"**Type:** {incident['type']}")
        
        with col2:
            st.write(f"**Severity:** {incident['severity']}")
            st.write(f"**Status:** {incident['status']}")
            st.write(f"**Date:** {incident['date']}")
        
        # Confirmation
        confirmation = st.text_input("Type 'DELETE' to confirm", key="delete_confirm")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("Delete Incident", type="primary", disabled=confirmation != "DELETE"):
                try:
                    result = delete_incident(incident_id)
                    st.success(f"✅ Incident {incident_id} deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting incident: {e}")

def main():
    st.title(" Cybersecurity Incidents")
    st.write("View and manage security incidents")
    st.divider()
    
    # Show all incidents
    show_read_form()
    
    st.divider()
    
    # Display statistics
    incidents = get_all_incidents()
    if len(incidents) > 0:
        st.subheader("📊 Incident Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Incidents", len(incidents))
        
        with col2:
            if 'severity' in incidents.columns:
                critical_count = len(incidents[incidents['severity'] == 'Critical'])
                st.metric("🔴 Critical", critical_count)
        
        with col3:
            if 'status' in incidents.columns:
                open_count = len(incidents[incidents['status'] == 'Open'])
                st.metric("🟡 Open", open_count)
        
        with col4:
            if 'status' in incidents.columns:
                resolved_count = len(incidents[incidents['status'] == 'Resolved'])
                st.metric("✅ Resolved", resolved_count)

if __name__ == "__main__":
    main()