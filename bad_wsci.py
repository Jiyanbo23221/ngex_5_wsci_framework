from pathlib import Path
from ollama import chat

question = """
I changed my university password this morning.
Now my Windows laptop won't connect to campus Wi-Fi,
but my phone still works.
"""

context = ""

for file in Path("knowledge").glob("*.txt"):
    context += file.read_text()
    context += "\n\n"

response = chat(
    model="qwen3:8b",
    messages=[
        {"role": "system", "content": "You are a helpful IT support assistant."},
        {"role": "user", "content": f"Student question: {question}\n\nKnowledge base:\n{context}"}
    ]
)

print("Context characters:", len(context))
print(response.message.content)
