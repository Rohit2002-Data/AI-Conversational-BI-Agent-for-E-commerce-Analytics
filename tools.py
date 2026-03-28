from langchain.tools import tool
import duckdb
import re
from llm import get_reasoning_llm, get_sql_llm

reason_llm = get_reasoning_llm()
sql_llm = get_sql_llm()

con = duckdb.connect("ecommerce.db")


@tool
def generate_sql(user_query: str) -> str:
    """Generate SQL query from user input"""

    prompt = f"""
### Task
Generate a SQL query for the given question.

### STRICT RULES:
- Use ONLY the columns listed below
- DO NOT invent columns (NO order_date ❌)
- Use proper JOIN when needed
- Return ONLY SQL
- SQL must start with SELECT

### DATABASE SCHEMA

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

order_products_train:
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

### COLUMN HINTS:
- order_hour_of_day → hour (0–23)
- order_dow → day of week (0–6)
- reordered → 1 means reordered
- product_name is in products table

### EXAMPLES:

Q: How many orders are there?
SQL: SELECT COUNT(*) FROM orders;

Q: Orders by hour
SQL: SELECT order_hour_of_day, COUNT(*) FROM orders GROUP BY order_hour_of_day;

Q: Top products
SQL: SELECT p.product_name, COUNT(*) 
FROM order_products_prior opp
JOIN products p ON opp.product_id = p.product_id
GROUP BY p.product_name
ORDER BY COUNT(*) DESC
LIMIT 5;

### USER QUESTION:
{user_query}

### SQL:
"""

    response = sql_llm.invoke(prompt)

    text = response.content if hasattr(response, "content") else str(response)

    if not text:
        return ""

    import re
    text = text.replace("```sql", "").replace("```", "").strip()

    match = re.search(r"(SELECT[\s\S]+)", text, re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return ""


@tool
def execute_sql(query: str) -> str:
    """Execute SQL"""

    try:
        if not query:
            return "ERROR: SQL generation failed"

        if "order_date" in query.lower():
            return "ERROR: Invalid column 'order_date'"

        if not query.lower().startswith("select"):
            return "ERROR: Only SELECT allowed"

        df = con.execute(query).fetchdf()

        if df.empty:
            return "No data found"

        return df.to_csv(index=False)

    except Exception as e:
        return f"ERROR: {str(e)}"


@tool
def generate_insights(data: str) -> str:
    """Generate insights"""

    prompt = f"""
You are a business analyst.

Data:
{data}

Give 2 short business insights.
"""

    return reason_llm.invoke(prompt).content.strip()
