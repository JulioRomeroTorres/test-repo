import inspect
import os

def get_path_file(func):

    module_address = func.__globals__['__file__']
    line_addres = inspect.getsourcelines(func)[1]
    function_name = func.__name__

    function_path = "%s:%d" % (module_address, line_addres+1)

    return [function_name, function_path]