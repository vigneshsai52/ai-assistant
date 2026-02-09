"""
AI Assistant with Multiple Tools
- Calculator for math
- Weather lookup (mock)
- Web search simulation
- Current time
"""

from dotenv import load_dotenv
import os
from groq import Groq
from pathlib import Path
import json
from datetime import datetime

# Load API key
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


# ============ TOOLS ============

def calculator(expression: str) -> str:
    """Calculate math expression safely"""
    try:
        # Only allow numbers and basic operators
        allowed = set('0123456789+-*/.() ')
        if not all(c in allowed for c in expression):
            return "Error: Only numbers and + - * / allowed"
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


def get_weather(city: str) -> str:
    """Get current weather (simulated)"""
    # In real app, you'd call weather API
    weathers = ["Sunny, 22°C", "Cloudy, 18°C", "Rainy, 15°C", "Snowy, -2°C"]
    import random
    weather = random.choice(weathers)
    return f"{weather} in {city}"


def search_web(query: str) -> str:
    """Simulate web search"""
    # In real app, you'd use SerpAPI, DuckDuckGo, etc.
    return f"Found 3 results for '{query}': [Result 1], [Result 2], [Result 3]"


def get_current_time() -> str:
    """Get current date and time"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


# ============ SETUP ============

available_functions = {
    "calculator": calculator,
    "get_weather": get_weather,
    "search_web": search_web,
    "get_current_time": get_current_time
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate mathematical expressions like 2+2, 15*8, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression to calculate"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get current date and time",
            "parameters": {"type": "object", "properties": {}}
        }
    }
]


def process_message(user_input: str, messages: list) -> str:
    """Process user message and return AI response"""
    
    messages.append({"role": "user", "content": user_input})
    
    # Get response from LLM
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    message = response.choices[0].message
    
    # Handle tool calls
    if message.tool_calls:
        # Add assistant message with tool calls
        messages.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [tc.model_dump() for tc in message.tool_calls]
        })
        
        # Execute tools
        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            
            print(f"  🔧 Using: {func_name}({func_args})")
            
            if func_name in available_functions:
                result = available_functions[func_name](**func_args)
                print(f"  📊 Result: {result}")
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
        
        # Get final response
        final = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )
        reply = final.choices[0].message.content
    else:
        reply = message.content
    
    messages.append({"role": "assistant", "content": reply})
    return reply


# ============ MAIN ============

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 AI Assistant with Tools")
    print("=" * 50)
    print("\nAvailable capabilities:")
    print("  • Math calculations")
    print("  • Weather lookup")
    print("  • Web search")
    print("  • Current time")
    print("\nType 'exit' to quit\n")
    
    messages = []
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() == 'exit':
            print("\nGoodbye! 👋")
            break
        
        print("  Thinking...")
        reply = process_message(user_input, messages)
        print(f"Bot: {reply}\n")