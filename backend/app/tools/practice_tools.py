from typing import Annotated
from langchain_core.tools import tool


@tool
def generate_quiz(
    topic: Annotated[str, "The topic or concept to generate quiz questions about."],
    num_questions: Annotated[int, "Number of questions to generate (default 5)."] = 5,
    difficulty: Annotated[str, "Difficulty level: 'easy', 'medium', or 'hard'."] = "medium",
) -> str:
    """
    Generate practice quiz questions based on uploaded study materials.
    First searches the knowledge base for relevant content about the topic,
    then creates questions with answer options and explanations.
    """
    from backend.app.services.rag_service import get_context_string
    from backend.app.config import get_practice_llm

    context = get_context_string(topic, k=5)

    llm = get_practice_llm(temperature=0.8)

    prompt = f"""Dựa trên nội dung tài liệu học tập dưới đây, hãy tạo {num_questions} câu hỏi ôn tập với độ khó "{difficulty}".

Nội dung tài liệu:
{context}

Yêu cầu:
- Tạo {num_questions} câu hỏi trắc nghiệm (4 đáp án A, B, C, D)
- Chủ đề: {topic}
- Độ khó: {difficulty}
- Mỗi câu hỏi phải có:
  + Câu hỏi rõ ràng
  + 4 đáp án (A, B, C, D)
  + Đáp án đúng
  + Giải thích ngắn gọn tại sao đáp án đúng

Định dạng output:
**Câu 1:** [câu hỏi]
A. [đáp án]
B. [đáp án]
C. [đáp án]
D. [đáp án]
✅ Đáp án: [X]
💡 Giải thích: [giải thích]
"""

    response = llm.invoke(prompt)
    return response.content
