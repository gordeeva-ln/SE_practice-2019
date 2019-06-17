from src.commands.Command import Command, Argument, CommandName


def split_by_quotes(current_number_of_token, current_char_of_line, splited_cl, line, quote):
    """
    Function for processing something in quotes (double or single)
    :param splited_cl: part of line, which has already dismantled
    :param quote: type of quotes
    :return: new state of input parametrs
    """

    if current_char_of_line != 0:
        current_number_of_token += 1
        splited_cl.append("")
    splited_cl[current_number_of_token] = quote
    current_char_of_line += 1
    char = line[current_char_of_line]
    while char != quote:
        splited_cl[current_number_of_token] += char
        current_char_of_line += 1
        char = line[current_char_of_line]
    splited_cl[current_number_of_token] += char
    current_char_of_line += 1
    current_number_of_token += 1
    splited_cl.append("")
    return splited_cl, current_char_of_line, current_number_of_token


def parse_for_one_part_of_pipe(part_of_pipe):
    """
    Function for parsing one part of pipe-line
    :return: new instance of Command
    """

    splited_cl = []
    current_number_of_token = 0
    current_char_of_line = 0
    char = part_of_pipe[0]
    splited_cl.append("")
    while current_char_of_line < len(part_of_pipe) - 1:
        if char == "'":
            splited_cl, current_char_of_line, current_number_of_token = split_by_quotes(
                current_number_of_token, current_char_of_line, splited_cl, part_of_pipe, "'")
            if current_char_of_line < len(part_of_pipe) and part_of_pipe[current_char_of_line] != " ":
                char = part_of_pipe[current_char_of_line]
            else:
                splited_cl.pop()
                break

        if char == '"':
            splited_cl, current_char_of_line, current_number_of_token = split_by_quotes(
                current_number_of_token, current_char_of_line, splited_cl, part_of_pipe, '"')
            if current_char_of_line < len(part_of_pipe) and part_of_pipe[current_char_of_line] != " ":
                char = part_of_pipe[current_char_of_line]
            else:
                splited_cl.pop()
                break

        elif char == " ":
            start = current_char_of_line
            while char == " ":
                current_char_of_line += 1
                char = part_of_pipe[current_char_of_line]
            if char != "'" and char != '"' and start != 0:
                current_number_of_token += 1
                splited_cl.append("")

        else:
            splited_cl[current_number_of_token] += char
            current_char_of_line += 1
            char = part_of_pipe[current_char_of_line]

    if char != "'" and char != '"' and char != " ":
        splited_cl[current_number_of_token] += char

    if splited_cl[0] == CommandName.EXIT.value:
        return False
    new_comm = Command(str(splited_cl[0]))

    # if this command has same arguments
    if len(splited_cl) != 1:
        arg_first = Argument(str(splited_cl[1]))
        new_comm.set(arg_first)
        arg_next = arg_first
        for arg in splited_cl[2:]:
            arg_next.next = Argument(str(arg))
            arg_next = arg_next.next

    return new_comm


def lex_and_parse(command_line):
    """
    Lexical analise and parse
    :return: first Command in Pipe
    """

    splited_for_pipes = command_line.split("|")
    command_first_in_pipe = parse_for_one_part_of_pipe(splited_for_pipes[0])
    commands_in_pipe = command_first_in_pipe
    for splited_cl in splited_for_pipes[1:]:
        commands_in_pipe.next = parse_for_one_part_of_pipe(splited_cl)
        commands_in_pipe = commands_in_pipe.next
    if not command_first_in_pipe:
        return False

    return command_first_in_pipe
