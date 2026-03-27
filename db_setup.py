import duckdb

def load_database():
    con = duckdb.connect("ecommerce.db")

    con.execute("CREATE TABLE IF NOT EXISTS orders AS SELECT * FROM 'data/orders.csv'")
    con.execute("CREATE TABLE IF NOT EXISTS order_products_prior AS SELECT * FROM 'data/order_products__prior.csv'")
    con.execute("CREATE TABLE IF NOT EXISTS order_products_train AS SELECT * FROM 'data/order_products__train.csv'")
    con.execute("CREATE TABLE IF NOT EXISTS products AS SELECT * FROM 'data/products.csv'")
    con.execute("CREATE TABLE IF NOT EXISTS aisles AS SELECT * FROM 'data/aisles.csv'")
    con.execute("CREATE TABLE IF NOT EXISTS departments AS SELECT * FROM 'data/departments.csv'")

    return con
