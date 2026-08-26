import re
from typing import Any


HEADING = re.compile(r"^(#{1,3})\s+(.+)$", re.MULTILINE)


def chunk_document(document: dict[str, Any], size: int, overlap: int) -> list[dict[str, Any]]:
    text = document["text"]
    matches = list(HEADING.finditer(text))
    sections: list[tuple[str, str]] = []
    if matches:
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            sections.append((match.group(2).strip(), text[match.start():end].strip()))
    else:
        sections.append(("Unstructured content", text))

    chunks = []
    for section, section_text in sections:
        start = 0
        while start < len(section_text):
            end = min(start + size, len(section_text))
            if end < len(section_text):
                boundary = section_text.rfind(" ", start, end)
                if boundary > start + size // 2:
                    end = boundary
            content = section_text[start:end].strip()
            if content:
                metadata = {**document["metadata"], "section": section}
                chunks.append({"text": content, "metadata": metadata})
            if end >= len(section_text):
                break
            start = max(end - overlap, start + 1)
    return chunks

