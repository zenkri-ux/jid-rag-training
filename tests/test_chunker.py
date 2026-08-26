from app.rag.chunker import chunk_document


def test_chunker_preserves_source_and_section():
    document = {"text": "# Role\nIntro\n## Skills\nPython and SQL", "metadata": {"source": "role.md"}}
    chunks = chunk_document(document, size=100, overlap=10)
    assert chunks
    assert all(chunk["metadata"]["source"] == "role.md" for chunk in chunks)
    assert {chunk["metadata"]["section"] for chunk in chunks} == {"Role", "Skills"}

