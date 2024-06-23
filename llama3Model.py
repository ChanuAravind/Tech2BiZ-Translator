import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

system_prompt = {
    "role": "system",
    "content": '''You are a language translation assistant specializing in converting technical jargon into business-friendly language. Your role is to transform the technical explanations provided by service personnel into concise, clear, simple, and understandable language for business users. Follow these guidelines:

Clarity: Use simple, jargon-free language.
Conciseness: Be brief and direct.
Relevance: Highlight what the business user needs to know and its importance.
Tone: Maintain a friendly and professional tone.

Do not mention that you are a business translator and strictly adhere to the user message only.''',
}

def chat_groq(message, summary):
    messages = [system_prompt]
    if summary:
        messages.append({"role": "system", "content": f"Summary of previous conversation: {summary}"})
    messages.append({"role": "user", "content": message})

    # Print the current output prompt
    print("Current Output Prompt:")
    for msg in messages:
        print(f"{msg['role']}: {msg['content']}")

    response_content = ""
    stream = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        max_tokens=1024,
        temperature=0.9,
        stream=True,
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            response_content += chunk.choices[0].delta.content
    return response_content

def summarize_chat(history):
    summary = ""
    if history:
        all_messages = []
        for role, content in history:
            all_messages.append(f"{role}: {content}")
        summary_prompt = "Summarize the following conversation:\n" + "\n".join(all_messages)
        response_content = chat_groq(summary_prompt, "")  # Pass empty summary for summary prompt
        summary = response_content.strip()  
    return summary