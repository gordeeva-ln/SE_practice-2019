import sys


def wc(args, std):
    """
    Print newline, word, and byte counts for each FILE,
     and a total line if more than one FILE is specified.
     With no FILE, or when FILE is -, read standard input.
    """

    lines = 0
    words = 0
    bytes_c = 0
    if std:
        # print(args.name)
        # print(args.name.count("\n"))
        lines = args.name.count("\n") + 1
        words = len(args.name.split())
        bytes_c = sys.getsizeof(args.name)

        return '{0} {1} {2}'.format(lines, words, bytes_c)

    new_arg = ""
    next_arg = args
    while next_arg:
        f = open(next_arg.name)
        for line in f:
            lines += args.name.count("\n") + 1
            words += len(line.split())
            bytes_c += sys.getsizeof(line)
        f.close()
        new_arg += '{0} {1} {2}'.format(lines, words, bytes_c) + '\n'
        next_arg = next_arg.next
    return new_arg[:-1]
