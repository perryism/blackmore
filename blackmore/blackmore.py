import argparse
from enum import EnumMeta
import typing

class Blackmore:
    def __init__(self, name, functions):
        self.name = name
        self.functions = dict([[f.__name__, f] for f in functions if not isinstance(f, Blackmore)])
        self.subcommands = dict([[f.__name__, f] for f in functions if isinstance(f, Blackmore)])
        # self.subcommand = subcommand

    @property
    def __name__(self):
        return self.name.lower()

    def execute(self, cmd_name = None,parser = None):
        if parser is None:
            parser = argparse.ArgumentParser(prog = self.name)
            parser.add_argument("cmd", help="command", choices=list(self.functions.keys()) + list(self.subcommands.keys()))
            args = parser.parse_known_args()
            cmd_name = args[0].cmd
        else:
            parser.add_argument(cmd_name, help="subcommand", choices=self.functions.keys())
            args = parser.parse_known_args()
            cmd_name = getattr(args[0], cmd_name)

        if cmd_name in self.subcommands:
            # parser.add_argument("subcommand", help="subcommand", choices=self.functions.keys())
            return self.subcommands[cmd_name].execute(cmd_name, parser)
        function = self.functions[cmd_name]
        if isinstance(function, Blackmore):
            return function.execute()
        else:
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

            return function(*params.values())

    def get_args(self, parser, function):
        for k, v in function.__annotations__.items():
            if hasattr(v, "__metadata__"):
               continue
            if v is str or v is int or v is float:
                parser.add_argument(k, type=v, help=f"{k}")
            elif isinstance(v, EnumMeta):
                parser.add_argument(k, help=k, choices=v.__members__.keys())
            elif typing.get_origin(v) is typing.Union:
                if type(None) in typing.get_args(v):
                    parser.add_argument(k, type=v.__args__[0], nargs="?", help=f"{k}")
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
