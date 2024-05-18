import logging
from sqlalchemy import text
from config import config
from database import Database

print(f"database host: {config.database_host}")
print(f"database port: {config.database_port}")
print(f"database port: {config.database_username}")
print(f"database port: {config.database_password}")
print(f"database port: {config.database_database}")

# Initiate logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s",
    handlers=[logging.StreamHandler()]
)


db: Database = Database()
result = db.get_connection().execute(text("select * from t_order "))
print(f"result: {result.fetchall()}")

