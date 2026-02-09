# AI Assistant with Tools

A Python-based AI assistant that uses LLM function calling to perform multiple tasks.

## Features

- **Calculator**: Solve mathematical expressions
- **Weather**: Get current weather for any city (simulated)
- **Web Search**: Search for information (simulated)
- **Time**: Get current date and time
- **Conversation Memory**: Remembers context throughout the chat

## Tech Stack

- Python
- Groq API (Llama 3.1)
- Function Calling / Tool Use

## Setup

1. Clone the repository
2. Create `.env` file with your Groq API key:
GROQ_API_KEY=your_key_here

3. Install dependencies:
pip install groq python-dotenv

Run:
python ai_assistant.py

Demo

You: What is 25 * 48?
  🔧 Using: calculator({'expression': '25 * 48'})
  📊 Result: 1200
Bot: 25 * 48 = 1200

You: Weather in London?
  🔧 Using: get_weather({'city': 'London'})
  📊 Result: Cloudy, 18°C in London
Bot: The weather in London is cloudy with a temperature of 18°C.

Author  
Vignesh Sai
