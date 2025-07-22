





def kind(char):
    match char:
        case x if x.isalpha():  return 'iden'
        case x if x.isdigit():  return 'numb'
        case ';':               return 'eos'
        case '\n':              return 'nl'
        case ' ':               return 'space'



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


    print(stream)




