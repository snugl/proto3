#!/usr/bin/python3

import sys

import lex



def compiler(path):
    stream = lex.tokenize(path)





def main():
    compiler(sys.argv[1])


if __name__ == "__main__":
    main()
