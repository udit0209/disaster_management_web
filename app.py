import streamlit as st
from streamlit_option_menu import option_menu
import folium
from streamlit_folium import folium_static
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import os

# Set page config
st.set_page_config(page_title="DisasterSync", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Simulated data
risk_data = pd.DataFrame({
    'lat': [40.7128, 34.0522, 37.7749],
    'lon': [-74.0060, -118.2437, -122.4194],
    'risk_score': [0.8, 0.6, 0.9],
    'disaster_type': ['Flood', 'Earthquake', 'Cyclone']
})

alerts_data = pd.DataFrame({
    'alert_id': [1, 2],
    'severity': ['High', 'Medium'],
    'zone': ['New York', 'Los Angeles'],
    'message': ['Flood Warning: Evacuate low-lying areas.', 'Earthquake Alert: Drop, Cover, Hold On.'],
    'timestamp': [datetime.now(), datetime.now()]
})

resources_data = pd.DataFrame({
    'resource_id': [1, 2, 3],
    'type': ['Rescue Team', 'Medical Aid', 'Shelter'],
    'location': ['New York', 'Los Angeles', 'San Francisco'],
    'status': ['Available', 'Deployed', 'Available']
})

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        "DisasterSync",
        ["Home", "Risk Dashboard", "Early Warning", "Resource Console", "Community App", 
         "Incident Reporting", "Transparency Log", "Engagement Portal", "Responder Toolkit"],
        icons=["house", "map", "bell", "box-arrow-up", "phone", "exclamation-triangle", 
               "journal-text", "people", "tools"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#f8fafc"},
            "icon": {"color": "#1e40af", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#e2e8f0",
            },
            "nav-link-selected": {"background-color": "#1e40af", "color": "white"},
        }
    )

# Page routing
if selected == "Home":
    st.title("Welcome to DisasterSync")
    st.markdown("""
        DisasterSync is an AI-powered platform for disaster preparedness and response. 
        Navigate through the sidebar to access dashboards, alerts, resource management, 
        and community engagement tools designed for crisis managers, responders, and citizens.
    """)
    st.image("https://via.placeholder.com/1200x400.png?text=DisasterSync+Hero+Image", use_container_width=True)

elif selected == "Risk Dashboard":
    st.title("Risk Prediction Dashboard")
    st.markdown("Interactive map showing real-time disaster risk zones and AI-generated risk scores.")
    
    # Map
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
    for _, row in risk_data.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=row['risk_score'] * 20,
            popup=f"{row['disaster_type']}: {row['risk_score']}",
            color='red' if row['risk_score'] > 0.7 else 'orange',
            fill=True,
            fill_color='red' if row['risk_score'] > 0.7 else 'orange'
        ).add_to(m)
    folium_static(m)
    
    # Risk Scores Plot
    fig = px.bar(risk_data, x='disaster_type', y='risk_score', color='risk_score', 
                 title="Risk Scores by Disaster Type")
    st.plotly_chart(fig, use_container_width=True)

elif selected == "Early Warning":
    st.title("Early Warning Panel")
    st.markdown("View and manage alerts with severity, affected zones, and recommended actions.")
    
    for _, alert in alerts_data.iterrows():
        with st.expander(f"Alert ID: {alert['alert_id']} - {alert['severity']}"):
            st.write(f"**Zone**: {alert['zone']}")
            st.write(f"**Message**: {alert['message']}")
            st.write(f"**Timestamp**: {alert['timestamp']}")
            st.button("Approve Alert", key=f"approve_{alert['alert_id']}")
            st.button("Dismiss Alert", key=f"dismiss_{alert['alert_id']}")

elif selected == "Resource Console":
    st.title("Resource Allocation Console")
    st.markdown("Deploy resources using AI-optimized recommendations and track status.")
    
    # Resource Map
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
    for _, res in resources_data.iterrows():
        folium.Marker(
            location=[risk_data.iloc[0]['lat'], risk_data.iloc[0]['lon']],
            popup=f"{res['type']}: {res['status']}",
            icon=folium.Icon(color='blue' if res['status'] == 'Available' else 'green')
        ).add_to(m)
    folium_static(m)
    
    # Resource Table
    st.dataframe(resources_data)
    st.button("Deploy Selected Resources")

elif selected == "Community App":
    st.title("Community App")
    st.markdown("Mobile interface for citizens to receive alerts, request help, and report incidents.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Send Alert")
        st.text_area("Alert Message")
        st.selectbox("Severity", ["Low", "Medium", "High"])
        st.button("Send Alert")
    with col2:
        st.subheader("Request Help")
        st.text_input("Location")
        st.text_area("Description")
        st.button("Submit Request")

elif selected == "Incident Reporting":
    st.title("Incident Reporting System")
    st.markdown("Log incidents, upload media, and provide situational updates.")
    
    st.text_input("Incident Location")
    st.text_area("Incident Description")
    st.file_uploader("Upload Media", accept_multiple_files=True)
    st.selectbox("Severity", ["Low", "Medium", "High"])
    st.button("Submit Incident")

elif selected == "Transparency Log":
    st.title("Transparency & Audit Log")
    st.markdown("Review AI decision rationales, human overrides, and bias audits.")
    
    st.dataframe(pd.DataFrame({
        'Action': ['Alert Issued', 'Resource Deployed'],
        'Timestamp': [datetime.now(), datetime.now()],
        'Rationale': ['High flood risk detected', 'AI recommended deployment'],
        'User': ['System', 'Manager']
    }))

elif selected == "Engagement Portal":
    st.title("Community Engagement Portal")
    st.markdown("Collect feedback, share preparedness resources, and engage citizens.")
    
    st.text_area("Feedback")
    st.button("Submit Feedback")
    st.markdown("### Preparedness Resources")
    st.write("- [Evacuation Guide](https://example.com)")
    st.write("- [Safety Tips](https://example.com)")

elif selected == "Responder Toolkit":
    st.title("Responder Mobile Toolkit")
    st.markdown("Navigation, live updates, and communication tools for first responders.")
    
    st.text_input("Incident Location")
    st.button("Navigate to Incident")
    st.text_area("Status Update")
    st.button("Submit Update")

# Footer
st.markdown("""
    <div class='footer'>
        © 2025 DisasterSync | <a href='#'>Privacy Policy</a> | <a href='#'>Contact Us</a>
    </div>
""", unsafe_allow_html=True)
