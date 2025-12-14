import streamlit as st
import pandas as pd
import plotly.express as px
from app.data.db import connect_database

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first!")
    st.stop()

with st.sidebar:
    st.write(f"User: {st.session_state.username}")
    st.write(f"Role: {st.session_state.role.upper()}")
    st.divider()

st.title("📊 Dashboard")

col1, col2 = st.columns([3, 1])

with col2:
    dashboard_type = st.selectbox(
        "Select Dashboard",
        ["🔐 Cybersecurity", "🔧 IT Operations", "📈 Data Analysis"],
        key="main_dashboard"
    )

st.divider()

if "Cybersecurity" in dashboard_type:
    st.subheader("🔐 Cybersecurity Dashboard")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        chart_type = st.selectbox(
            "Chart Type",
            ["Bar", "Pie", "Line"],
            key="cyber_chart"
        )
    
    try:
        conn = connect_database()
        incidents_df = pd.read_sql_query(
            "SELECT * FROM cyber_incidents LIMIT 100",
            conn
        )
        conn.close()
        
        if incidents_df.empty:
            st.warning("No incidents data available")
        else:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Incidents", len(incidents_df))
            
            with col2:
                critical = len(incidents_df[incidents_df['severity'].str.lower() == 'critical'])
                st.metric("Critical", critical)
            
            with col3:
                high = len(incidents_df[incidents_df['severity'].str.lower() == 'high'])
                st.metric("High", high)
            
            with col4:
                resolved = len(incidents_df[incidents_df['status'].str.lower() == 'resolved'])
                st.metric("Resolved", resolved)
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Incidents by Severity")
                severity_counts = incidents_df['severity'].value_counts()
                severity_df = severity_counts.reset_index()
                severity_df.columns = ['severity', 'count']
                
                if chart_type == "Bar":
                    fig = px.bar(
                        severity_df,
                        x='severity',
                        y='count',
                        labels={'severity': 'Severity', 'count': 'Count'},
                        color='severity',
                        color_discrete_map={
                            'critical': 'darkred',
                            'high': 'red',
                            'medium': 'orange',
                            'low': 'green'
                        }
                    )
                elif chart_type == "Pie":
                    fig = px.pie(
                        severity_df,
                        values='count',
                        names='severity',
                        title="Severity Distribution"
                    )
                else:
                    fig = px.line(
                        severity_df,
                        x='severity',
                        y='count',
                        markers=True,
                        labels={'severity': 'Severity', 'count': 'Count'}
                    )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Incidents by Status")
                status_counts = incidents_df['status'].value_counts()
                status_df = status_counts.reset_index()
                status_df.columns = ['status', 'count']
                fig = px.pie(
                    status_df,
                    values='count',
                    names='status',
                    title="Status Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            with st.expander("📋 View All Incidents"):
                st.dataframe(incidents_df, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")

elif "IT Operations" in dashboard_type:
    st.subheader("🔧 IT Operations Dashboard")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        chart_type = st.selectbox(
            "Chart Type",
            ["Bar", "Pie", "Line"],
            key="it_chart"
        )
    
    try:
        conn = connect_database()
        tickets_df = pd.read_sql_query(
            "SELECT * FROM it_tickets LIMIT 100",
            conn
        )
        conn.close()
        
        if tickets_df.empty:
            st.warning("No tickets data available")
        else:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Tickets", len(tickets_df))
            
            with col2:
                open_tickets = len(tickets_df[tickets_df['status'].str.lower() == 'open'])
                st.metric("Open", open_tickets)
            
            with col3:
                in_progress = len(tickets_df[tickets_df['status'].str.lower() == 'in progress'])
                st.metric("In Progress", in_progress)
            
            with col4:
                closed = len(tickets_df[tickets_df['status'].str.lower() == 'closed'])
                st.metric("Closed", closed)
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Tickets by Status")
                status_counts = tickets_df['status'].value_counts()
                status_df = status_counts.reset_index()
                status_df.columns = ['status', 'count']
                
                if chart_type == "Bar":
                    fig = px.bar(
                        status_df,
                        x='status',
                        y='count',
                        labels={'status': 'Status', 'count': 'Count'},
                        color='status',
                        color_discrete_map={
                            'open': 'red',
                            'in progress': 'orange',
                            'closed': 'green'
                        }
                    )
                elif chart_type == "Pie":
                    fig = px.pie(
                        status_df,
                        values='count',
                        names='status',
                        title="Status Distribution"
                    )
                else:
                    fig = px.line(
                        status_df,
                        x='status',
                        y='count',
                        markers=True,
                        labels={'status': 'Status', 'count': 'Count'}
                    )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Tickets by Priority")
                priority_counts = tickets_df['priority'].value_counts()
                priority_df = priority_counts.reset_index()
                priority_df.columns = ['priority', 'count']
                fig = px.pie(
                    priority_df,
                    values='count',
                    names='priority',
                    title="Priority Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            with st.expander("📋 View All Tickets"):
                st.dataframe(tickets_df, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")

elif "Data Analysis" in dashboard_type:
    st.subheader("📈 Data Analysis Dashboard")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        chart_type = st.selectbox(
            "Chart Type",
            ["Bar", "Pie", "Scatter"],
            key="data_chart"
        )
    
    try:
        conn = connect_database()
        datasets_df = pd.read_sql_query(
            "SELECT * FROM datasets_metadata LIMIT 100",
            conn
        )
        conn.close()
        
        if datasets_df.empty:
            st.warning("No datasets data available")
        else:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Datasets", len(datasets_df))
            
            with col2:
                unique_categories = datasets_df['category'].nunique()
                st.metric("Categories", unique_categories)
            
            with col3:
                unique_owners = datasets_df['owner'].nunique() if 'owner' in datasets_df.columns else 0
                st.metric("Owners", unique_owners)
            
            with col4:
                st.metric("Records", len(datasets_df))
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Datasets by Category")
                category_counts = datasets_df['category'].value_counts()
                category_df = category_counts.reset_index()
                category_df.columns = ['category', 'count']
                
                if chart_type == "Bar":
                    fig = px.bar(
                        category_df,
                        x='category',
                        y='count',
                        labels={'category': 'Category', 'count': 'Count'},
                        color='count',
                        color_continuous_scale="Blues"
                    )
                elif chart_type == "Pie":
                    fig = px.pie(
                        category_df,
                        values='count',
                        names='category',
                        title="Category Distribution"
                    )
                else:
                    scatter_df = category_df.rename(columns={'category': 'Category', 'count': 'Count'})
                    fig = px.scatter(
                        scatter_df,
                        x='Category',
                        y='Count',
                        size='Count',
                        color='Count',
                        color_continuous_scale="Viridis"
                    )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Data Distribution")
                if 'format' in datasets_df.columns:
                    format_counts = datasets_df['format'].value_counts()
                    format_df = format_counts.reset_index()
                    format_df.columns = ['format', 'count']
                    fig = px.pie(
                        format_df,
                        values='count',
                        names='format',
                        title="Format Distribution"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Format data not available")
            
            st.divider()
            
            with st.expander("📋 View All Datasets"):
                st.dataframe(datasets_df, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")