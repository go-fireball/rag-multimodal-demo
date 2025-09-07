from .db import get_conn


def search_text(query_vec: list[float], k: int = 10):
    sql = """
          SELECT chunk_id, doc_id, page, section_path, text,
                 1 - (embedding <=> %s::vector) AS score
          FROM chunks
          ORDER BY embedding <=> %s::vector
              LIMIT %s \
          """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (query_vec, query_vec, k))
        return cur.fetchall()


def search_figures(query_vec: list[float], k: int = 10):
    sql = """
          SELECT figure_id, doc_id, page, caption_dense, thumb_uri,
                 1 - (embedding <=> %s::vector) AS score
          FROM figures
          ORDER BY embedding <=> %s::vector
              LIMIT %s \
          """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (query_vec, query_vec, k))
        return cur.fetchall()