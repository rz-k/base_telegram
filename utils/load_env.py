from dotenv import dotenv_values


class Config:
    def __init__(self, env=".env"):
        self._values = {}

        for key, value in dotenv_values(env).items():
            if value in ['true', "True"]:
                value = True
            elif value in ['false', "False"]:
                value = False
            self._values[key.upper()] = value

    def get(self, key: str, default=None):
        return self._values.get(key.upper(), None)

    def __getattr__(self, key: str):
        return self._values.get(key.upper(), None)


env = Config()
