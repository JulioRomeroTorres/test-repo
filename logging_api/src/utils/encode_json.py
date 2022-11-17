import json
from json import JSONEncoder
from typing import Any
import datetime

class DateEncoder(JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, (datetime.date, datetime.datetime) ):
            return obj.isoformat()
