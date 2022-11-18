from typing import TypeVar, Any, Callable
import functools
import contextvars
from starlette.responses import JSONResponse
from typing import Dict, Any, TypeVar, Callable
from .utils.function_info import get_path_file
from .utils.clean import req2dict, get_positional_arguments
from .utils.encode_json import convert2json
import time
import json

_TFunc = TypeVar("_TFunc", bound=Callable[..., Any])
class BaseLogger:
    def __init__(self, name: str):
        self.logger = 0
        pass

    def router(self, *, level: str, time_out: float):
        pass

    def database(self, *, level: str, time_out: float):
        pass

    def function(self, *, level: str, time_out: float):
        pass
