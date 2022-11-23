from starlette.responses import JSONResponse
from typing import Dict, Any, TypeVar, Callable
import json 
import time
import google.cloud.logging
import contextvars
import functools
from .base_logger import BaseLogger
from .utils.function_info import get_path_file
from .utils.clean import req2dict, get_positional_arguments
from .utils.encode_json import convert2json, convert2dict
import inspect
import sys
import traceback

_TFunc = TypeVar("_TFunc", bound=Callable[..., Any])

class GcpLogger(BaseLogger):

    def __init__(self,name) -> None:
        self.trace_gcp = contextvars.ContextVar("gcp_id", default=None)
        self.trace_aws = contextvars.ContextVar("aws_id", default=None)
        self.client = google.cloud.logging.Client()
        self.logger_gcp = self.client.logger(name)
    
    def send_logging_to_gcp(self, data_json) -> None:
        self.logger_gcp.log_struct(data_json, severity=data_json['level_logging'], trace = self.trace_gcp.get())

    def set_trace(self, *, gcp = None, aws = None ) -> None:
        
        self.trace_aws.set(aws)
        self.trace_gcp.set(gcp)

    def log_exception( self, severity:str, payload, exc_info: bool ):
        
        traceback_str = ""
        
        if exc_info :
            traceback_str_aux = traceback.format_exception(etype=type(payload), value = payload, tb = payload.__traceback__)
            traceback_str = "".join(traceback_str_aux)
            self.logger_gcp.log_text(traceback_str, severity=severity, trace = self.trace_gcp.get())
            return 
        self.logger_gcp.log_text(payload, severity=severity, trace = self.trace_gcp.get())

    def warning(self, payload, exc_info :bool = False):
        self.log_exception("WARNING", payload, exc_info)
    
    def error(self, payload, exc_info :bool = False):
        self.log_exception("ERROR", payload, exc_info)
    
    def debug(self, message: str = "Logging something here"):
        self.logger_gcp.log_text(message, severity="DEBUG", trace = self.trace_gcp.get())

    def router( self, *, level: str = "DEBUG", time_out: float = 15.0 ):

        def wrapper_aux(func: _TFunc) -> _TFunc :
            @functools.wraps(func)
            async def wrapper( *args, **kwargs ):
                json_request     = req2dict(kwargs)
                json_arguments   = get_positional_arguments(list(args))
                start_time = time.time()

                info_function = get_path_file(func)

                data_json = dict()
                common_payload = dict(
                            trace_aws = self.trace_aws.get(),
                            input_logging = {**json_request, **json_arguments},
                            function_name = info_function[0],
                            script_path =  info_function[1],
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

                self.send_logging_to_gcp(data_json)

                return fastApiResponse

            return wrapper
        
        return wrapper_aux
    
    def database( self,  *, level: str = "INFO", time_out: float = 10.0 ) -> _TFunc:

        def wrapper_aux(func: _TFunc) -> _TFunc :
            @functools.wraps(func)
            def wrapper( *args, **kwargs ):
                start_time = time.time()
                info_function = get_path_file(func)
                
                data_json = dict()
                common_payload = dict(
                            trace_aws = self.trace_aws.get(),
                            input_logging = kwargs,
                            function_name = info_function[0],
                            script_path =  info_function[1],
                            level_logging = level
                )
                try:
                    dataBaseResponse = func( *args, **kwargs )
                    #ouput_logging = json.dumps(dataBaseResponse, indent=2, default=str)

                    if isinstance(dataBaseResponse, list):
                        ouput_logging = convert2dict(dataBaseResponse[0])
                    else:
                        ouput_logging = convert2dict(dataBaseResponse)
                    
                    success_payload  = dict(
                            
                            ouput_logging = ouput_logging,
                            elapsed_time_s= time.time()- start_time,
                            error_message= None,
                            additional_params = dict(
                                                query = args[0].query_name,
                                                database  = args[0].database
                            )
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

                self.send_logging_to_gcp(data_json)
                return dataBaseResponse

            return wrapper
        
        return wrapper_aux

    def function( self,  *, level: str = "INFO", time_out: float = 10.0) -> _TFunc:
        def wrapper_aux(func: _TFunc) -> _TFunc :
            @functools.wraps(func)
            def wrapper( *args, **kwargs ):

                start_time = time.time()
                info_function = get_path_file(func)

                data_json = dict()
                common_payload = dict(
                            trace_aws = self.trace_aws.get(),
                            input_logging = { "args" : str(args),
                                               "kwargs": str(kwargs)},
                            function_name = info_function[0],
                            script_path =  info_function[1],
                            level_logging = level
                )

                try:
                    generalResponse  = func( *args, **kwargs )
                    
                    success_payload  = dict(
                            ouput_logging = str(generalResponse),
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
                
                self.send_logging_to_gcp(data_json)

                return generalResponse

            return wrapper
        
        return wrapper_aux






                
