

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

    def eval(self, ctx):
        print(self.target.eval(ctx))



@dataclass
class _put:
    lhs : expr.node
    rhs : expr.node

    @classmethod
    def parse(cls, stream):
        lhs = expr.parse(stream)
        stream.expect('=')
        rhs = expr.parse(stream)
        return cls(lhs, rhs)

    def eval(self, ctx):
        val = self.rhs.eval(ctx)
        self.lhs.write(ctx, val)


@dataclass
class _lab:
    label : str

    @classmethod
    def parse(cls, stream):
        label = stream.pop()
        return cls(label)

    def process(self, ctx, index):
        ctx.labels[self.label] = index 

    def eval(self, ctx):
        pass #doesn't do anything


@dataclass()
class _jump:
    target : str

    @classmethod
    def parse(cls, stream):
        label = stream.pop()
        return cls(label)

    def eval(self, ctx):
        ctx.ip = ctx.labels[self.target]


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

    vars  : dict[str, int] = field(default_factory=lambda: {})
    const : dict[str, int] = field(default_factory=lambda: {})

    labels : dict[str, int] = field(default_factory=lambda: {})

    ip : int = 0

    def process(self):
        for index, stat in enumerate(self.statements):
            if hasattr(stat, 'process'):
                stat.process(self, index) 


    def run(self):
        while self.ip < len(self.statements):
            obj = self.statements[self.ip]
            self.ip += 1
            obj.eval(self)



def parse_prog(stream):
    root = prog()
    while stream.has():
        root.statements.append(
            parse_statement(stream))

    return root







