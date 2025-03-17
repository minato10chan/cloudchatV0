import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="💬",
    layout="centered",
)

# App title and description
st.title("AI Chatbot")
st.markdown("""
This is a simple AI chatbot built with Streamlit and powered by OpenAI's API.
Enter your message below to start chatting!
""")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for user message
prompt = st.chat_input("Enter your message here...")

# Function to generate response from OpenAI
def generate_response(prompt, history):
    # Prepare messages for the API call
    messages = [
        {"role": "system", "content": "You are a helpful, friendly, and knowledgeable assistant."}
    ]
    
    # Add chat history
    for message in history:
        messages.append({"role": message["role"], "content": message["content"]})
    
    # Add user's new prompt
    messages.append({"role": "user", "content": prompt})
    
    try:
        # Make the API call
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Handle user input and generate response
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant thinking indicator
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        # Generate and display assistant response
        response = generate_response(prompt, st.session_state.messages[:-1])
        message_placeholder.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Add a sidebar with information
with st.sidebar:
    st.title("About")
    st.markdown("""
    This chatbot uses OpenAI's API to generate responses.
    
    To use this application:
    1. Type your message in the input field
    2. Press Enter to send
    3. Wait for the AI to respond
    
    Your chat history will be preserved during your session.
    """)
    
    # Add API key input
    if not os.getenv("OPENAI_API_KEY"):
        st.warning("OpenAI API key not found in environment variables.")
        api_key = st.text_input("Enter your OpenAI API key:", type="password")
        if api_key:
            openai.api_key = api_key
            st.success("API key set successfully!")
    
    # Add a clear button
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.experimental_rerun()
    
    st.divider()
    st.caption("© 2023 AI Chatbot")
