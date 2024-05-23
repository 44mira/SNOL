from interfaces import Node, Error
from lexer import Token

type Command = list[Token]


def parser(tokens: Command) -> Node:
    return _parse_command(tokens)


def _parse_command(command: Command) -> Node:
    """
    Attempts to parse a command from the given tokens.

    <command> : ( <expression>
                | <assignment>
                | <output>
                | <EXIT!>
                ) /EOF/

    :return: The parsed command as an AST.
    :raises: Error if the command is invalid or parser fails to reach end of
             line.
    """

    ast: Node | None = (
        _parse_assignment(command)
        or _parse_output(command)
        or _parse_exit(command)
        or _parse_expression(command)
    )

    if not ast:
        raise Error("Invalid command")

    if command[0] != ("EOF", "0"):
        raise Error("Parser failed to reach end of line")

    return ast


def _parse_expression(expression) -> Node | None:
    """
    Attempts to parse an expression from the given tokens.

    <expression> : <term> { <precedence_1> <term> }

    :return: The parsed expression as an AST.
    """
    left = _parse_term(expression) or None

    # if left is not a term, return None
    if not left:
        return

    while expression[0][0] == "PRECEDENCE 1":
        operator = expression[0][1]
        del expression[0]

        right = _parse_term(expression)

        left = Node(operator, "EXPRESSION", [left, right])

    return left


def _parse_term(term) -> Node | None:
    """
    Attempts to parse a term from the given tokens.

    <term> : <factor> { <precedence_2> <factor> }

    :return: The parsed term as an AST.
    """

    left = _parse_factor(term) or None

    # if left is not a factor, return None
    if not left:
        return

    while term[0][0] == "PRECEDENCE 2":
        operator = term[0][1]
        del term[0]

        right = _parse_factor(term)

        left = Node(operator, "TERM", [left, right])

    return left


def _parse_factor(factor) -> Node | None:
    """
    Attempts to parse a factor from the given tokens.

    <factor> : <number>
             | <variable>
             | <(> expression <)>
    """

    if factor[0] == ("PRECEDENCE 3", "("):
        del factor[0]  # remove left parenthesis
        result = _parse_expression(factor)
        if factor[0] != ("PRECEDENCE 3", ")"):
            raise Error("Expected right parenthesis")
        del factor[0]  # remove right parenthesis
        result = Node(None, "FACTOR", [result])
        return result

    elif factor[0][0] == "NUMBER" or factor[0][0] == "VARIABLE":
        result = Node(factor[0][1], "FACTOR")
        del factor[0]
        return result
    # edge case falls off and returns None


def _parse_assignment(assignment) -> Node | None:
    if assignment[0] == ("KEYWORD", "BEG") and assignment[1][0] == "VARIABLE":
        del assignment[0]
        result = Node(assignment[0], "BEG")
        del assignment[0]
        return result
    elif assignment[0][0] != "VARIABLE" or assignment[1] != ("KEYWORD", "="):
        return

    variable = assignment[0][1]
    del assignment[0]
    del assignment[0]  # remove equal sign

    expression = _parse_expression(assignment)

    return Node(variable, "ASSIGNMENT", [expression])


def _parse_output(output) -> Node | None:
    if output[0] != ("KEYWORD", "PRINT"):
        return

    del output[0]  # remove print keyword

    if output[0][0] == "NUMBER" or output[0][0] == "VARIABLE":
        result = Node(output[0], "OUTPUT")
        del output[0]
        return result


def _parse_exit(exit) -> Node | None:
    if exit[0] != ("KEYWORD", "EXIT!"):
        return
    return Node(None, "EXIT")
