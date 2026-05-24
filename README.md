# Hust-Agentic-AI-Group-8

## 📚 Multi-Agent AI Study Assistant

Hệ thống trợ lý học tập AI sử dụng kiến trúc **Multi-Agent** với **LangGraph**, tự động phân tích tài liệu và hỗ trợ ôn tập thông minh.

### 🏗️ Kiến trúc

```
User Input → Supervisor Agent
                ├── 🔍 QA Agent        (trả lời câu hỏi từ tài liệu)
                ├── 📝 Practice Agent   (tạo câu hỏi ôn tập trắc nghiệm)
                └── 🗺️ Mindmap Agent    (tạo sơ đồ tư duy)
```

- **Supervisor** — Phân tích yêu cầu, chuyển task đến agent phù hợp
- **QA Agent** — Tìm kiếm RAG trong ChromaDB, trả lời câu hỏi chính xác
- **Practice Agent** — Tạo bộ câu hỏi trắc nghiệm với đáp án và giải thích
- **Mindmap Agent** — Tạo sơ đồ tư duy Mermaid trực quan

### 🛠️ Tech Stack

| Thành phần | Công nghệ |
|---|---|
| LLM | GPT-4.1-nano (OpenAI) |
| Vision | Gemini 2.5 Flash (Google) |
| Embeddings | Google Embedding-001 |
| Vector DB | ChromaDB |
| Agent Framework | LangGraph + LangChain |
| File Processing | PyMuPDF, python-pptx, python-docx |

### 📦 Cài đặt

```bash
# Clone repo
git clone https://github.com/Datdajt03/Hust-Agentic-AI-Group-8.git
cd Hust-Agentic-AI-Group-8

# Tạo virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Cài dependencies
pip install -r requirements.txt

# Cấu hình API keys
cp .env.example .env
# Sửa file .env, thêm OPENAI_API_KEY và GOOGLE_API_KEY
```

### 🚀 Sử dụng

```bash
# Ingest tài liệu và bắt đầu chat
python -m backend.app.main --ingest path/to/document.pdf

# Chỉ chat (đã ingest trước đó)
python -m backend.app.main
```

**Các lệnh trong chat:**

| Lệnh | Mô tả |
|---|---|
| `/ingest <path>` | Upload thêm tài liệu |
| `/quit` | Thoát chương trình |

**File formats hỗ trợ:** PDF, PPTX, DOCX, TXT

### 📁 Cấu trúc project

```
Hust-Agentic-AI-Group-8/
├── backend/
│   └── app/
│       ├── main.py              # CLI entrypoint
│       ├── config.py            # LLM configuration
│       ├── workflow.py          # LangGraph multi-agent workflow
│       ├── services/
│       │   ├── process_data.py  # File processing (PDF, DOCX, PPTX, TXT)
│       │   └── rag_service.py   # RAG pipeline (ChromaDB)
│       └── tools/
│           ├── handoff_tools.py # Agent routing tools
│           ├── rag_tools.py     # Knowledge base search tool
│           ├── practice_tools.py# Quiz generation tool
│           └── mindmap_tools.py # Mind map generation tool
├── requirements.txt
├── .env.example
└── README.md
```

### 👥 Nhóm 8

Hust Agentic AI — Group 8