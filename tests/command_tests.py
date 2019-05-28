import pytest
from src.Parsers import lex_and_parse
import unittest
from src.Variable import Variables
from src.commands.Command import CommandName
import os
import re


class TestStringMethods(unittest.TestCase):
    @staticmethod
    def _test(command_line, var):
        command = lex_and_parse(command_line)
        if not command:
            return CommandName.EXIT.value
        command.expansions(var)
        answer = command.execution()
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

    def test_another(self):
        var = Variables()
        self.assertTrue(len(re.findall(".py", self._test("dir " + os.getcwd(), var))) == 1)
        print(os.getcwd())
        src_path = "\\".join((os.getcwd().split("\\"))[:-1]) + "\\src"
        python_files = len([i for i in self._test("dir " + src_path, var).split("\n") if i.endswith(".py")])
        self.assertTrue(python_files == 3)


if __name__ == '__main__':
    unittest.main()
