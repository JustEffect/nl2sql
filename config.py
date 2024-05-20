from envyaml import EnvYAML


class Config:

    def __init__(self):
        self._config_file: EnvYAML = EnvYAML(yaml_file='config.yaml', strict=False)
        # Database
        self.database_host: str = self._config_file.get('database.host')
        self.database_port: str = self._config_file.get('database.port')
        self.database_username: str = self._config_file.get('database.username')
        self.database_password: str = self._config_file.get('database.password')
        self.database_database: str = self._config_file.get('database.database')
        self.openai_api_key: str = self._config_file.get('openai.apiKey')
        self.openai_model: str = self._config_file.get('openai.model')
        self.openai_temperature: float = self._config_file.get('openai.temperature')
        self.openai_debug: str = self._config_file.get('openai.debug')
        self.app_table_list: [str] = self._config_file.get('app.tables')
        self.database_fetch_size: int = self._config_file.get('app.database_fetch_size')


config: Config = Config()
