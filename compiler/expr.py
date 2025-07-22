from dataclasses import dataclass

import error


@dataclass
class node:
    kind : str
    content : str | int
    left  : 'node | None' = None
    right : 'node | None' = None

    def write(self, ctx, val):
        match self.kind:
            case 'var':
                ctx.vars[self.content] = val

            case _:
                error.error("Unable to write to expression!")
     
    def eval(self, ctx) -> int:
        match self.kind:
            case 'num': return int(self.content)
            case 'var': return ctx.vars[self.content]
            case 'op' if self.left and self.right:
                l = self.left.eval(ctx)
                r = self.right.eval(ctx)

                match self.content:
                    case '+': return l + r
                    case '-': return l - r
                    case '*': return l * r

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

