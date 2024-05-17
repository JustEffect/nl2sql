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


config: Config = Config()
