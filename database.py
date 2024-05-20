import logging

from sqlalchemy import create_engine, Connection, Engine
from config import config


class Database:

    def __init__(self):
        logging.info("initialize database")
        self._engine: Engine = self._create_engine()
        self._connection: Connection = self._engine.connect().execution_options(stream_results=True)

    def __del__(self):
        logging.info("close connection to database")
        self._disconnect()

    def _disconnect(self):
        self._connection.close()

    @staticmethod
    def _create_engine() -> Engine:
        url: str = f"postgresql+psycopg2://{config.database_username}:{config.database_password}@{config.database_host}:{config.database_port}/{config.database_database}"
        return create_engine(url=url)

    def get_engine(self) -> Engine:
        return self._engine

    def get_connection(self) -> Connection:
        return self._connection
