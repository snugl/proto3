#!/usr/bin/python3

import sys

import lex
import objs





def compiler(path):
    stream = lex.tokenize(path)
    prog = objs.parse_prog(stream)

    prog.resolve_labels()
    prog.infer_variables()
    prog.generate()

    print(prog.render())






def main():
    compiler(sys.argv[1])


if __name__ == "__main__":
    main()
