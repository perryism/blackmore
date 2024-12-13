import argparse
from enum import EnumMeta

class Blackmore:
    def __init__(self, name, functions):
        self.name = name
        self.functions = dict([[f.__name__, f] for f in functions])

    def execute(self):
        parser = argparse.ArgumentParser(prog = self.name)
        parser.add_argument("cmd", help="command", choices=self.functions.keys())
        args = parser.parse_known_args()
        cmd_name = args[0].cmd
        function = self.functions[cmd_name]
        args = self.get_args(parser, function)

        params = {}
        for k, v in function.__annotations__.items():
            if isinstance(v, EnumMeta):
                params[k] = getattr(v, getattr(args, k))
            else:
                if hasattr(v, "__metadata__"):
                    if callable(v.__metadata__[0]):
                        params[k] = v.__metadata__[0]()
                        continue

                params[k] = getattr(args, k)

        return function(**params)#.values())

    def get_args(self, parser, function):
        for k, v in function.__annotations__.items():
            if hasattr(v, "__metadata__"):
               continue
            if v is str or v is int or v is float:
                parser.add_argument(k, type=v, help=f"{k}")
            elif isinstance(v, EnumMeta):
                parser.add_argument(k, help=k, choices=v.__members__.keys())
            else:
                raise TypeError(f"{v} is not supported")

        return parser.parse_args()

from functools import wraps

def parser(**kwargs):
    def decorator(f):
        f.__original_annotations__ = f.__annotations__.copy()
        for k, v in kwargs.items():
            f.__annotations__[k] = str
        @wraps(f)
        def wrapper(*args, **kwargs2):
            for k, v in kwargs.items():
                kwargs2[k] = kwargs[k](kwargs2[k])
            return f(*args, **kwargs2)
        return wrapper
    return decorator
