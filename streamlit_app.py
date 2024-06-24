import streamlit as st
from chat_groq import chat_groq
from summary import summary_groq

st.title("Tech2Biz Translator")

if "history" not in st.session_state:
    st.session_state["history"] = []

if "summary" not in st.session_state:
    st.session_state["summary"] = ""

if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

def submit():
    user_message = st.session_state["user_input"].strip() 
    if user_message:
        history = st.session_state["history"]
        summary = st.session_state["summary"]
        
        system_prompt = f'''
        You are a language translation assistant specializing in converting technical jargon into business-friendly language. Your role is to transform the technical explanations provided by service personnel into concise, clear, simple, and understandable language for business users. Follow these guidelines:
        
        1. Clarity: Use simple, jargon-free language.
        2. Conciseness: Be brief and direct.
        3. Relevance: Highlight what the business user needs to know and its importance.
        4. Tone: Maintain a friendly and professional tone.
        
        Do not mention that you are a business translator. Strictly adhere to the user message and the provided summary only, without including any extra information.
        
        Example:
        - Technical Explanation: "The server experienced a DDoS attack which led to a temporary disruption in service availability due to overwhelming traffic."
        - Business-Friendly Language: "Our server faced a temporary disruption because it received too much traffic at once. We're working on resolving this issue quickly."
        
        Chat Summary:
        {summary}
        '''
        
        summarized_system_prompt = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        prompt_response = chat_groq(summarized_system_prompt)
        history.append((user_message, prompt_response))
        
        st.session_state["current_prompt"] = prompt_response

        current_user_assistant_prompt = [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": prompt_response}
        ]

        st.session_state["summary"] = summary_groq(summary, current_user_assistant_prompt)
        st.session_state["user_input"] = ""  

st.text_area("Enter your message:", key="user_input")
st.button('Submit', on_click=submit)

if "current_prompt" in st.session_state and st.session_state["current_prompt"]:
    st.write(st.session_state["current_prompt"])

with st.expander("Chat Summary"):
    st.write(st.session_state["summary"])

with st.expander("Chat History (Last 4)"):
    for i, (user_msg, assistant_msg) in enumerate(st.session_state["history"][-4:][::-1]):
        st.write(f"{i+1}. User: {user_msg}")
        st.write(f"  Assistant: {assistant_msg}")
