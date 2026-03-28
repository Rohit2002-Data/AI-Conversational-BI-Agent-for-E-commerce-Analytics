import duckdb
import streamlit as st

@st.cache_resource
def load_database():
    con = duckdb.connect("ecommerce.db")

    con.execute("CREATE OR REPLACE TABLE orders AS SELECT * FROM 'data/orders.csv'")
    con.execute("CREATE OR REPLACE TABLE order_products_prior AS SELECT * FROM 'data/order_products__prior.csv'")
    con.execute("CREATE OR REPLACE TABLE products AS SELECT * FROM 'data/products.csv'")

    return con
