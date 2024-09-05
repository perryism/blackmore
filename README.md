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


## Nested commands

<pre>

def ls(path: str):
    print(os.listdir(path))

def cat(file_name: str):
    with open(file_name) as f:
        print(f.read())

math = Blackmore("Math", [add, calculate])
utils = Blackmore("Utils", [ls, cat])

blackmore = Blackmore("Perry", [math, utils])

blackmore.execute()

</pre>