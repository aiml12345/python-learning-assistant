import streamlit as st
from dotenv import load_dotenv

# Load secrets from .env file BEFORE importing anything that uses them
load_dotenv()

from chatbot import get_response
from config import APP_TITLE, APP_ICON, APP_DESCRIPTION, PAGE_LAYOUT

# Page configuration
st.set_page_config(
    page_title=APP_TITLE.replace("🐍 ", ""),
    page_icon=APP_ICON,
    layout=PAGE_LAYOUT
)

# --- Initialize chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.title("📚 About")
    st.markdown("""
    **Python Learning Assistant**
    
    A single-domain chatbot that answers 
    only Python programming questions.
    """)
    
    st.divider()
    
    # 📝 EDIT THESE LINES WITH YOUR REAL INFORMATION
    st.markdown("""
    **👥 Team:** Your Name 1, Your Name 2, Your Name 3, Your Name 4  
    **🏫 College:** Your College Name  
    **👨‍🏫 Guide:** Your Guide Name  
    **📅 Year:** 2026
    """)
    
    st.divider()
    
    st.markdown("""
    💡 **Tip:** Ask about variables, loops, functions, 
    OOP, file handling, and more!
    """)
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ============================================
# MAIN CONTENT
# ============================================
st.title(APP_TITLE)
st.markdown(APP_DESCRIPTION)

# --- Display chat history ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User input ---
user_question = st.chat_input("Ask a Python question...")

if user_question:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_question})
    
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_question)
    
    # Show spinner while AI thinks (only for API calls)
    with st.spinner("🤔 PyGuide is thinking..."):
        bot_response = get_response(user_question)
    
    # Add bot response to history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    
    # Show bot response
    with st.chat_message("assistant"):
        st.markdown(bot_response)