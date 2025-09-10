from langchain_openai import ChatOpenAI



# Supervisor LLM
def get_supervisor_llm(temperature: float = 0.7, top_p: float = 0.8):
    return ChatOpenAI(
        model="gpt-4.1-nano",
        temperature=temperature,
        top_p=top_p,
    )


# QA LLM
def get_qa_llm(temperature: float = 0.7, top_p: float = 0.8):
    return ChatOpenAI(
        model="gpt-4.1-nano",
        temperature=temperature,
        top_p=top_p,
    )


# Practice LLM
def get_practice_llm(temperature: float = 0.7, top_p: float = 0.8):
    return ChatOpenAI(
        model="gpt-4.1-nano",
        temperature=temperature,
        top_p=top_p,
    )


# Mindmap LLM
def get_mindmap_llm(temperature: float = 0.7, top_p: float = 0.8):
    return ChatOpenAI(
        model="gpt-4.1-nano",
        temperature=temperature,
        top_p=top_p,
    )