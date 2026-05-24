import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

from backend.app.services.process_data import extract_content_as_string

load_dotenv()

# ── Embedding model ──────────────────────────────────────────────────
_embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

import chromadb

# ── Persistent ChromaDB vectorstore ──────────────────────────────────
_chroma_client = chromadb.CloudClient(
    api_key='ck-13vQibxEbVCGid5fMaj4d5cUQdvND3nKxu3nwLBhB4xt',
    tenant='aca727ff-a3d7-4d72-855d-88c471ec9d52',
    database='husta8'
)

_vectorstore = Chroma(
    client=_chroma_client,
    collection_name="study_documents",
    embedding_function=_embeddings,
)

# ── Text splitter ────────────────────────────────────────────────────
_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""],
)


def ingest_file(file_path: str) -> int:
    """
    Đọc file (PDF/PPTX/DOCX/TXT), trích xuất nội dung,
    chia thành chunks và lưu vào ChromaDB.
    Trả về số chunks đã lưu.
    """
    raw_text = extract_content_as_string(file_path)
    if not raw_text.strip():
        return 0

    chunks = _splitter.split_text(raw_text)

    # Metadata cho mỗi chunk
    metadatas = [
        {"source": os.path.basename(file_path), "chunk_index": i}
        for i in range(len(chunks))
    ]

    _vectorstore.add_texts(texts=chunks, metadatas=metadatas)
    return len(chunks)


def search_documents(query: str, k: int = 5) -> list[dict]:
    """
    Tìm kiếm top-k chunks liên quan nhất từ ChromaDB.
    Trả về list dict {"content": ..., "source": ..., "score": ...}
    """
    results = _vectorstore.similarity_search_with_relevance_scores(query, k=k)
    return [
        {
            "content": doc.page_content,
            "source": doc.metadata.get("source", "unknown"),
            "score": round(score, 4),
        }
        for doc, score in results
    ]


def get_retriever(k: int = 5):
    """Trả về LangChain retriever để dùng trong agent."""
    return _vectorstore.as_retriever(search_kwargs={"k": k})


def get_context_string(query: str, k: int = 5) -> str:
    """
    Tìm kiếm và ghép các chunks thành một string context duy nhất,
    tiện cho việc truyền vào prompt.
    """
    results = search_documents(query, k=k)
    if not results:
        return "Không tìm thấy thông tin liên quan trong tài liệu."
    
    context_parts = []
    for i, r in enumerate(results, 1):
        context_parts.append(f"[{i}] (Nguồn: {r['source']})\n{r['content']}")
    return "\n\n---\n\n".join(context_parts)
