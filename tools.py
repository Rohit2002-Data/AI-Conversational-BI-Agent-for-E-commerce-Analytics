from langchain.tools import tool
import duckdb
from llm import get_reasoning_llm, get_sql_llm

reason_llm = get_reasoning_llm()
sql_llm = get_sql_llm()
con = duckdb.connect("ecommerce.db")

@tool
def generate_sql(user_query: str) -> str:
    """Generate SQL query from user input"""
    prompt = f'''
You are an expert SQL generator.

Schema:
orders, order_products_prior, products, aisles, departments

Generate SQL for:
{user_query}

Return only SQL.
'''
    return sql_llm.invoke(prompt).content

@tool
def execute_sql(query: str) -> str:
    """Execute SQL query and return results"""
    try:
        df = con.execute(query).fetchdf()
        return df.to_csv(index=False)
    except Exception as e:
        return f"ERROR: {str(e)}"

@tool
def fix_sql(input_text: str) -> str:
    """Fix SQL query if execution fails"""
    prompt = f'''
Fix this SQL error:

{input_text}

Return corrected SQL only.
'''
    return reason_llm.invoke(prompt).content

@tool
def generate_insights(data: str) -> str:
    """Generate business insights from query results"""
    prompt = f'''
Analyze this data and give 2 business insights:

{data}
'''
    return reason_llm.invoke(prompt).content