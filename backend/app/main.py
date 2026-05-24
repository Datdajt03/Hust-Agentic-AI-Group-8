"""
CLI Entrypoint cho Multi-Agent AI Study Assistant.

Usage:
    python -m backend.app.main                          # Interactive mode
    python -m backend.app.main --ingest path/to/file    # Ingest file rồi chat
"""

import os
import sys
import argparse
from dotenv import load_dotenv

load_dotenv()


def print_banner():
    print()
    print("=" * 60)
    print("  📚 Multi-Agent AI Study Assistant")
    print("  Hust Agentic AI — Group 8")
    print("=" * 60)
    print()
    print("  Agents:")
    print("    🔍 QA Agent       — Trả lời câu hỏi")
    print("    📝 Practice Agent — Tạo câu hỏi ôn tập")
    print("    🗺️  Mindmap Agent  — Tạo sơ đồ tư duy")
    print()
    print("  Commands:")
    print("    /ingest <path>  — Upload thêm tài liệu")
    print("    /quit           — Thoát chương trình")
    print()
    print("-" * 60)


def ingest_file(file_path: str):
    """Ingest file vào ChromaDB."""
    from backend.app.services.rag_service import ingest_file as _ingest

    if not os.path.isfile(file_path):
        print(f"  ❌ File không tồn tại: {file_path}")
        return

    print(f"  📄 Đang xử lý: {os.path.basename(file_path)} ...")
    try:
        num_chunks = _ingest(file_path)
        print(f"  ✅ Đã lưu {num_chunks} chunks vào knowledge base!")
    except Exception as e:
        print(f"  ❌ Lỗi khi xử lý file: {e}")


def run_chat():
    """Interactive chat loop."""
    from langchain_core.messages import HumanMessage
    from backend.app.workflow import build_graph

    print("  🔨 Đang khởi tạo workflow ...")
    graph = build_graph()
    print("  ✅ Sẵn sàng! Hãy đặt câu hỏi.\n")

    while True:
        try:
            user_input = input("  🧑 Bạn: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  👋 Tạm biệt!")
            break

        if not user_input:
            continue

        if user_input.lower() == "/quit":
            print("  👋 Tạm biệt!")
            break

        if user_input.lower().startswith("/ingest "):
            path = user_input[8:].strip()
            ingest_file(path)
            continue

        print("  🤖 Đang xử lý ...\n")

        try:
            result = graph.invoke(
                {"messages": [HumanMessage(content=user_input)]}
            )

            # Lấy message cuối cùng từ agent
            last_msg = result["messages"][-1]
            print(f"  🤖 Trợ lý: {last_msg.content}\n")

        except Exception as e:
            print(f"  ❌ Lỗi: {e}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Multi-Agent AI Study Assistant"
    )
    parser.add_argument(
        "--ingest",
        type=str,
        nargs="+",
        help="Đường dẫn file(s) cần ingest vào knowledge base",
    )

    args = parser.parse_args()

    print_banner()

    # Ingest files nếu được chỉ định
    if args.ingest:
        for path in args.ingest:
            ingest_file(path)
        print()

    # Chạy interactive chat
    run_chat()


if __name__ == "__main__":
    main()
