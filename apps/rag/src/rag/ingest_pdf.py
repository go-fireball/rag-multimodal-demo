import uuid, pdfplumber
from pathlib import Path
from .db import get_conn
from .embeddings import embed_text
from .chunking import split_text_into_chunks
import sys


def insert(sql, params):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, params)


def ingest_pdf(path: str):
    doc_id = uuid.uuid4()
    insert("INSERT INTO documents(doc_id, title, source_uri) VALUES (%s,%s,%s)",
           (str(doc_id), Path(path).name, str(Path(path).resolve())))
    print(f"Ingested {path}")
    # text chunks
    with pdfplumber.open(path) as pdf:
        for pnum, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            for chunk in split_text_into_chunks(text):
                emb = embed_text(chunk)
                insert(
                    "INSERT INTO chunks(chunk_id, doc_id, page, section_path, text, embedding, meta) "
                    "VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (str(uuid.uuid4()), str(doc_id), pnum, None, chunk, emb, None)
                )


# TODO: figure extraction + caption (via VLM), store in figures table


if __name__ == "__main__":
    print(sys.argv[1])
    ingest_pdf(sys.argv[1])
