from typing import List


def split_text_into_chunks(text: str, max_tokens: int = 500, overlap: int = 80) -> List[str]:
    # naive token-ish splitter; replace with tiktoken as needed
    words = text.split()
    chunks, i = [], 0
    step = max_tokens - overlap
    while i < len(words):
        chunk = " ".join(words[i:i+max_tokens])
        chunks.append(chunk)
        i += step
    return chunks