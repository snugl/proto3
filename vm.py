#!/usr/bin/python3

import sys

def lex(raw):
    prog = []
    for line in raw.split('\n'):
        if not line.strip():
            continue

        comps = list(filter(
            lambda x: bool(x.strip()),
            line.split(' ')
        ))

        inst = comps[0]
        arg  = int(comps[1]) if len(comps) > 1 else None

        prog.append((inst, arg))

    return prog



def run(prog):
    mem_size = 65536
    heap_base = mem_size // 2


    ip = 0
    acc = 0
    mem = [0 for _ in range(mem_size)]
    stack = []

    running = True


    while ip < len(prog) and running:
        inst, arg = prog[ip]
        ip += 1

        match inst:
            case 'const': acc = arg

            #arithmetic
            case 'add': acc += stack.pop()
            case 'sub': acc -= stack.pop()
            case 'mul': acc *= stack.pop()

            #data stack
            case 'push':  stack.append(acc)
            case 'pull':  acc = stack.pop()

            #generic memory
            case 'load':  acc = mem[arg]
            case 'store': mem[arg] = acc

            #flow
            case 'jump': ip = arg

            #misc
            case 'debug': print(acc)
            case 'halt': running = False



            case x:
                print(f"unknown instruction {x}")



def main():
    with open(sys.argv[1]) as f:
        prog = lex(f.read())

    run(prog)


if __name__ == "__main__":
    main()


