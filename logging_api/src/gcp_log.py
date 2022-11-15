from starlette.responses import JSONResponse
from typing import Dict, Any, TypeVar, Callable
import json 
import time
import google.cloud.logging
import contextvars
import functools
from .base_logger import BaseLogger
import inspect
import os

from .utils.clean import req2dict, get_positional_arguments

_TFunc = TypeVar("_TFunc", bound=Callable[..., Any])

class GcpLogger(BaseLogger):

    def __init__(self,name) -> None:
        self.trace_gcp = contextvars.ContextVar("gcp_id", default=None)
        self.trace_aws = contextvars.ContextVar("aws_id", default=None)
        self.client = google.cloud.logging.Client()
        self.logger_gcp = self.client.logger(name)
    
    def send_logging_to_gcp(self, data_json):
        self.logger_gcp.log_struct(data_json, severity=data_json['level_logging'], trace = self.trace_gcp.get())

    def router( self, level: str = "DEBUG", time_out: float = 15.0 ):

        def wrapper_aux(function: _TFunc) -> _TFunc :
            @functools.wraps(function)
            async def wrapper( *args, **kwargs ):
                json_request     = req2dict(kwargs)
                json_arguments   = get_positional_arguments(list(args))
                start_time = time.time()

                total_info = inspect.stack()
                current_info   = total_info[2][0]
                function_name   = current_info.f_code.co_name
                file_name    = os.path.basename(current_info.f_code.co_filename)
                line_number = current_info.f_lineno  
                file_path = "%s:%d" % (file_name, line_number)

                try:
                    fastApiResponse : JSONResponse = await function( *args, **kwargs )
                    json_response: Dict = json.loads(fastApiResponse.body.decode())
                    data_json = dict(
                            trace_aws = self.trace_aws.get(),
                            input_logging = {**json_request, **json_arguments},
                            function_name = function_name,
                            ouput_logging = json_response,
                            script_path =  file_path,
                            elapsed_time_s= time.time()- start_time,
                            error_message= None,
                            level_logging = level
                        )
                    
                    if data_json['elapsed_time_s'] > time_out:
                        data_json['level_logging'] = "WARNING"
                        data_json['error_message'] = "Time Out in function"

                    self.send_logging_to_gcp(data_json)

                except Exception as e:

                    data_json = dict(
                            trace_id = self.trace_gcp.get(),
                            trace_aws = self.trace_aws.get(),
                            input_logging = {**json_request, **json_arguments},
                            function_name = function_name,
                            script_path =  file_path,
                            error_message= str(e),
                            level_logging = "ERROR"
                        )

                    self.send_logging_to_gcp(data_json)
                    raise e
                return fastApiResponse

            return wrapper
        
        return wrapper_aux
    
    def database( self, level: str = "INFO", time_out: float = 10.0 ) -> _TFunc:

        def wrapper_aux(function) -> _TFunc :
            async def wrapper( *args, **kwargs ):
                
                json_request     = req2dict(kwargs)
                json_arguments   = get_positional_arguments(list(args))
                start_time = time.time()
                fastApiResponse:JSONResponse = await function( *args, **kwargs )
                
                total_info = inspect.stack()
                current_info   = total_info[2][0]
                function_name   = current_info.f_code.co_name
                file_name    = os.path.basename(current_info.f_code.co_filename)
                line_number = current_info.f_lineno  
                file_path = "%s:%d" % (file_name, line_number)

                try:
                    json_response: Dict = json.loads(fastApiResponse.body.decode())
                    data_json = dict(
                            trace_id = self.trace_gcp.get(),
                            trace_aws = self.trace_aws.get(),
                            input_logging = {**json_request, **json_arguments},
                            function_name = function_name,
                            ouput_logging = json_response,
                            script_path =  file_path,
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
                            function_name = function_name,
                            script_path =  file_path,
                            error_message= str(e),
                            level_logging = "ERROR"
                        )

                    self.send_logging_to_gcp(data_json)
                    raise e
                return fastApiResponse

            return wrapper
        
        return wrapper_aux

    def function( self, level: str, time_out: float ) -> _TFunc:
        def wrapper_aux(function) -> _TFunc :
            async def wrapper( *args, **kwargs ):
                
                json_request     = req2dict(kwargs)
                json_arguments   = get_positional_arguments(list(args))
                start_time = time.time()
                fastApiResponse:JSONResponse = await function( *args, **kwargs )
                
                total_info = inspect.stack()
                current_info   = total_info[2][0]
                function_name   = current_info.f_code.co_name
                file_name    = os.path.basename(current_info.f_code.co_filename)
                line_number = current_info.f_lineno  
                file_path = "%s:%d" % (file_name, line_number)

                try:
                    json_response: Dict = json.loads(fastApiResponse.body.decode())
                    data_json = dict(
                            trace_id = self.trace_gcp.get(),
                            trace_aws = self.trace_aws.get(),
                            input_logging = {**json_request, **json_arguments},
                            function_name = function_name,
                            ouput_logging = json_response,
                            script_path =  file_path,
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
                            function_name = function_name,
                            script_path =  file_path,
                            error_message= str(e),
                            level_logging = "ERROR"
                        )

                    self.send_logging_to_gcp(data_json)
                    raise e
                return fastApiResponse

            return wrapper
        return wrapper_aux






                
