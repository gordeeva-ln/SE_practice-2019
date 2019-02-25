# SE_practice-2019

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

