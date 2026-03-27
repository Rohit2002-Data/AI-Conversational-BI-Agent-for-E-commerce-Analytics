from langchain_community.chat_models import ChatOllama

def get_reasoning_llm():
    return ChatOllama(model="llama3", temperature=0)

def get_sql_llm():
    return ChatOllama(model="sqlcoder", temperature=0)
