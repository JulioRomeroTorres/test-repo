from typing import Dict, Any, TypeVar, Callable
import json
from .utils.clean import req2dict, get_positional_arguments
from .utils.function_info import get_path_file
import time
from starlette.responses import JSONResponse
from .base_logger import BaseLogger
import contextvars
import functools

import logging
_TFunc = TypeVar("_TFunc", bound=Callable[..., Any])

class ConsoleLogger(BaseLogger):

    def __init__(self,name) -> None:
        self.trace_console = contextvars.ContextVar("console", default=None)
        self.logger_console = logging.getLogger(name)

    def router( self, *, level: str = "DEBUG", time_out: float = 15.0 ):

        def wrapper_aux(func: _TFunc) -> _TFunc :
            @functools.wraps(func)
            async def wrapper( *args, **kwargs ):
                json_request     = req2dict(kwargs)
                json_arguments   = get_positional_arguments(list(args))
                start_time = time.time()

                function_name, file_path = get_path_file(func)

                data_json = dict()
                common_payload = dict(
                            trace = self.trace_console.get(),
                            input_logging = {**json_request, **json_arguments},
                            function_name = func.__name__,
                            script_path =  file_path,
                            level_logging = level
                )
                try:
                    fastApiResponse : JSONResponse = await func( *args, **kwargs )
                    json_response: Dict = json.loads(fastApiResponse.body.decode())
                    
                    success_payload  = dict(
                            ouput_logging = json_response,
                            elapsed_time_s= time.time()- start_time,
                            error_message= None
                        )
                    
                    data_json = { **common_payload, **success_payload}

                    if data_json['elapsed_time_s'] > time_out:
                        data_json['level_logging'] = "WARNING"
                        data_json['error_message'] = "Time Out in function"

                except Exception as e:
                    
                    fail_payload = dict(
                            error_message= str(e),
                            level_logging = "ERROR"
                        )

                    data_json = { **common_payload, **fail_payload}
                    
                    raise e

                self.logger_console.debug(json.dumps(data_json))

                return fastApiResponse

            return wrapper
        
        return wrapper_aux

    def database( self,  *, level: str = "INFO", time_out: float = 10.0 ) -> _TFunc:

        def wrapper_aux(func: _TFunc) -> _TFunc :
            @functools.wraps(func)
            async def wrapper( *args, **kwargs ):
                json_request     = req2dict(kwargs)
                json_arguments   = get_positional_arguments(list(args))
                start_time = time.time()

                function_name, file_path = get_path_file(func)
                
                data_json = dict()
                common_payload = dict(
                            trace = self.trace_console.get(),
                            input_logging = {**json_request, **json_arguments},
                            function_name = func.__name__,
                            script_path =  file_path,
                            level_logging = level
                )
                try:
                    fastApiResponse : JSONResponse = await func( *args, **kwargs )
                    json_response: Dict = json.loads(fastApiResponse.body.decode())
                    
                    success_payload  = dict(
                            ouput_logging = json_response,
                            elapsed_time_s= time.time()- start_time,
                            error_message= None
                        )
                    
                    data_json = { **common_payload, **success_payload}

                    if data_json['elapsed_time_s'] > time_out:
                        data_json['level_logging'] = "WARNING"
                        data_json['error_message'] = "Time Out in function"

                except Exception as e:
                    
                    fail_payload = dict(
                            error_message= str(e),
                            level_logging = "ERROR"
                        )

                    data_json = { **common_payload, **fail_payload}

                    raise e

                self.logger_console.debug(json.dumps(data_json))
                return fastApiResponse

            return wrapper
        
        return wrapper_aux

    def function( self,  *, level: str, time_out: float ) -> _TFunc:
        def wrapper_aux(func: _TFunc) -> _TFunc :
            @functools.wraps(func)
            async def wrapper( *args, **kwargs ):
                json_request     = req2dict(kwargs)
                json_arguments   = get_positional_arguments(list(args))
                start_time = time.time()

                function_name, file_path = get_path_file(func)

                data_json = dict()
                common_payload = dict(
                            trace = self.trace_console.get(),
                            input_logging = {**json_request, **json_arguments},
                            function_name = func.__name__,
                            script_path =  file_path,
                            level_logging = level
                )

                try:
                    fastApiResponse : JSONResponse = await func( *args, **kwargs )
                    json_response: Dict = json.loads(fastApiResponse.body.decode())
                    
                    success_payload  = dict(
                            ouput_logging = json_response,
                            elapsed_time_s= time.time()- start_time,
                            error_message= None
                        )
                    
                    data_json = { **common_payload, **success_payload}

                    if data_json['elapsed_time_s'] > time_out:
                        data_json['level_logging'] = "WARNING"
                        data_json['error_message'] = "Time Out in function"

                    

                except Exception as e:
                    
                    fail_payload = dict(
                            error_message= str(e),
                            level_logging = "ERROR"
                        )

                    data_json = { **common_payload, **fail_payload}

                    raise e
                
                self.logger_console.debug(json.dumps(data_json))

                return fastApiResponse

            return wrapper
        
        return wrapper_aux






                