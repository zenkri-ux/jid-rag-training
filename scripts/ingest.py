import json
import os
import urllib.request


base_url = os.getenv("ASSISTANT_URL", "http://localhost:8000")
request = urllib.request.Request(f"{base_url}/knowledge/reindex", data=b"", method="POST")
with urllib.request.urlopen(request) as response:
    print(json.dumps(json.load(response), indent=2))
