from typing import Annotated
from langchain_core.tools import tool


@tool
def search_knowledge_base(
    query: Annotated[str, "The search query to find relevant information from uploaded study materials."],
) -> str:
    """
    Search the uploaded study documents for information relevant to the query.
    Use this tool whenever you need to find specific facts, concepts, or details
    from the user's study materials to answer their questions accurately.
    """
    from backend.app.services.rag_service import get_context_string

    context = get_context_string(query, k=5)
    return context
