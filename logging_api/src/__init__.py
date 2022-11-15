from typing import Dict, Type
from .gcp_log import GcpLogger
from .console_log import ConsoleLogger
from .base_logger import BaseLogger

log_types: Dict[str, Type[BaseLogger]] = {
    "console": ConsoleLogger,
    "gcp": GcpLogger,
}

def rimac_logger(type_logger: str, name: str):
    return log_types[type_logger](name)

