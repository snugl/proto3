#!/usr/bin/python3

import sys

import lex
import objs





def compiler(path):
    stream = lex.tokenize(path)
    root = objs.parse_prog(stream)
    root.process()
    root.run()





def main():
    compiler(sys.argv[1])


if __name__ == "__main__":
    main()
