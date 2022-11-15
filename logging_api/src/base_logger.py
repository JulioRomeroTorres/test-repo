class BaseLogger:
    def __init__(self, name: str):
        pass

    def router(self, *, level: str, timeout: float):
        pass

    def database(self, *, level: str, timeout: float):
        pass

    def function(self, *, level: str, timeout: float):
        pass
