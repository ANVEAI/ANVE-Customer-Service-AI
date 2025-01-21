import streamlit as st
import requests
import json
from datetime import datetime

# Configure the app
st.set_page_config(
    page_title="ANVE Customer Service AI",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# API Configuration
API_URL = "http://localhost:8000"

def login():
    st.sidebar.title("Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        try:
            response = requests.post(
                f"{API_URL}/token",
                data={"username": email, "password": password}
            )
            if response.status_code == 200:
                token = response.json()["access_token"]
                st.session_state.token = token
                st.session_state.authenticated = True
                st.sidebar.success("Successfully logged in!")
            else:
                st.sidebar.error("Invalid credentials")
        except Exception as e:
            st.sidebar.error(f"Error: {str(e)}")

def create_ticket():
    st.subheader("Create New Ticket")
    title = st.text_input("Title")
    description = st.text_area("Description")
    priority = st.selectbox("Priority", ["LOW", "MEDIUM", "HIGH", "URGENT"])
    
    if st.button("Submit Ticket"):
        try:
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            response = requests.post(
                f"{API_URL}/tickets/",
                json={
                    "title": title,
                    "description": description,
                    "priority": priority
                },
                headers=headers
            )
            if response.status_code == 200:
                st.success("Ticket created successfully!")
                return response.json()["id"]
            else:
                st.error("Failed to create ticket")
        except Exception as e:
            st.error(f"Error: {str(e)}")

def chat_interface(ticket_id):
    st.subheader("Chat with AI Assistant")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        try:
            # Send message to API
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            response = requests.post(
                f"{API_URL}/chat/{ticket_id}",
                json={"message": prompt},
                headers=headers
            )
            
            if response.status_code == 200:
                ai_response = response.json()["response"]
                # Add AI response to chat history
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
                # Display AI response
                with st.chat_message("assistant"):
                    st.write(ai_response)
            else:
                st.error("Failed to get response from AI")
        except Exception as e:
            st.error(f"Error: {str(e)}")

def main():
    st.title("ANVE Customer Service AI")
    
    if not st.session_state.authenticated:
        login()
    else:
        # Sidebar navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["New Ticket", "My Tickets", "Chat"])
        
        if page == "New Ticket":
            ticket_id = create_ticket()
            if ticket_id:
                st.session_state.current_ticket = ticket_id
                st.session_state.messages = []
        
        elif page == "My Tickets":
            try:
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                response = requests.get(f"{API_URL}/tickets/", headers=headers)
                if response.status_code == 200:
                    tickets = response.json()
                    for ticket in tickets:
                        st.write(f"Ticket #{ticket['id']}: {ticket['title']}")
                        st.write(f"Status: {ticket['status']}")
                        st.write(f"Created: {ticket['created_at']}")
                        st.write("---")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        elif page == "Chat":
            if "current_ticket" in st.session_state:
                chat_interface(st.session_state.current_ticket)
            else:
                st.warning("Please create or select a ticket first")

if __name__ == "__main__":
    main() 