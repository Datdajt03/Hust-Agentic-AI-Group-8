from typing import Annotated
from langchain_core.tools import tool


@tool
def generate_mindmap(
    topic: Annotated[str, "The topic or concept to create a mind map about."],
) -> str:
    """
    Generate a mind map in Markdown format based on the uploaded study materials.
    Searches the knowledge base for relevant content about the topic,
    then organizes the information into a structured mind map.
    """
    from backend.app.services.rag_service import get_context_string
    from backend.app.config import get_mindmap_llm

    context = get_context_string(topic, k=7)

    llm = get_mindmap_llm(temperature=0.5)

    prompt = f"""Dựa trên nội dung tài liệu học tập dưới đây, hãy tạo một sơ đồ tư duy (mind map) chi tiết về chủ đề "{topic}".

Nội dung tài liệu:
{context}

Yêu cầu:
1. Tạo mind map bằng cú pháp Mermaid (mindmap) để có thể render trực quan.
2. Bao gồm các nhánh chính, nhánh phụ, và các chi tiết quan trọng.
3. Tổ chức logic, dễ hiểu, phù hợp cho việc ôn tập.
4. Sau mind map Mermaid, thêm phần giải thích text cho từng nhánh chính.

Định dạng output:

## 🗺️ Sơ đồ tư duy: {topic}

```mermaid
mindmap
  root(({topic}))
    Nhánh 1
      Chi tiết 1.1
      Chi tiết 1.2
    Nhánh 2
      Chi tiết 2.1
      Chi tiết 2.2
```

## 📝 Giải thích chi tiết

### Nhánh 1: [Tên]
- [Giải thích]

### Nhánh 2: [Tên]
- [Giải thích]
"""

    response = llm.invoke(prompt)
    return response.content
