from langchain.agents import initialize_agent, AgentType
from langchain_core.prompts import ChatPromptTemplate

from tools import generate_sql, execute_sql, fix_sql, generate_insights
from llm import get_reasoning_llm


def create_agent():
    llm = get_reasoning_llm()
    tools = [generate_sql, execute_sql, fix_sql, generate_insights]

    system_prompt = '''
You are an AI BI Agent.

Steps:
1. Understand query
2. Use generate_sql
3. Use execute_sql
4. If error → use fix_sql
5. Then generate insights

Always use tools.
'''

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    return agent
