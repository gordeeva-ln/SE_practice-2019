import subprocess
from src.commands.cat import cat
from src.commands.echo import echo
from src.commands.wc import wc
from src.commands.pwd import pwd
from src.commands.grep import grep
import argparse
import os
from enum import Enum
import sys
import shlex


class CommandName(Enum):
    """Enum with command names."""
    CAT = "cat"
    ECHO = "echo"
    WC = "wc"
    PWD = "pwd"
    EXIT = "exit"
    GREP = "grep"
    INITIALIZE = "initialize"


class Argument:
    """
    Class for arguments of same command.
    name - string, next - next argument (when command have several arguments).
    """

    def __init__(self, name, next=None):
        self.next = next  # next argument
        self.name = name  # what argument is

    def expansion_of_one_part(self, vars):
        """Do expansion in one token."""

        if not self:
            return
        if self.name[0] == self.name[-1] == '"':
            self.name = self.name[1:-1]

            var = self.name.split("=")
            vars.set(var[0], '='.join(var[1:]))
            if len(var) > 1:
                self.name = CommandName.INITIALIZE.value
            current_char_of_line = 0
            while current_char_of_line < len(self.name):
                if self.name[current_char_of_line] == "$":
                    var_curr = ""
                    start = current_char_of_line
                    current_char_of_line += 1
                    while current_char_of_line < len(self.name) \
                            and self.name[current_char_of_line] != " " \
                            and self.name[current_char_of_line] != "$":
                        var_curr += self.name[current_char_of_line]
                        current_char_of_line += 1
                    if var_curr in vars.vars.keys():
                        self.name = self.name[:start] + vars.get(var_curr) + self.name[current_char_of_line:]
                    else:
                        self.name = self.name[:start] + self.name[current_char_of_line:]
                current_char_of_line += 1
        elif self.name[0] == self.name[-1] == "'":
            self.name = self.name[1:-1]


class Command:
    """
    Class describes one command.
    If this command in pipe, attribute next will be a next command in this pipe.
    args - first of all arguments for command (it have a link to another one).
    name - command name, which is one of CommandName class.
    std - if out will be printed to standard output or in file.
    """

    def __init__(self, name, arguments=None, next=None, std=False):
        self.next = next
        self.args = arguments
        self.name = name
        self.std = std

    def get(self):
        """:return first argument of this command, which have a link to another one"""
        return self.args

    def set(self, arg):
        """
        Set attribute args equals arg.
        :param arg - argument of this command
        """

        self.args = arg

    def expansions(self, vars):
        """Do expansion of all line."""
        curr_command = self
        while curr_command:
            curr_command.expansion_of_one_part(vars)
            curr_arg = curr_command.args
            while curr_arg:
                curr_arg.expansion_of_one_part(vars)
                curr_arg = curr_arg.next
            curr_command = curr_command.next

    def exec_part_of_pipe(self, parser):
        """Execution one command in pipe."""

        if self.name == CommandName.CAT.value:
            return cat(self.get(), self.std)
        if self.name == CommandName.ECHO.value:
            return echo(self.get())
        if self.name == CommandName.WC.value:
            return wc(self.get(), self.std)
        if self.name == CommandName.PWD.value:
            return pwd()
        if self.name == CommandName.EXIT.value:
            return CommandName.EXIT.value
        if self.name == CommandName.GREP.value:
            return grep(self.get(), parser)
        if self.name == CommandName.INITIALIZE.value:
            return ""
        try:
            list_of_args = []
            next_arg = self.get()
            while next_arg:
                list_of_args.append(next_arg)
                next_arg = next_arg.next

            s = subprocess.getstatusoutput(" ".join([self.name] + [arg.name for arg in list_of_args]))
            if s[0] != 0:
                return self.name + ": command not found"
            return s[1]
        except TypeError:
            print(self.name + ": command not found")

    def execution(self, parser):
        """Execution of all commands."""

        next_comm = self
        arg = next_comm.exec_part_of_pipe(parser)

        while next_comm:
            if not next_comm.args and (next_comm.name == CommandName.WC.value
                                       or next_comm.name == CommandName.CAT.value):
                next_comm.set(Argument(arg))
                next_comm.std = True
            arg = next_comm.exec_part_of_pipe(parser)
            next_comm = next_comm.next
        return arg

    def expansion_of_one_part(self, vars):
        """Do expansion in one token."""

        if not self:
            return
        if self.name[0] == self.name[-1] == '"':
            self.name = self.name[1:-1]
        if self.name[0] == self.name[-1] == "'":
            self.name = False
        var = self.name.split("=")
        vars.set(var[0], '='.join(var[1:]))
        if len(var) > 1:
            self.name = CommandName.INITIALIZE.value
        current_char_of_line = 0
        while current_char_of_line < len(self.name):
            if self.name[current_char_of_line] == "$":

                var_curr = ""
                start = current_char_of_line
                current_char_of_line += 1
                while current_char_of_line < len(self.name) \
                        and self.name[current_char_of_line] != " " \
                        and self.name[current_char_of_line] != "$":
                    var_curr += self.name[current_char_of_line]
                    current_char_of_line += 1
                if var_curr in vars.vars.keys():
                    self.name = self.name[:start] + vars.get(var_curr) + self.name[current_char_of_line:]
                else:
                    self.name = self.name[:start] + self.name[current_char_of_line:]
            else:
                current_char_of_line += 1
