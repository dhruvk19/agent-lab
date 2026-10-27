import sys
from datetime import datetime
import ollama

MODEL = "qwen3:4b-instruct"

def get_current_time() -> str:
    """Get the current date and time on this computer."""
    return datetime.now().strftime("%A, %B %d, %Y %I:%M %p")

def add_numbers(a: float, b: float) -> float:
    """Add two numbers together.

    Args:
      a: The first number
      b: The second number
    """
    return float(a) + float(b)

TOOLS = {"get_current_time": get_current_time, "add_numbers": add_numbers}

question = " ".join(sys.argv[1:]) or "What time is it right now?"
messages = [{"role": "user", "content": question}]

response = ollama.chat(model=MODEL, messages=messages, tools=list(TOOLS.values()))

if response.message.tool_calls:
    messages.append(response.message)
    for call in response.message.tool_calls:
        name, args = call.function.name, call.function.arguments
        if name not in TOOLS:
            print(f"[model asked for unknown tool: {name}]")
            continue
        result = TOOLS[name](**args)
        print(f"[model used {name}({args}) -> {result}]")
        messages.append({"role": "tool", "content": str(result), "tool_name": name})
    response = ollama.chat(model=MODEL, messages=messages)

print(response.message.content)
