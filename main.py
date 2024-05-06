"""
    SNOL Program by:

    Danica Apostol
    Legolas Tyrael Lada
    Chris Samuel Salcedo
    Mohammad Muraya Tampugao

    2-BSCS 2024
"""

from interfaces import Environment

#  TODO:
# - Lexer
# - Parser
# - Evaluator

# from lexer import lexer
# from parser import parser
# from evaluator import evaluator


def interpret(command: str, env: Environment):
    """
    Commands are sent here to be interpreted. The environment is passed in the
    case of assignment or accessing operations.

    :param env Environment: the variable environment of the current program
    :param command str: the command to be interpreted
    """

    # tokens = lexer(command)
    # ast = parser(tokens)
    # result = evaluator(ast, env)

    # ...


def eval_loop():
    """
    The Evaluation Loop of the program, also known as the User Interface.
    """
    env: Environment = {}

    while True:
        command = input("Command: ")
        interpret(command, env)


def main():
    print(
        "The SNOL Environment is now active, \
          you may proceed with giving your commands"
    )
    eval_loop()


if __name__ == "__main__":
    main()
