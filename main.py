"""
    SNOL Program by:

    Danica Apostol
    Legolas Tyrael Lada
    Chris Samuel Salcedo
    Mohammad Muraya Tampugao

    2-BSCS 2024
"""

from interfaces import Environment


from lexer import lexer
from parser import parser
from evaluator import evaluator
from interfaces import Error

# from evaluator import evaluator


def interpret(command: str, env: Environment):
    """
    Commands are sent here to be interpreted. The environment is passed in the
    case of assignment or accessing operations.

    :param env Environment: the variable environment of the current program
    :param command str: the command to be interpreted
    """

    try:
        tokens = lexer(command)
        ast = parser(tokens)
        evaluator(ast, env)
    except Error as e:
        print(f"Error: {e}")
    except KeyError as e:
        print(f"Error: Variable {e} is not defined")


def eval_loop():
    """
    The Evaluation Loop of the program, also known as the User Interface.
    """
    env: Environment = {}

    while True:
        command = input("\nSNOL $> ")
        interpret(command, env)


def main():
    print(
        "The SNOL Environment is now active, you may proceed with giving your commands\n"
    )
    eval_loop()


if __name__ == "__main__":
    main()
