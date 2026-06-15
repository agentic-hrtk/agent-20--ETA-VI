"""Customer data extraction from source systems — NexaCorp."""
import os
import snowflake.connector

def get_snowflake_conn():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        schema="PUBLIC",
    )

def extract_customers(since_date: str):
    conn = get_snowflake_conn()
    cur  = conn.cursor()
    cur.execute(
        "SELECT customer_id, full_name, email, phone, credit_score "
        "FROM customers_prod WHERE updated_at >= %s",
        (since_date,)
    )
    return cur.fetchall()
