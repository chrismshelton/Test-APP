import sys

def current_function_name():
    return sys._getframe().f_back.f_code.co_name
