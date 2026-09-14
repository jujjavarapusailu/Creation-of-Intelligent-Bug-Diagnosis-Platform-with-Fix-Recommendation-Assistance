import json
from pathlib import Path


# Cleaned dataset location
dataset_path = Path("../datasets/mozilla/cleaned_bugs.json")

# Read cleaned dataset
with open(dataset_path, "r", encoding="utf-8") as file:
    bugs = json.load(file)


# Create text chunks for RAG
chunks = []

for bug in bugs:
    text = f"""
Bug ID: {bug.get('bug_id')}
Title: {bug.get('title')}
Component: {bug.get('component')}
Severity: {bug.get('severity')}
Priority: {bug.get('priority')}
Status: {bug.get('status')}
Operating System: {bug.get('operating_system')}
Keywords: {', '.join(bug.get('keywords', []))}
""".strip()

    chunks.append({
        "bug_id": bug.get("bug_id"),
        "text": text,
        "metadata": {
            "component": bug.get("component"),
            "severity": bug.get("severity"),
            "priority": bug.get("priority"),
            "status": bug.get("status")
        }
    })


# Save chunks
output_path = Path("../datasets/mozilla/bug_chunks.json")

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(chunks, file, indent=4)


print("Total bugs:", len(bugs))
print("Total chunks created:", len(chunks))
print("Chunks saved successfully!")
print("File:", output_path)