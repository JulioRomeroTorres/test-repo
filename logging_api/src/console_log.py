from typing import Dict, Any, TypeVar, Callable
import json
from .utils.clean import req2dict, get_positional_arguments
import time
from starlette.responses import JSONResponse
from .base_logger import BaseLogger

import logging
_TFunc = TypeVar("_TFunc", bound=Callable[..., Any])

logger = logging.getLogger('console')


class ConsoleLogger(BaseLogger):

    def router(self, level: str, time_out: float):
        def wrapper_aux(function: _TFunc) -> _TFunc:
            async def wrapper( *args, **kwargs ):
                
                json_request     = req2dict(kwargs)
                json_arguments   = get_positional_arguments(list(args))
                start_time = time.time()
                fastApiResponse:JSONResponse = await function( *args, **kwargs )
                
                try: 

                    json_response: Dict = json.loads(fastApiResponse.body.decode())
                    data_json = dict(
                            trace_id = self.logger_gcp.trace_gcp.get(),
                            trace_aws = self.logger_gcp.trace_aws.get(),
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

                    logger.debug(json.dumps(data_json))
                
                except Exception as e:
                    data_json = dict(
                            trace_id = self.logger_gcp.trace_gcp.get(),
                            trace_aws = self.logger_gcp.trace_aws.get(),
                            input_logging = {**json_request, **json_arguments},
                            function_name = function.__name__,
                            script_path =  __file__,
                            error_message= str(e),
                            level_logging = "ERROR"
                        )

                    logger.debug(json.dumps(data_json))
                    raise e
                
                return fastApiResponse
            return wrapper
        return wrapper_aux

    def database( self, level: str, time_out: float ):
        def wrapper_aux(function) -> _TFunc :
            async def wrapper( *args, **kwargs ):
                
                json_request     = req2dict(kwargs)
                json_arguments   = get_positional_arguments(list(args))
                start_time = time.time()
                fastApiResponse:JSONResponse = await function( *args, **kwargs )

                try:
                    json_response: Dict = json.loads(fastApiResponse.body.decode())
                    data_json = dict(
                            trace_id = self.logger_gcp.trace_gcp.get(),
                            trace_aws = self.logger_gcp.trace_aws.get(),
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
                            trace_id = self.logger_gcp.trace_gcp.get(),
                            trace_aws = self.logger_gcp.trace_aws.get(),
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

    def function(level: str, time_out: float):
        return True