# SE_practice-2019

CLI - command line interpreter.
Support commands:

1. cat [FILE] (or stdin)
2. echo
3. wc [FILE] (or stdin)
4. pwd
5. exit
6. grep

Сonsists of 2 structs:

1. Command
2. Argument
3. CLI


Command sequence:

1. input
2. lex_and_parse
3. expansions
4. execution

Command grep support 3 keys:
1. -i - ignore-case
2. -w - word-regexp
3. -A - after-context
