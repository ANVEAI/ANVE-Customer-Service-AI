import streamlit as st
import requests
from datetime import datetime

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

# Sidebar for settings
with st.sidebar:
    st.title("Settings ⚙️")
    st.session_state.api_key = st.text_input("OpenAI API Key", value=st.session_state.api_key, type="password")
    
    if st.button("Check API Health"):
        try:
            response = requests.get("http://localhost:8000/health")
            if response.status_code == 200:
                st.success("API is healthy!")
            else:
                st.error("API is not responding correctly")
        except Exception as e:
            st.error(f"Could not connect to API: {str(e)}")

# Main chat interface
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
                        ai_message = response.json()["response"]
                        st.write(ai_message)
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