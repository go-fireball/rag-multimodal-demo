from typing import List


def pack_snippets(text_hits: List[dict], fig_hits: List[dict], max_chars=6000) -> str:
    parts = []
    for h in text_hits:
        cite = f"[doc:{h['doc_id']} p:{h['page']}]"
        parts.append(f"TEXT {cite}\n{h['text']}\n")
    for f in fig_hits:
        cite = f"[doc:{f['doc_id']} p:{f['page']}]"
        parts.append(f"FIGURE {cite}\n{f['caption_dense']}\n")
    out = "\n---\n".join(parts)
    return out[:max_chars]
