from dataclasses import dataclass

import error


@dataclass
class node:
    kind : str
    content : str | int
    left  : 'node | None' = None
    right : 'node | None' = None

    def infer(self, ctx):
        if self.kind == 'var':
            ctx.alloc_var(self.content)


    #generate write from acc to expr
    def gen_write(self, ctx):
        match self.kind:
            case 'var':
                var_addr = ctx.vars[self.content]
                ctx.emit(f'store {var_addr}')

            case _:
                error.error("Unable to write to expression!")
     
    #generate read from expr to acc
    def gen_read(self, ctx):
        match self.kind:
            case 'num': ctx.emit(f'const {self.content}')
            case 'var': 
                var_addr = ctx.vars[self.content]
                ctx.emit(f'load {var_addr}')
            case 'op' if self.left and self.right:
                self.left.gen_read(ctx)
                ctx.emit('push')
                self.right.gen_read(ctx)

                match self.content:
                    case '+': ctx.emit('add')
                    case '-': ctx.emit('sub')
                    case '*': ctx.emit('mul')

                    case _:
                        error.error("Internal fucking error, bitch!")

            case _:
                error.error("Internal fucking error, bitch!")



prec_cats = (
    ("<", ">", "<=", ">="),
    ("+", "-"),
    ("*"),
    ("."),
)



def parse_expr(stream, prec_level) -> node:
    left = parse_higher(stream, prec_level)

    if str(stream.peek()) not in prec_cats[prec_level]:
        return left

    op = stream.pop()
    right = parse_expr(stream, prec_level)
    return node(
        kind = 'op',
        content = op,
        left = left,
        right = right
    )

#parse at higher precedence level
def parse_higher(stream, prec_level) -> node:
    prec_level_next = prec_level + 1
    if prec_level_next < len(prec_cats):
        return parse_expr(stream, prec_level_next)
    else:
        return parse_terminal(stream)

def parse_terminal(stream) -> node:
    match stream.pop():
        case '(':
            expr = parse_expr(stream, 0)
            stream.expect(")")
            return expr
        case x if x.isdigit():
            return node(
                kind = 'num',
                content = int(x)
            )
        case x if x.isalpha():
            return node(
                kind = 'var',
                content = x
            )
        case x:
            error.error(f"Unable to parse terminal '{x}'")


def parse(stream) -> node:
    return parse_expr(stream, 0)

