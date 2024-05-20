import logging

from ai import Ai
from database import Database

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s",
    handlers=[logging.StreamHandler()]
)

database: Database = Database()
ai: Ai = Ai()
