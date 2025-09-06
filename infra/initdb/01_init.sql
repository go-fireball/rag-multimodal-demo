CREATE
EXTENSION IF NOT EXISTS vector;

-- Documents
CREATE TABLE IF NOT EXISTS documents
(
    doc_id UUID PRIMARY KEY,
    title TEXT,
    source_uri TEXT,
    ingested_at TIMESTAMP DEFAULT now()
);

-- Text chunks
CREATE TABLE IF NOT EXISTS chunks (
                                      chunk_id UUID PRIMARY KEY,
                                      doc_id UUID REFERENCES documents(doc_id) ON DELETE CASCADE,
    page INT,
    section_path TEXT,
    text TEXT,
    embedding vector(1536),
    meta JSONB
    );
CREATE INDEX IF NOT EXISTS idx_chunks_doc ON chunks(doc_id);
CREATE INDEX IF NOT EXISTS idx_chunks_embed ON chunks USING ivfflat (embedding
    vector_cosine_ops) WITH (lists = 100);
-- Figures (image-derived)
CREATE TABLE IF NOT EXISTS figures (
                                       figure_id UUID PRIMARY KEY,
                                       doc_id UUID REFERENCES documents(doc_id) ON DELETE CASCADE,
    page INT,
    bbox TEXT,
    caption_short TEXT,
    caption_dense TEXT,
    ocr_text TEXT,
    thumb_uri TEXT,
    embedding vector(1536),
    meta JSONB
    );
CREATE INDEX IF NOT EXISTS idx_figures_doc ON figures(doc_id);
CREATE INDEX IF NOT EXISTS idx_figures_embed ON figures USING ivfflat
    (embedding vector_cosine_ops) WITH (lists = 100);