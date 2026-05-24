"""
Multi-Agent Workflow sử dụng LangGraph.

Kiến trúc:
  Supervisor (router) ──┬──> QA Agent       (trả lời câu hỏi)
                        ├──> Practice Agent  (tạo câu hỏi ôn tập)
                        └──> Mindmap Agent   (tạo sơ đồ tư duy)
"""

from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command

from backend.app.config import (
    get_supervisor_llm,
    get_qa_llm,
    get_practice_llm,
    get_mindmap_llm,
)
from backend.app.tools.handoff_tools import (
    assign_to_qa_agent_with_description,
    assign_to_practice_agent_with_description,
    assign_to_mindmap_agent_with_description,
)
from backend.app.tools.rag_tools import search_knowledge_base
from backend.app.tools.practice_tools import generate_quiz
from backend.app.tools.mindmap_tools import generate_mindmap


# ═══════════════════════════════════════════════════════════════════════
# SUPERVISOR — quyết định chuyển task đến agent nào
# ═══════════════════════════════════════════════════════════════════════

SUPERVISOR_SYSTEM_PROMPT = """Bạn là một trợ lý học tập AI thông minh (Supervisor).
Nhiệm vụ của bạn là phân tích yêu cầu của người dùng và chuyển đến agent phù hợp nhất.

Bạn có 3 agents chuyên biệt:
1. **QA Agent** — Trả lời câu hỏi, giải thích khái niệm, tìm kiếm thông tin trong tài liệu
2. **Practice Agent** — Tạo câu hỏi ôn tập, quiz trắc nghiệm
3. **Mindmap Agent** — Tạo sơ đồ tư duy, tổng hợp kiến thức trực quan

Quy tắc:
- Nếu người dùng hỏi/yêu cầu giải thích → chuyển cho QA Agent
- Nếu người dùng muốn ôn tập/luyện tập/quiz → chuyển cho Practice Agent  
- Nếu người dùng muốn tóm tắt/sơ đồ/mindmap → chuyển cho Mindmap Agent
- Nếu không rõ, hãy hỏi lại người dùng

Hãy luôn chuyển task kèm mô tả chi tiết để agent hiểu rõ ngữ cảnh.
"""

supervisor_agent = create_react_agent(
    model=get_supervisor_llm(),
    tools=[
        assign_to_qa_agent_with_description,
        assign_to_practice_agent_with_description,
        assign_to_mindmap_agent_with_description,
    ],
    prompt=SUPERVISOR_SYSTEM_PROMPT,
    name="supervisor",
)


# ═══════════════════════════════════════════════════════════════════════
# QA AGENT — trả lời câu hỏi dựa trên RAG
# ═══════════════════════════════════════════════════════════════════════

QA_SYSTEM_PROMPT = """Bạn là chuyên gia trả lời câu hỏi học tập (QA Agent).

Nhiệm vụ:
- Sử dụng tool search_knowledge_base để tìm thông tin từ tài liệu đã upload
- Trả lời chính xác, chi tiết, dễ hiểu
- Nếu thông tin không có trong tài liệu, hãy nói rõ và cung cấp kiến thức chung nếu có

Phong cách:
- Trả lời bằng tiếng Việt
- Sử dụng bullet points, bold, emoji để dễ đọc
- Trích dẫn nguồn tài liệu khi có thể
"""

qa_agent = create_react_agent(
    model=get_qa_llm(),
    tools=[search_knowledge_base],
    prompt=QA_SYSTEM_PROMPT,
    name="qa_agent",
)


# ═══════════════════════════════════════════════════════════════════════
# PRACTICE AGENT — tạo câu hỏi ôn tập
# ═══════════════════════════════════════════════════════════════════════

PRACTICE_SYSTEM_PROMPT = """Bạn là chuyên gia tạo câu hỏi ôn tập (Practice Agent).

Nhiệm vụ:
- Sử dụng tool generate_quiz để tạo bộ câu hỏi trắc nghiệm từ tài liệu
- Có thể tùy chỉnh số lượng câu hỏi và độ khó theo yêu cầu
- Đảm bảo câu hỏi bám sát nội dung tài liệu đã upload

Mặc định: 5 câu hỏi, độ khó medium. Điều chỉnh theo yêu cầu người dùng.
"""

practice_agent = create_react_agent(
    model=get_practice_llm(),
    tools=[generate_quiz],
    prompt=PRACTICE_SYSTEM_PROMPT,
    name="practice_agent",
)


# ═══════════════════════════════════════════════════════════════════════
# MINDMAP AGENT — tạo sơ đồ tư duy
# ═══════════════════════════════════════════════════════════════════════

MINDMAP_SYSTEM_PROMPT = """Bạn là chuyên gia tạo sơ đồ tư duy (Mindmap Agent).

Nhiệm vụ:
- Sử dụng tool generate_mindmap để tạo sơ đồ tư duy từ tài liệu
- Tổ chức kiến thức một cách trực quan, logic
- Output bao gồm Mermaid diagram và giải thích chi tiết

Hãy tạo mind map bao quát và chi tiết nhất có thể.
"""

mindmap_agent = create_react_agent(
    model=get_mindmap_llm(),
    tools=[generate_mindmap],
    prompt=MINDMAP_SYSTEM_PROMPT,
    name="mindmap_agent",
)


# ═══════════════════════════════════════════════════════════════════════
# BUILD GRAPH — Kết nối tất cả agents lại thành workflow
# ═══════════════════════════════════════════════════════════════════════

def build_graph():
    """
    Xây dựng LangGraph StateGraph:
    START → supervisor → (qa_agent | practice_agent | mindmap_agent) → END
    """
    builder = StateGraph(MessagesState)

    builder.add_node(supervisor_agent)
    builder.add_node(qa_agent)
    builder.add_node(practice_agent)
    builder.add_node(mindmap_agent)

    builder.add_edge(START, "supervisor")
    builder.add_edge("qa_agent", END)
    builder.add_edge("practice_agent", END)
    builder.add_edge("mindmap_agent", END)

    graph = builder.compile()
    return graph
