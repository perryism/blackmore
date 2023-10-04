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
                params[k] = getattr(args, k)

        return function(*params.values())

    def get_args(self, parser, function):
        for k, v in function.__annotations__.items():
            if v is str or v is int or v is float:
                parser.add_argument(k, type=v, help=k)
            elif isinstance(v, EnumMeta):
                parser.add_argument(k, help=k, choices=v.__members__.keys())
            else:
                raise TypeError(f"{v} is not supported")

        return parser.parse_args()