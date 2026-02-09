from dotenv import load_dotenv
import os
from groq import Groq
from pathlib import Path
import json

# Load API key
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Define tools
def calculator(expression):
    """Calculate math expression"""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except:
        return "Error: Invalid expression"

def get_weather(city):
    """Get weather (mock - returns fake data)"""
    return f"Weather in {city}: Sunny, 25°C"

# Tool definitions for LLM
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate math expressions",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression like 2+2"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"}
                },
                "required": ["city"]
            }
        }
    }
]

# Map tool names to functions
available_functions = {
    "calculator": calculator,
    "get_weather": get_weather
}

print("🤖 Chatbot with Tools! Type 'exit' to quit.")
print("Try: 'What is 15 * 23?' or 'Weather in London?'\n")

messages = []

while True:
    user_input = input("You: ")
    
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    
    messages.append({"role": "user", "content": user_input})
    
    # Get response with tool calling
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    message = response.choices[0].message
    
    # Check if tool calls needed
    if message.tool_calls:
        # Add assistant message to history
        messages.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [tc.model_dump() for tc in message.tool_calls]
        })
        
        # Execute each tool
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"🔧 Using tool: {function_name}({function_args})")
            
            # Call the function
            if function_name in available_functions:
                result = available_functions[function_name](**function_args)
                print(f"📊 Result: {result}")
                
                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
        
        # Get final response after tool use
        final_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )
        
        ai_message = final_response.choices[0].message.content
        messages.append({"role": "assistant", "content": ai_message})
        print(f"Bot: {ai_message}\n")
    else:
        # No tools needed, regular response
        ai_message = message.content
        messages.append({"role": "assistant", "content": ai_message})
        print(f"Bot: {ai_message}\n")