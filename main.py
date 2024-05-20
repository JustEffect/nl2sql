import logging

from llama_index.core import SQLDatabase
from llama_index.core.indices.struct_store import NLSQLTableQueryEngine
from sqlalchemy import text
from config import config
from extensions import database, ai



logging.info(f"database host: {config.database_host}")
logging.info(f"database port: {config.database_port}")
logging.info(f"database port: {config.database_username}")
logging.info(f"database port: {config.app_table_list}")




sql_database = SQLDatabase(database.get_engine())

query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database, tables=config.app_table_list, llm=ai.get_llm()
)
query_str = ("what price each customer spent on their order (dont sum up the price, its already the total) and print their names, price and if they've paid for it or not")
response = query_engine.query(query_str)

logging.info(response)
