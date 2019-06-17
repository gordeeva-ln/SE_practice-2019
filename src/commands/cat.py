def cat(args, std):
    """
    Concatenate files and print on the standard output, if std = False.
    If std = True print args from previous command in pipe.
    """

    if std:
        return args.name
    new_arg = ""
    next_arg = args
    while next_arg:
        # print(next_arg.name)
        try:
            f = open(next_arg.name)

            for line in f:
                new_arg += line
            f.close()
        except FileNotFoundError:
            return "cat: " + next_arg.name + ": no such file or directory"
        next_arg = next_arg.next
    return new_arg
