import re
from pathlib import Path
from typing import Any


FRONT_MATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _value(raw: str) -> Any:
    raw = raw.strip().strip('"').strip("'")
    if raw.isdigit():
        return int(raw)
    return raw


def load_documents(root: Path, include_problematic: bool = True) -> list[dict[str, Any]]:
    documents = []
    for path in sorted(root.rglob("*.md")):
        if not include_problematic and "problematic" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        metadata: dict[str, Any] = {"source": path.name, "path": str(path.relative_to(root)).replace("\\", "/")}
        match = FRONT_MATTER.match(text)
        if match:
            for line in match.group(1).splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = _value(value)
            text = text[match.end():]
        documents.append({"text": text.strip(), "metadata": metadata})
    return documents

