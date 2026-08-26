import json
import os
import urllib.request
from pathlib import Path


BASE_URL = os.getenv("ASSISTANT_URL", "http://localhost:8000")
questions = json.loads(Path("tests/evaluation_questions.json").read_text(encoding="utf-8"))
for item in questions:
    payload = json.dumps({"message": item["question"], "conversation_id": f"eval-{item['id']}"}).encode()
    request = urllib.request.Request(f"{BASE_URL}/chat", data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request) as response:
        result = json.load(response)
    print(f"\n[{item['id']}] {item['category']}\n{result['answer']}\nSources: {result['sources']}")

