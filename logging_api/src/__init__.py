from typing import Dict, Type
from .gcp_log import GcpLogger
from .console_log import ConsoleLogger
from .base_logger import BaseLogger

log_types: Dict[str, Type[BaseLogger]] = {
    "console": ConsoleLogger,
    "gcp": GcpLogger,
}

log_instances: Dict[str, BaseLogger] = dict()

def rimac_logger(type_logger: str, name: str):
    key = f'{type_logger}_{name}'
    if key in log_instances:
        return log_instances[key]
    log_instances[key] = log_types[type_logger](name)
    return log_instances[key]
