import inspect
from typing import Iterable
from threading import Thread
import sys
debug = True


def print_debug(msg):
    if debug:
        print(msg)


def print_warnings(function, is_debug, *args, **kwargs):
    fullargspec: inspect.FullArgSpec = inspect.getfullargspec(function)
    args = args[0]
    for arg_name, expected_type in fullargspec.annotations.items():
        index_of = fullargspec.args.index(arg_name)
        got = args[index_of]
        will_print = False
        if isinstance(expected_type, Iterable):
            if type(got) not in expected_type:
                will_print = True
        else:
            if not (isinstance(args[index_of], expected_type)):
                will_print = True
        if will_print:
            if is_debug:
                print_debug(
                    f"Expected [{expected_type}],"
                    f" got [{type(got)}: {got}] "
                    f"in function {str(sys.modules[__name__]).replace('<', '').replace('>', '')}:{function.__name__}")
            else:
                print(
                    f"Expected [{expected_type}],"
                    f" got [{type(got)}: {got}] "
                    f"in function {str(sys.modules[__name__]).replace('<', '').replace('>', '')}:{function.__name__}")


def error_handler(is_debug=True,print_warnings=False, error_handler_callback=None):
    """
            This decorator gives the capacity of a try catch and will print a message if you call the function with
            wrong types

            The printing will be executed in a independent Thread.

            Try catch definition:
                try:
                    function(...)
                except Exception:
                    error_handler(e,args,kwargs)

            :parameter is_debug: if True will print only in debug mode else will print always. Default is True
            :parameter error_handler_callback: this will be called with the arguments and the error. Default is None.
            :parameter print_warnings: if true will print warnings about the types of the parameters.
    """
    def error_safety(*args, **kwargs):
        def wrapper(function):
            if print_warnings:
                Thread(target=print_warnings, args=(function, is_debug, args), kwargs=kwargs).start()
            try:
                return function(*args, **kwargs)
            except Exception as e:
                if error_handler_callback:
                    error_handler_callback(e, args, kwargs)

        return wrapper

    return error_safety
