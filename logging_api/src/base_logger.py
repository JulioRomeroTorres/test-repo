class BaseLogger:
    def __init__(self, name: str):
        pass

    def router(self, *, level: str, time_out: float):
        pass

    def database(self, *, level: str, time_out: float):
        pass

    def function(self, *, level: str, time_out: float):
        pass
