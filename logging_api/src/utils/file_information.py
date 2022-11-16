import inspect
import os

def get_path_file():
    total_info = inspect.stack()
    current_info   = total_info[2][0]
    function_name   = current_info.f_code.co_name
    file_name    = os.path.basename(current_info.f_code.co_filename)
    line_number = current_info.f_lineno  
    file_path = "%s:%d" % (file_name, line_number)

    return function_name, file_path