import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def chat_groq(prompt):
    response_content = ""
    # Start interaction with Groq API
    stream = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=prompt,
        max_tokens=1024,
        temperature=0.9,
        stream=True,
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            response_content += content
    return response_content
