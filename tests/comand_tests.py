import pytest
from src.Parsers import lex_and_parse
import unittest
from src.Variable import Variables
from src.commands.Command import CommandName
import os
import re
import argparse


class TestStringMethods(unittest.TestCase):
    @staticmethod
    def _test(command_line, var, parser=None):
        command = lex_and_parse(command_line)
        if not command:
            return CommandName.EXIT.value
        command.expansions(var)
        answer = command.execution(parser)
        return answer

    def test_echo(self):
        var = Variables()
        self.assertTrue(self._test("echo 'Hello, world!'", var) == "Hello, world!")
        self.assertTrue(self._test("echo 123", var) == "123")
        self.assertTrue(self._test("echo", var) == "")
        self._test("var=r", var)
        self.assertTrue(self._test('echo "$var"', var) == "r")
        self.assertTrue(self._test("echo '$var'", var) == "$var")
        self.assertTrue(self._test("echo 4|echo 5", var) == "5")
        self.assertTrue(self._test("echo '$var'|echo 5", var) == "5")
        self.assertTrue(self._test("echo 5|echo '$var'", var) == "$var")
        self.assertTrue(self._test('echo 5 | echo "$var"', var) == "r")

    def test_cat(self):
        var = Variables()
        self.assertTrue(self._test("cat name.txt", var) == "cat: name.txt: no such file or directory")
        self.assertTrue(self._test("echo dddd | cat", var) == "dddd")
        self._test("var=r", var)
        self.assertTrue(self._test('echo "$var" | cat', var) == "r")
        path = "cat_test_file.txt"
        f = open(path, "w+")
        f.write("some magic text")
        f.close()
        self.assertTrue(self._test("cat " + path, var) == "some magic text")
        os.remove(path)

    def test_wc(self):
        var = Variables()
        self.assertTrue(self._test("echo aaaaaa|wc", var) == "1 1 31")
        self.assertTrue(self._test("echo|wc", var) == "1 0 25")
        self.assertTrue(self._test("wc", var) == "1 0 25")
        path = "wc_test_file.txt"
        f = open(path, "w+")
        f.write("some magic text")
        f.close()
        self.assertTrue(self._test("wc " + path, var) == "1 3 40")
        os.remove(path)

    def test_pwd(self):
        var = Variables()
        self.assertTrue(self._test("pwd", var) == os.getcwd())

    def test_exit(self):
        var = Variables()
        self.assertTrue(self._test("exit", var) == CommandName.EXIT.value)
        self._test("x=ex", var)
        self._test("y=it", var)
        self.assertTrue(self._test("$x$y", var) == CommandName.EXIT.value)

    def test_grep(self):
        var = Variables()
        parser = argparse.ArgumentParser()
        parser.add_argument('PATTERN', nargs='?')
        parser.add_argument('FILES', nargs='?')

        parser.add_argument('-i', '--ignore-case', action='store_true', default=False,
                            help="Ignore case distinctions, so that "
                            "characters that differ only in case match each other.")

        parser.add_argument('-w', '--word-regexp', action='store_true', default=False,
                            help="Select  only  those  lines  containing "
                            "matches  that form whole words.")

        parser.add_argument('-A', '--after-context', type=int, action='store', default=0,
                            help="Print  NUM  lines  of  trailing  context  after  matching lines.")
        file = "wrong_file.txt"
        self.assertTrue(self._test("grep text " + file, var, parser) == "File " + file + " does not exists.")
        self.assertTrue(self._test("grep text test.txt", var, parser) == "text text\naaa_text\nnottextatall")
        self.assertTrue(self._test("grep -A 2 text test.txt", var, parser) ==
                        "text text\naaa_text\nasd\nteeest\nnottextatall")
        self.assertTrue(self._test("grep -w text test.txt", var, parser) == "text text\n")

        self.assertTrue(self._test("grep -i text test.txt", var, parser) ==
                        "TextWith\ntext text\naaa_text\nteXt\nnottextatall")

    def test_another(self):
        var = Variables()
        self.assertTrue(len(re.findall(".py", self._test("dir " + os.getcwd(), var))) == 1)
        print(os.getcwd())
        src_path = "\\".join((os.getcwd().split("\\"))[:-1]) + "\\src"
        python_files = len([i for i in self._test("dir " + src_path, var).split("\n") if i.endswith(".py")])
        self.assertTrue(python_files == 3)


if __name__ == '__main__':
    unittest.main()
