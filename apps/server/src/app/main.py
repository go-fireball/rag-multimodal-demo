from fastapi import FastAPI
from pydantic import BaseModel
from .embeddings import embed_text
from .retrieval import search_text, search_figures
from .context import pack_snippets
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ANSWER_MODEL = os.getenv("ANSWER_MODEL", "gpt-4o")


class QueryReq(BaseModel):
    query: str
    want_figures: bool = True
    k: int = 10


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/query")
def query(req: QueryReq):
    qvec = embed_text(req.query)
    text_hits = search_text(qvec, k=req.k)
    fig_hits = search_figures(qvec, k=min(5, req.k)) if req.want_figures else []

    context = pack_snippets(text_hits, fig_hits)

    system = (
        "You are a precise assistant. Use ONLY the provided snippets. "
        "Cite claims like [doc:ID p:PAGE]. If answers aren't in snippets, say you don't know."
    )

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"Question: {req.query}\n\nSnippets:\n{context}"},
    ]

    resp = client.chat.completions.create(model=ANSWER_MODEL, messages=messages)
    return {
        "answer": resp.choices[0].message.content,
        "text_hits": text_hits,
        "figure_hits": fig_hits,
    }
