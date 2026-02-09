from dotenv import load_dotenv
import os
from groq import Groq
from pathlib import Path

# Load API key
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

# Store conversation history
messages = []

print("🤖 Chatbot started! Type 'exit' to quit.\n")

while True:
    # Get user input
    user_input = input("You: ")
    
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    
    # Add user message to history
    messages.append({"role": "user", "content": user_input})
    
    # Get AI response
    response = client.chat.completions.create(
       model="llama-3.1-8b-instant",
        messages=messages
    )
    
    ai_message = response.choices[0].message.content
    
    # Add AI response to history
    messages.append({"role": "assistant", "content": ai_message})
    
    print(f"Bot: {ai_message}\n")