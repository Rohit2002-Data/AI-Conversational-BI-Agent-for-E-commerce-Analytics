from langchain.tools import tool
import duckdb
import re
from llm import get_reasoning_llm, get_sql_llm

reason_llm = get_reasoning_llm()
sql_llm = get_sql_llm()

con = duckdb.connect("ecommerce.db")


@tool
def generate_sql(user_query: str) -> str:
    """Generate SQL query"""

    prompt = f"""
### Task
Generate SQL query.

### RULES:
- Use ONLY given columns
- DO NOT use order_date
- Use order_hour_of_day for time
- Use order_dow for day
- Always return SQL starting with SELECT

### Schema

orders(order_id, user_id, order_number, order_dow, order_hour_of_day, days_since_prior_order)

order_products_prior(order_id, product_id, add_to_cart_order, reordered)

products(product_id, product_name, aisle_id, department_id)

### Question
{user_query}

### SQL Query
"""

    try:
        response = sql_llm.invoke(prompt)

        text = response.content if hasattr(response, "content") else str(response)

        if not text:
            return ""

        text = text.strip().replace("```sql", "").replace("```", "")

        match = re.search(r"(SELECT[\s\S]+)", text, re.IGNORECASE)

        if match:
            sql = match.group(1).strip()

            # 🚨 HARD FIX (prevent order_date error)
            if "order_date" in sql.lower():
                return ""

            return sql

        return ""

    except:
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
