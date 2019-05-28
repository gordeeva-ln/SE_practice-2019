def echo(args):
    """Write arguments to the standard output."""

    next_arg = args
    new_arg = ""
    while next_arg:
        new_arg += next_arg.name + " "
        next_arg = next_arg.next
    return new_arg[:-1]
