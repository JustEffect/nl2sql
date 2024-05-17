from sqlalchemy import create_engine
from config import config


class Database:

    def __init__(self):
        url: str = f"postgresql+psycopg2://{config.database_username}:{config.database_password}@{config.database_host}:{config.database_port}/{config.database_database}"
        self.database_engine = create_engine(url=url)
