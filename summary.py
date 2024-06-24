from chat_groq import chat_groq

def summary_groq(summary,current_response):
    
    summary_prompt = []
    summary_prompt.append({"role": "system","content": "Your ability to summarize conversations between the user and the assistant is commendable."})
    summary_prompt.append({"role":"user","content":f'Please update the conversation summary with new response and create a new summary:\n\nConversation Summary:\n{summary}\n\nNew Response:\n{current_response}'})
    
    return chat_groq(summary_prompt)
