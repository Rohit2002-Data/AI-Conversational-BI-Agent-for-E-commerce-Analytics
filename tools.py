from langchain.tools import tool
import duckdb
from llm import get_reasoning_llm, get_sql_llm

# Initialize LLMs
reason_llm = get_reasoning_llm()
sql_llm = get_sql_llm()

# Connect to database
con = duckdb.connect("ecommerce.db")


@tool
def generate_sql(user_query: str) -> str:
    """Generate SQL query from user input"""
    
    prompt = f'''
You are an expert SQL generator.

Database Schema:

orders:
- order_id
- user_id
- order_number
- order_dow
- order_hour_of_day
- days_since_prior_order

order_products_prior:
- order_id
- product_id
- add_to_cart_order
- reordered

products:
- product_id
- product_name
- aisle_id
- department_id

aisles:
- aisle_id
- aisle

departments:
- department_id
- department

IMPORTANT RULES:
- Use ONLY the columns listed above
- Use JOINs when needed
- product_name exists ONLY in products table
- reordered exists ONLY in order_products_prior
- Do NOT use columns that do not exist
- Return ONLY SQL (no explanation)

User Query:
{user_query}
'''
    return sql_llm.invoke(prompt).content.strip()


@tool
def execute_sql(query: str) -> str:
    """Execute SQL query and return results"""
    try:
        df = con.execute(query).fetchdf()
        
        if df.empty:
            return "No data found."

        return df.head(20).to_csv(index=False)  # limit output for safety

    except Exception as e:
        return f"ERROR: {str(e)}"


@tool
def fix_sql(input_text: str) -> str:
    """Fix SQL query if execution fails"""
    
    prompt = f'''
You are an expert SQL debugger.

Fix the SQL query based on the error.

Rules:
- Use correct table names
- Use correct columns
- Add JOINs if needed
- Return ONLY corrected SQL

Error + Query:
{input_text}
'''
    return reason_llm.invoke(prompt).content.strip()


@tool
def generate_insights(data: str) -> str:
    """Generate business insights from query results"""
    
    prompt = f'''
You are a data analyst.

Here is the query output:

{data}

Provide:
- 2 clear business insights
- Keep it simple and practical
'''
    return reason_llm.invoke(prompt).content.strip()
