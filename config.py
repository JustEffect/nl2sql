from envyaml import EnvYAML


class Config:

    def __init__(self):
        self._config_file: EnvYAML = EnvYAML(yaml_file='config.yaml', strict=False)
        # Database
        self.database_host: str = self._config_file.get('database.host')
