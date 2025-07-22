

from dataclasses import dataclass
from dataclasses import field
import typing


import expr
import error

@dataclass
class _debug:
    target : expr.node

    @classmethod
    def parse(cls, stream):
        target = expr.parse(stream)
        return cls(target)



@dataclass
class _put:
    lsh : expr.node
    rhs : expr.node

    @classmethod
    def parse(cls, stream):
        lsh = stream.pop() 
        rhs = expr.parse(stream)




def parse_statement(stream):
    iden = stream.pop()
    name = f"_{iden}"


    namespace = globals()
    if name not in namespace:
        error.error(f"Invalid statement name: {iden}")

    obj = namespace[name].parse(stream)
    stream.expect(';')

    return obj


@dataclass
class prog:
    statements : typing.Any = field(default_factory=lambda: [])


def parse_prog(stream):
    root = prog()
    while stream.has():
        root.statements.append(
            parse_statement(stream))

    return root







