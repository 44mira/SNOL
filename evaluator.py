from interfaces import Error, Node, Environment


def evaluator(ast: Node, env: Environment):
    """
    :param ast list: the abstract syntax tree to be evaluated
    :param env Environment: the variable environment of the current program
    :return any: the result of the operation
    """

    match ast.node_type:
        case "EXIT":
            return _evaluate_exit()
        case "BEG":
            return _evaluate_beg(str(ast.value), env)
        case "OUTPUT":
            return _evaluate_output(str(ast.value), ast.children[0], env)
        case "EXPRESSION":
            return _evaluate_expression(ast, env)
        case "TERM":
            return _evaluate_term(ast, env)
        case "FACTOR":
            return _evaluate_factor(ast, env)
        case "ASSIGNMENT":
            return _evaluate_assignment(str(ast.value), ast.children[0], env)


def _evaluate_expression(ast: Node, env: Environment) -> int | float:
    if not ast:
        raise Error("Cannot evaluate expression")

    match ast.value:
        case "+":
            op1 = _evaluate_expression(ast.children[0], env)
            op2 = _evaluate_term(ast.children[1], env)

            if type(op1) != type(op2):
                raise Error(f"Cannot add {type(op1)} to {type(op2)}. Type mismatch.")

            return op1 + op2
        case "-":
            op1 = _evaluate_expression(ast.children[0], env)
            op2 = _evaluate_term(ast.children[1], env)

            if type(op1) != type(op2):
                raise Error(
                    f"Cannot subtract {type(op1)} to {type(op2)}. Type mismatch."
                )

            return op1 - op2
        case _:
            return _evaluate_term(ast, env)


def _evaluate_term(ast: Node, env: Environment) -> int | float:
    if not ast:
        raise Error("Cannot evaluate term")

    match ast.value:
        case "*":
            op1 = _evaluate_term(ast.children[0], env)
            op2 = _evaluate_factor(ast.children[1], env)

            if type(op1) != type(op2):
                raise Error(
                    f"Cannot multiply {type(op1)} to {type(op2)}. Type mismatch."
                )

            return op1 * op2
        case "/":
            op1 = _evaluate_term(ast.children[0], env)
            op2 = _evaluate_factor(ast.children[1], env)

            if type(op1) != type(op2):
                raise Error(f"Cannot divide {type(op1)} to {type(op2)}. Type mismatch.")

            if type(op1) == type(0):
                return op1 // op2
            return op1 / op2
        case "%":
            op1 = _evaluate_term(ast.children[0], env)
            op2 = _evaluate_factor(ast.children[1], env)

            if type(op1) != type(op2):
                raise Error(f"Cannot modulo {type(op1)} to {type(op2)}. Type mismatch.")

            return op1 % op2
        case _:
            return _evaluate_factor(ast, env)


def _evaluate_factor(ast: Node, env: Environment) -> int | float:
    if not ast:
        raise Error("Cannot evaluate factor")

    val = str(ast.value)

    try:
        return int(str(val))
    except ValueError:
        try:
            return float(str(val))
        except ValueError:
            if val[0] == "-":
                return -env[val[1:]]
            return env[val]


def _evaluate_assignment(variable: str, value: Node, env: Environment):
    res: int | float
    try:
        res = int(_evaluate_expression(value, env))
    except ValueError:
        res = float(_evaluate_expression(value, env))
    env[variable] = res


def _evaluate_output(output_type: str, value: str, env: Environment):
    if output_type == "VARIABLE":
        print(env[value])
        return
    print(value)


def _evaluate_beg(variable: str, env: Environment):
    value = input(f"\nProvide a value for variable {variable} >> ")

    try:
        value = int(value)
    except ValueError:
        value = float(value)

    env[variable] = value


def _evaluate_exit():
    print("\nExiting SNOL Program...")
    exit(0)
