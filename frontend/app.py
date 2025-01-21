import streamlit as st
import requests
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="ANVE Customer Service AI",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'view' not in st.session_state:
    st.session_state.view = "chat"

# Sidebar for navigation and settings
with st.sidebar:
    st.title("Settings ⚙️")
    st.session_state.api_key = st.text_input("OpenAI API Key", value=st.session_state.api_key, type="password")
    
    st.title("Navigation 🧭")
    view = st.radio("Select View", ["Chat", "Analytics", "System Health"])
    st.session_state.view = view.lower()
    
    if st.button("Check API Health"):
        try:
            response = requests.get("http://localhost:8000/health")
            if response.status_code == 200:
                st.success("API is healthy!")
            else:
                st.error("API is not responding correctly")
        except Exception as e:
            st.error(f"Could not connect to API: {str(e)}")

# Main content area
if st.session_state.view == "chat":
    st.title("ANVE Customer Service AI 🤖")
    st.write("Welcome! How can I assist you today?")

    # Chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "timestamp" in message:
                st.caption(f"Sent at {message['timestamp']}")

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
            st.caption(f"Sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Get AI response
        try:
            if not st.session_state.api_key:
                st.error("Please enter your OpenAI API key in the settings panel")
            else:
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = requests.post(
                            "http://localhost:8000/chat",
                            json={
                                "message": prompt,
                                "api_key": st.session_state.api_key
                            }
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            ai_message = data["response"]
                            st.write(ai_message)
                            st.caption(f"Response time: {data['processing_time']:.2f}s")
                            st.caption(f"Received at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                            
                            # Add AI response to chat history
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": ai_message,
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                        else:
                            st.error("Failed to get response from API")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

elif st.session_state.view == "analytics":
    st.title("Analytics Dashboard 📊")
    
    # Time range selector
    timeframe = st.selectbox(
        "Select Time Range",
        ["1h", "24h", "7d", "30d"],
        index=1
    )
    
    try:
        # Get analytics data
        response = requests.get(f"http://localhost:8000/analytics/metrics?timeframe={timeframe}")
        if response.status_code == 200:
            data = response.json()
            
            # Create metrics columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Interactions", data["total_interactions"])
            
            with col2:
                avg_response_time = sum(data["response_times"].values()) / len(data["response_times"]) if data["response_times"] else 0
                st.metric("Avg Response Time", f"{avg_response_time:.2f}s")
            
            with col3:
                total_errors = sum(data["error_rates"].values())
                st.metric("Total Errors", total_errors)
            
            # Response time graph
            if data["response_times"]:
                st.subheader("Response Times by Endpoint")
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(data["response_times"].keys()),
                        y=list(data["response_times"].values())
                    )
                ])
                fig.update_layout(
                    xaxis_title="Endpoint",
                    yaxis_title="Response Time (s)"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Error rates graph
            if data["error_rates"]:
                st.subheader("Error Rates by Endpoint")
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(data["error_rates"].keys()),
                        y=list(data["error_rates"].values())
                    )
                ])
                fig.update_layout(
                    xaxis_title="Endpoint",
                    yaxis_title="Number of Errors"
                )
                st.plotly_chart(fig, use_container_width=True)
                
        else:
            st.error("Failed to fetch analytics data")
            
    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")

else:  # System Health view
    st.title("System Health Monitor 🏥")
    
    try:
        response = requests.get("http://localhost:8000/analytics/health")
        if response.status_code == 200:
            health_data = response.json()
            
            # Overall status
            status_color = "green" if health_data["status"] == "healthy" else "red"
            st.markdown(f"### Overall Status: <span style='color:{status_color}'>{health_data['status'].upper()}</span>", unsafe_allow_html=True)
            
            # Last check time
            st.markdown(f"Last checked: {health_data['last_check']}")
            
            # Component status
            st.subheader("Component Status")
            for component, status in health_data["components"].items():
                status_color = "green" if status == "operational" else "red"
                st.markdown(f"- {component}: <span style='color:{status_color}'>{status.upper()}</span>", unsafe_allow_html=True)
                
        else:
            st.error("Failed to fetch system health data")
            
    except Exception as e:
        st.error(f"Error loading system health: {str(e)}") 