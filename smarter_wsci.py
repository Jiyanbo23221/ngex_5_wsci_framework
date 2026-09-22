from pathlib import Path
from ollama import chat
import json

question = """
I changed my university password this morning.
Now my Windows laptop won't connect to campus Wi-Fi,
but my phone still works.
"""

## WRITE ##
service_status = {
    "wifi": "operational"
}

state = {
    "problem": question,
    "wi_fi status": "operational",
    "wi-fi_check": True
}

with open("state.json", "w") as file:
    json.dump(state, file, indent=2)

with open("state.json", "r") as file:
    state = json.load(file)

print(state)

## SELECT CONTEXT FILES BASED ON QUESTION
def select_context(question):
    question_lower = question.lower()
    keyword_map = {
        "password": "knowledge/password_changes.txt",
        "wi-fi": "knowledge/wifi_setup.txt",
        "wifi": "knowledge/wifi_setup.txt",
        "wireless": "knowledge/wifi_setup.txt",
        "service": "knowledge/service_status.txt",
        "status": "knowledge/service_status.txt",
        "email": "knowledge/email_setup.txt",
        "vpn": "knowledge/vpn.txt",
        "print": "knowledge/printing.txt",
        "printer": "knowledge/printing.txt",
        "projector": "knowledge/classroom_projectors.txt",
        "classroom": "knowledge/classroom_projectors.txt"
    }
    selected = []
    for keyword, filepath in keyword_map.items():
        if keyword in question_lower:
            if filepath not in selected:
                selected.append(filepath)
    return selected

selected_files = select_context(question)
print("Selected files:", selected_files)

## READ SELECTED FILES
context = ""
for file in selected_files:
    context += Path(file).read_text()
    context += "\n\n"

## COMPRESS CONTEXT
def compress_context(context, question):
    prompt = f"""You are an IT support assistant. Extract only the information relevant to the following question from the given context. Return a concise summary.

Question: {question}

Context:
{context}
"""
    response = chat(
        model="qwen3:8b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.message.content

compressed_context = compress_context(context, question)

print("Compressed context length:", len(compressed_context))

## Final call for structured output
final_prompt = f"""You are an IT support assistant. Based on the following information, provide a step-by-step solution for the student's problem.

Student question: {question}

Relevant information:
{compressed_context}

Provide your answer in JSON format with keys: "diagnosis", "steps" (list), "additional_notes".
"""

response = chat(
    model="qwen3:8b",
    messages=[{"role": "user", "content": final_prompt}]
)

print(response.message.content)

## WRITE the above output in an artifact called "state"
final_output = response.message.content
try:
    final_data = json.loads(final_output)
except json.JSONDecodeError:
    final_data = {"raw_response": final_output}

state["solution"] = final_data
with open("state.json", "w") as file:
    json.dump(state, file, indent=2)

print("\nUpdated state.json:")
print(json.dumps(state, indent=2))
