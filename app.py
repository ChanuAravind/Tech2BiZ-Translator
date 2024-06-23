from llama3Model import chat_groq, summarize_chat  # Assuming correct import path for your model functions
import streamlit as st

# Streamlit app setup
st.title("Tech2Biz Translator")

# Initialize session state variables
if "history" not in st.session_state:
    st.session_state["history"] = []

if "summary" not in st.session_state:
    st.session_state["summary"] = ""

if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# Function to process user input and update session state
def submit():
    user_message = st.session_state["user_input"].strip()  # Ensure input is cleaned up
    if user_message:
        history = st.session_state["history"]
        current_prompt = chat_groq(user_message, history)  # Call chat_groq with user message and history
        history.append((user_message, current_prompt))
        st.session_state["current_prompt"] = current_prompt
        st.session_state["summary"] = summarize_chat(history)
        st.session_state["user_input"] = ""  # Clear the input field

# Input text field with button trigger
st.text_area("Enter your message:", key="user_input")
st.button('Submit', on_click=submit)  

# Display the current output prompt if available
if "current_prompt" in st.session_state and st.session_state["current_prompt"]:
    st.write(st.session_state["current_prompt"])

# Display Chat Summary with expander
with st.expander("Chat Summary"):
    st.write(st.session_state["summary"])

# Display Chat History with expander
with st.expander("Chat History (Last 4)"):
    for i, (user_msg, assistant_msg) in enumerate(st.session_state["history"][-4:][::-1]):
        st.write(f"{i+1}. User: {user_msg}")
        st.write(f"  Assistant: {assistant_msg}")
