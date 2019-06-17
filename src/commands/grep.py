import sys
import re


def local_parser(stream, reg, re_flags, n):
    """
    Parse io stream and collect answer for grep
    """
    numb = 0
    answer = ""
    for line in stream:
        if line == "\n":
            return answer
        res = re.findall(reg, line, re_flags)
        if res:
            numb = n + 1
        if numb:
            answer += line
            numb -= 1
    return answer


def grep(args, parser):
    """
    Search file(s) for specific text.
    """
    next_arg = args  # link for first arg
    new_arg = []
    not_propose_arg = 0
    # parser = argparse.ArgumentParser()
    while next_arg:
        new_arg.append(next_arg.name)
        if next_arg.name.startswith("-"):
            not_propose_arg += 1
        next_arg = next_arg.next

    # new_arg = ['text', 'test.txt']
        # new_arg = ['-h']
    try:
        args_from_parse = parser.parse_args(new_arg)
    except AttributeError:
        return "Invalid arguments for command grep."
    re_flags = 0
    if args_from_parse.ignore_case:
        re_flags = re.IGNORECASE

    reg = args_from_parse.PATTERN
    if args_from_parse.word_regexp:
        reg = reg.split("/")
        if len(reg) > 1:
            reg = reg[1]
        else:
            reg = reg[0]
        reg = "/\\s" + reg + "\\s" + "|^" + reg + "\\s|\\s" + reg + "$/"
    # print(reg)
    n = args_from_parse.after_context
    file = args_from_parse.FILES
    if file:
        try:
            with open(file) as f:
                answer = local_parser(f, reg, re_flags, n)
        except IOError:
            answer = "File " + file + " does not exists."
    else:
        answer = local_parser(sys.stdin, reg, re_flags, n)
    return answer
