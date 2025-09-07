# PDF-based RAG System Demo

A proof-of-concept implementation of Retrieval-Augmented Generation (RAG) focused on processing PDF documents with both text and image extraction capabilities.

## Overview

This project demonstrates a complete RAG pipeline that:
- Ingests PDF documents extracting both text and images
- Chunks text content for optimal retrieval
- Generates vector embeddings for semantic search
- Extracts and processes images from PDFs
- Captions images using Vision Language Models (VLM)
- Stores all data in PostgreSQL for efficient retrieval

## Features

- **PDF Processing**: Extract text and images from PDF documents using pdfplumber and PyMuPDF
- **Semantic Chunking**: Break text into meaningful chunks for better retrieval
- **Vector Embeddings**: Generate embeddings for text and image captions
- **Image Understanding**: Caption images using OpenAI's vision models
- **OCR Integration**: Extract text from images when available
- **Web Interface**: Browse and search through ingested documents

## Project Structure

```
.
├── apps/
│   ├── rag/                     # Python backend for RAG processing
│   │   ├── src/rag/             # Core RAG implementation
│   │   │   ├── ingest_pdf.py    # PDF processing pipeline
│   │   │   ├── db.py            # Database connection handling
│   │   │   ├── embeddings.py    # Vector embedding generation
│   │   │   ├── chunking.py      # Text chunking algorithms
│   │   │   └── caption_vlm.py   # Vision model integration
│   │   ├── samples/             # Sample documents and generated thumbnails
│   │   │   └── images/          # Extracted image thumbnails
│   │   ├── tests/               # Test suite
│   │   └── .env.example         # Environment configuration template
│   └── web/                     # Frontend application
├── infra/                       # Infrastructure configuration
├── docs/                        # Documentation
└── Makefile                     # Build and deployment scripts
```

## Setup

### Prerequisites

- Python 3.12+
- PostgreSQL database
- OpenAI API key

### Configuration

Copy the example environment file and configure your settings:

```bash
cp apps/rag/.env.example apps/rag/.env
```

Required environment variables:

```
DATABASE_URL=postgresql://rag:ragpw@localhost:5433/ragdb
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
OPENAI_EMBED_MODEL=text-embedding-3-small
VLM_MODEL=gpt-4o
```

### Database Setup

The project includes a Docker Compose setup for PostgreSQL with pgvector extension:

```bash
# Start the PostgreSQL database with vector extension support
cd infra
docker-compose up -d
```

This will:
- Start a PostgreSQL 16 instance with pgvector extension at port 5433
- Create the required database schema via initialization scripts
- Launch Adminer database UI available at http://localhost:8080

The database schema includes tables for:
- `documents` - Document metadata
- `chunks` - Text chunks with embeddings
- `figures` - Extracted images with captions and embeddings

## Usage

### Ingesting a PDF

```bash
cd apps/rag
python -m rag.ingest_pdf path/to/your/document.pdf
```

This will:
1. Extract text from the PDF and split into chunks
2. Generate vector embeddings for each chunk
3. Extract images from the PDF
4. Generate captions and OCR for images using VLM
5. Store all information in the database

### Web Interface

The web interface allows browsing and searching through ingested documents.

```bash
cd apps/web
npm run dev
```

## How It Works

### PDF Ingestion Process

1. **Document Registration**: Each PDF is registered with a unique ID
2. **Text Extraction**: Text is extracted and chunked for optimal retrieval
3. **Image Extraction**: Images are extracted directly from the PDF
4. **Image Understanding**: Images are processed by a Vision Language Model to:
   - Generate short captions
   - Generate detailed descriptions
   - Extract text visible in the image (OCR)
   - Identify entities and generate tags
5. **Vector Storage**: All text and image captions are converted to vector embeddings

### Retrieval Process

Queries are processed through a similar pipeline:
1. Convert query to vector embedding
2. Find similar content (text chunks or images) using vector similarity
3. Return relevant information with proper context

## Technical Details

- **Embedding Model**: OpenAI's text-embedding-3-small
- **Vision Model**: OpenAI's GPT-4o for image understanding
- **PDF Processing**: Combination of pdfplumber (text) and PyMuPDF (images)
- **Database**: PostgreSQL with vector extensions

## Contributing

This is a proof-of-concept demonstration. Contributions are welcome to improve:
- Performance optimizations
- Support for additional document types
- Enhanced chunking strategies
- Improved image understanding

## License

