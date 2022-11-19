import inspect
import os
from typing import List

def get_offset_line(keyword: str, arr_strings: List) -> int:
    ans = 0
    for string_elemen in arr_strings:
        if keyword in string_elemen:
            return ans
        ans = ans + 1  
    return ans

def get_path_file(func):

    module_address = func.__globals__['__file__']
    info_function = inspect.getsourcelines(func) 
    line_addres = info_function[1]
    function_name = func.__name__

    function_path = "%s:%d" % (module_address, line_addres+get_offset_line( function_name,  info_function[0]))

    return [function_name, function_path]