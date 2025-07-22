
from dataclasses import dataclass

import error


@dataclass
class streamer:
    container : list[str]

    def pop(self):
        return self.container.pop(0)

    def peek(self):
        return self.container[0]

    def expect(self, content):
        token = self.pop()
        if token != content:
            error.error(f"Expected '{content}' but got '{token}'")

    def has(self):
        return len(self.container) > 0






def kind(char):
    match char:
        case x if x.isalpha():  return 'iden'
        case x if x.isdigit():  return 'numb'
        case ';':               return 'eos'
        case '\n':              return 'nl'
        case ' ':               return 'space'
        
        case '(':               return 'open_paran'
        case ')':               return 'close_paran'

        case _:                 return 'sym'



def tokenize(path):
    with open(path) as f:
        source = f.read()

    kind_old = None
    buffer = []
    stream = []
    for char in source:
        kind_new = kind(char)

        if kind_old != kind_new:
            if kind_old not in ('nl', 'space', None):
                stream.append("".join(buffer))
            buffer = []

        kind_old = kind_new
        buffer.append(char)


    return streamer(stream)




