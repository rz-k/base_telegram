import configparser


class Config:
    def __init__(self, env=".env") -> None:
        config = configparser.ConfigParser(interpolation=None)
        file_name = f"{env}.ini"
        config.read(file_name)

        self._values = {}

        for section_name in config.sections():
            for key, value in config[section_name].items():
                if value in ['true', "True"]:
                    value = True
                elif value in ['false', "False"]:
                    value = False
                self._values[key.upper()] = value

    def get(self, key, default=None):
        return self._values.get(key.upper(), default)

    def __getattr__(self, key):
        return self._values.get(key.upper())

env = Config()
