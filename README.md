# Overview
Blackmore allows you to create a command line tool more efficiently

<pre>
def add(x: int, y: int):
    print(x + y)

from enum import Enum

class Algorithm(Enum):
    ADD = "ADD"
    SUBTRACT = "SUBTRACT"

def calculate(algorithm: Algorithm, x: int, y: int):
    if algorithm == Algorithm.ADD:
        print(add(x, y))
    elif algorithm == Algorithm.SUBTRACT:
        print(x - y)
    else:
        print("not support")

blackmore = Blackmore("Perry", [add, calculate])
blackmore.execute()
</pre>

<pre>
blackmore add 3 26
</pre>

# Standard Input

<pre>
from typing import Annotated
import tomllib

def to_json(x: Annotated[str, lambda: sys.stdin.read()]):
    print(tomllib.loads(x))

blackmore = Blackmore("Perry", [to_json])
blackmore.execute()
</pre>

<pre>
cat pyproject.toml | blackmore to_json
</pre>
