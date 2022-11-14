from typing import Dict, Any, List
import json
from pydantic import BaseModel

def req2dict(reqData: Dict) -> Dict:
    request: Dict = dict()
    for k, v in reqData.items():
        if isinstance(v, BaseModel):
            request[k] = json.loads(v.json())
    return request

def get_positional_arguments(args: List[Any]) -> List[str]:
    res = []
    for v in args:
        if isinstance(v, BaseModel):
            res.append(json.loads(v.json()))
    return res