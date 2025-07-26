

from dataclasses import dataclass
from dataclasses import field
import typing
import itertools


import expr
import error

@dataclass
class _debug:
    target : expr.node

    @classmethod
    def parse(cls, stream):
        target = expr.parse(stream)
        return cls(target)

    def __len__(self):
        return len(self.target) + 1
    def generate(self, ctx):
        self.target.gen_read(ctx)
        ctx.emit('debug')



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

    def infer(self, ctx):
        self.lhs.infer(ctx)

    def __len__(self):
        return len(self.rhs) + len(self.lhs)
    def generate(self, ctx):
        self.rhs.gen_read(ctx)
        self.lhs.gen_write(ctx)



@dataclass
class _lab:
    label : str

    @classmethod
    def parse(cls, stream):
        label = stream.pop()
        return cls(label)

    def resolve(self, ctx, index):
        ctx.labels[self.label] = index 

    def __len__(self):
        return 0
    def generate(self, ctx):
        pass #doesn't do anything


@dataclass
class _jump:
    target : str

    @classmethod
    def parse(cls, stream):
        label = stream.pop()
        return cls(label)

    def __len__(self):
        return 1
    def generate(self, ctx):
        target_addr = ctx.labels[self.target]
        ctx.emit(f'jump {target_addr}')

@dataclass
class _sub:
    target : str

    @classmethod
    def parse(cls, stream):
        return cls(stream.pop())

    def __len__(self):
        return 1
    def generate(self, ctx):
        target_addr = ctx.labels[self.target]
        ctx.emit(f'call {target_addr}')

@dataclass
class _return:
    @classmethod
    def parse(cls, stream):
        return cls()
    def __len__(self):
        return 1
    def generate(self, ctx):
        ctx.emit('return')

@dataclass
class _push:
    target : expr.node

    @classmethod
    def parse(cls, stream):
        return cls(expr.parse(stream))

    def __len__(self):
        return len(self.target) + 1
    def generate(self, ctx):
        self.target.gen_read(ctx)
        ctx.emit('push')

@dataclass
class _pull:
    target : expr.node

    @classmethod
    def parse(cls, stream):
        return cls(expr.parse(stream))

    def infer(self, ctx):
        self.target.infer(ctx)

    def __len__(self):
        return len(self.target) + 1
    def generate(self, ctx):
        ctx.emit('pull')
        self.target.gen_write(ctx)


class _swap:
    @classmethod
    def parse(cls, stream):
        return cls()
    def __len__(self):
        return 8
    def generate(self, ctx):
        #read
        ctx.emit('pull')
        ctx.emit(f'store {ctx.tmp_fst_addr}')
        ctx.emit('pull')
        ctx.emit(f'store {ctx.tmp_snd_addr}')

        #write
        ctx.emit(f'load {ctx.tmp_fst_addr}')
        ctx.emit('push')
        ctx.emit(f'load {ctx.tmp_snd_addr}')
        ctx.emit('push')


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
    statements : typing.Any     = field(default_factory=lambda: [])
    const      : dict[str, int] = field(default_factory=lambda: {})
    labels     : dict[str, int] = field(default_factory=lambda: {})

    vars        : dict[str, int]  = field(default_factory=lambda: {})
    mem_allocer : typing.Iterator = field(default_factory=lambda: itertools.count(2))

    emit_buffer : list[str] = field(default_factory=lambda: [])

    
    #symmetric address pair for temporary offloading
    tmp_fst_addr : int = 0
    tmp_snd_addr : int = 1

    def emit(self, output):
        self.emit_buffer.append(output)

    def alloc_var(self, name):
        if name not in self.vars:
            self.vars[name] = next(self.mem_allocer)

    def resolve_labels(self):
        index = 0
        for stat in self.statements:
            if type(stat) is _lab:
                stat.resolve(self, index) 

            index += len(stat)

    def infer_variables(self):
        for stat in self.statements:
            if type(stat) is _put or \
               type(stat) is _pull:
                stat.infer(self)


    def generate(self):
        for stat in self.statements:
            stat.generate(self)

        self.emit('halt')

    def render(self):
        return "\n".join(self.emit_buffer)

    def write(self, path):
        with open(path, 'w') as f:
            f.write(self.render())

def parse_prog(stream):
    root = prog()
    while stream.has():
        root.statements.append(
            parse_statement(stream))

    return root







