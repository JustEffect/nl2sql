import logging

from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler
from llama_index.llms.openai import OpenAI
from config import config


class Ai:

    def __init__(self):
        logging.info("Initialize AI")
        self._llm = OpenAI(api_key=config.openai_api_key, temperature=config.openai_temperature, model=config.openai_model)
        self._settings()

    def _settings(self):
        Settings.llm = self._llm
        Settings.embed_model = "local"
        if config.openai_debug:
            Settings.callback_manager = CallbackManager(handlers=[LlamaDebugHandler(print_trace_on_end=True)])

    def getLlm(self):
        return self._llm
