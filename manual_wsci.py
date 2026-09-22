from pathlib import Path
from ollama import chat

question = """
I changed my university password this morning.
Now my Windows laptop won't connect to campus Wi-Fi,
but my phone still works.
"""

selected_files = [
    "knowledge/wifi_setup.txt",
    "knowledge/password_changes.txt",
    "knowledge/service_status.txt"
]

context = ""

for file in selected_files:
    context += Path(file).read_text()
    context += "\n\n"

response = chat(
    model="qwen3:8b",
    messages=[
        {"role": "system", "content": "You are a helpful IT support assistant."},
        {"role": "user", "content": f"Student question: {question}\n\nRelevant knowledge:\n{context}"}
    ]
)

print("Context characters:", len(context))
print(response.message.content)
