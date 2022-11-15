from starlette.responses import JSONResponse
from typing import Dict, Any, TypeVar, Callable
import json 
import time
import google.cloud.logging
import contextvars
import functools

from .utils.clean import req2dict, get_positional_arguments

_TFunc = TypeVar("_TFunc", bound=Callable[..., Any])

class gcp_logger:

    def __init__(self,name) -> None:
        self.trace_gcp = contextvars.ContextVar("request_id", default=None)
        self.trace_aws = contextvars.ContextVar("request_id2", default=None)
        self.client = google.cloud.logging.Client()
        self.logger_gcp = self.client.logger(name)
    
    def send_logging_to_gcp(self, data_json):
        self.logger_gcp.log_struct(data_json, severity=data_json['level_logging'], trace = self.trace_gcp.get())

    def log_api( self, level: str, time_out: float ) -> _TFunc:

        def wrapper_aux(function) -> _TFunc :
            @functools.wraps(function)
            async def wrapper( *args, **kwargs ):
                print('a debuguear :', args)
                print('a debuguear :', kwargs)
                print(f"{level} and {time_out}")
                json_request     = req2dict(kwargs)
                json_arguments   = get_positional_arguments(list(args))
                start_time = time.time()
                try:
                    fastApiResponse : JSONResponse = await function( *args, **kwargs )
                    json_response: Dict = json.loads(fastApiResponse.body.decode())
                    data_json = dict(
                            trace_id = self.trace_gcp.get(),
                            trace_aws = self.trace_aws.get(),
                            input_logging = {**json_request, **json_arguments},
                            function_name = function.__name__,
                            ouput_logging = json_response,
                            script_path =  __file__,
                            elapsed_timeMs= time.time()- start_time,
                            error_message= None,
                            level_logging = level
                        )
                    
                    if data_json['elapsed_timeMs'] > time_out:
                        data_json['level_logging'] = "WARNING"
                        data_json['error_message'] = "Time Out in function"

                    self.send_logging_to_gcp(data_json)

                except Exception as e:

                    data_json = dict(
                            trace_id = self.trace_gcp.get(),
                            trace_aws = self.trace_aws.get(),
                            input_logging = {**json_request, **json_arguments},
                            function_name = function.__name__,
                            script_path =  __file__,
                            error_message= str(e),
                            level_logging = "ERROR"
                        )

                    self.send_logging_to_gcp(data_json)
                    raise e
                return fastApiResponse

            return wrapper
        
        return wrapper_aux
    
    def log_db( self, level: str, time_out: float ) -> _TFunc:

        def wrapper_aux(function) -> _TFunc :
            async def wrapper( *args, **kwargs ):
                
                json_request     = req2dict(kwargs)
                json_arguments   = get_positional_arguments(list(args))
                start_time = time.time()
                fastApiResponse:JSONResponse = await function( *args, **kwargs )

                try:
                    json_response: Dict = json.loads(fastApiResponse.body.decode())
                    data_json = dict(
                            trace_id = self.trace_gcp.get(),
                            trace_aws = self.trace_aws.get(),
                            input_logging = {**json_request, **json_arguments},
                            function_name = function.__name__,
                            ouput_logging = json_response,
                            script_path =  __file__,
                            elapsed_timeMs= time.time()- start_time,
                            error_message= None,
                            level_logging = level,
                            additionalParams = dict(
                                        query = kwargs['query']
                                    )
                    )
                    
                    if data_json['elapsed_timeMs'] > time_out:
                        data_json['level_logging'] = "WARNING"
                        data_json['error_message'] = "Time Out in function"

                    self.send_logging_to_gcp(data_json)

                except Exception as e:

                    data_json = dict(
                            trace_id = self.trace_gcp.get(),
                            trace_aws = self.trace_aws.get(),
                            input_logging = {**json_request, **json_arguments},
                            function_name = function.__name__,
                            script_path =  __file__,
                            error_message= str(e),
                            level_logging = "ERROR"
                        )

                    self.send_logging_to_gcp(data_json)
                    raise e
                return fastApiResponse

            return wrapper
        
        return wrapper_aux







        
