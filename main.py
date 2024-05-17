from config import config
from database import Database

print(f"database host: {config.database_host}")
print(f"database port: {config.database_port}")
print(f"database port: {config.database_username}")
print(f"database port: {config.database_password}")
print(f"database port: {config.database_database}")

db: Database = Database()
connection = db.database_engine.connect()
result = connection.execute("select current_timestamp ")
print(f"database host: {config.database_host}")
