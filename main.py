"""
CLI - command line interpreter.
Support commands:

1. cat [FILE] (or stdin)
2. echo
3. wc [FILE] (or stdin)
4. pwd
5. exit

Сonsists of 2 structs:

1. Command
2. Argument
3. CLI

Command:

1.next - next command in pipe
2.args - argument for this command (Argument object)
3.name - name of this command
4.std - input is stdin or not

Argument:

1.next - next argument for current command
2.name - string, body of this argument

CLI:

This class has only one method:
start - which starts up this CLI


Command sequence:

1. input()
2. lex_and_parse -> parse_for_one_part_of_pipe (for one part of pipe) -> quotes (for parsing in quotes)
3. expansions -> expansion_of_one_part (for one part of command)
4. execution -> exec_part_of_pipe (for execution one part of pipe) ->
                                                                        1.cat
                                                                        2.echo
                                                                        3.wc
                                                                        4.pwd
"""

from src.Parsers import lex_and_parse
from src.Variable import Variables
from src.commands.Command import CommandName
import argparse


def start():
    """Run command line."""

    var = Variables()
    parser = argparse.ArgumentParser()
    parser.add_argument('PATTERN', nargs='?')
    parser.add_argument('FILES', nargs='?')

    parser.add_argument(
        '-i', '--ignore-case',
        action='store_true',
        default=False,
        help="Ignore case distinctions, so that \
                 #                     characters that differ only in case match each other."
    )

    parser.add_argument(
        '-w', '--word-regexp',
        action='store_true',
        default=False,
        help="Select  only  those  lines  containing \
                #                      matches  that form whole words."
    )

    parser.add_argument(
        '-A', '--after-context',
        type=int,
        action='store',
        default=0,
        help="Print  NUM  lines  of  trailing  context  after  matching lines."
    )

    while True:
        command_line = input()
        command = lex_and_parse(command_line)
        if not command:
            break
        command.expansions(var)
        answer = command.execution(parser)
        if answer == CommandName.EXIT.value:
            break
        print(answer)


if __name__ == '__main__':
    start()
