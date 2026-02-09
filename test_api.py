from dotenv import load_dotenv
import os
from groq import Groq
from pathlib import Path

# Force load from current directory
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Get API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("ERROR: .env file not found or GROQ_API_KEY not set")
    exit(1)

print("✓ API key loaded successfully!")

client = Groq(api_key=api_key)

response = client.chat.completions.create(
   model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Say hello and tell me one fun fact about AI"}]
)

print("\nAI Response:")
print(response.choices[0].message.content)