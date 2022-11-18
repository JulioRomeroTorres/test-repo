import json
from json import JSONEncoder
from typing import Any
import datetime

class DateEncoder(JSONEncoder):

    def default(self, obj: Any) -> Any:
        if isinstance(obj, (datetime.date, datetime.datetime) ):
            return obj.isoformat()
    
def convert2json(data):
    return json.dumps(data, indent=4, cls=DateEncoder)
    
def convert2dict(current_dict):
    for k,v in current_dict.items():
        new_dict = dict()
        if isinstance(current_dict[k], dict):
            v = convert2dict(current_dict[k])
        if isinstance(current_dict[k], (datetime.date, datetime.datetime)):
            v = current_dict[k].isoformat()
        new_dict[k] = v
    return new_dict

