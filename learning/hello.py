import ollama

response = ollama.chat(
    model="qwen3:4b-instruct",
    messages=[{"role": "user", "content": "Give me one tip for staying focused, in one sentence."}],
)
print(response.message.content)
