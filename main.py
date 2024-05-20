import logging

from llama_index.core import SQLDatabase
from llama_index.core.indices.struct_store import NLSQLTableQueryEngine
from sqlalchemy import text
from config import config
from database import Database
from ai import Ai

# Initiate logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s",
    handlers=[logging.StreamHandler()]
)

logging.info(f"database host: {config.database_host}")
logging.info(f"database port: {config.database_port}")
logging.info(f"database port: {config.database_username}")
logging.info(f"database port: {config.database_database}")

db: Database = Database()
ai = Ai()


sql_database = SQLDatabase(db.get_engine())

query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database, tables=["t_customer", "t_order", "t_order_item", "t_products"], llm=ai.get_llm()
)
query_str = ("what price each customer spent on their order (dont sum up the price, its already the total) and print their names, price and if they've paid for it or not")
response = query_engine.query(query_str)

logging.info(response)
