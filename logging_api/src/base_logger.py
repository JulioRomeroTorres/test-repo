from typing import TypeVar, Any, Callable
import functools
import contextvars
from starlette.responses import JSONResponse
from typing import Dict, Any, TypeVar, Callable
from .utils.file_information import get_path_file
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

    def set_trace(self, *, trace_gcp = None, trace_aws = None ) -> None:
        
        self.trace_aws.set(trace_aws)
        self.trace_gcp.set(trace_gcp)
        
    def router( self, *, level: str = "DEBUG", time_out: float = 15.0 ):

        def wrapper_aux(func: _TFunc) -> _TFunc :
            @functools.wraps(func)
            async def wrapper( *args, **kwargs ):
                json_request     = req2dict(kwargs)
                json_arguments   = get_positional_arguments(list(args))
                start_time = time.time()

                function_name, file_path = get_path_file()

                data_json = dict()
                common_payload = dict(
                            trace_aws = self.trace_aws.get(),
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

                self.send_logging_to_gcp(data_json)

                return fastApiResponse

            return wrapper
        
        return wrapper_aux
    
    def database( self,  *, level: str = "INFO", time_out: float = 10.0 ) -> _TFunc:

        def wrapper_aux(func: _TFunc) -> _TFunc :
            @functools.wraps(func)
            def wrapper( *args, **kwargs ):
                start_time = time.time()
                function_name, file_path = get_path_file()
                
                data_json = dict()
                common_payload = dict(
                            trace_aws = self.trace_aws.get(),
                            input_logging = kwargs,
                            function_name = func.__name__,
                            script_path =  file_path,
                            level_logging = level
                )
                try:
                    dataBaseResponse = func( *args, **kwargs )
                    #ouput_logging = json.dumps(dataBaseResponse, indent=2, default=str)
                    success_payload  = dict(
                            ouput_logging = convert2json(dataBaseResponse),
                            elapsed_time_s= time.time()- start_time,
                            error_message= None,
                            additional_params = dict(
                                                query = str(args[0].query_name),
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
                function_name, file_path = get_path_file()

                data_json = dict()
                common_payload = dict(
                            trace_aws = self.trace_aws.get(),
                            input_logging = { "args" : str(args),
                                               "kwargs": str(kwargs)},
                            function_name = func.__name__,
                            script_path =  file_path,
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
