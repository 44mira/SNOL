import re
from interfaces import Token, Error

NUMBER = r"\d+\.?\d*"
VARIABLE = r"[a-zA-Z]+[0-9a-zA-Z]*"
OPERATOR = r"[=+-/*%]"


def lexer(command: str) -> list[Token]:
    definitions = "|".join(["BEG", "PRINT", "EXIT!", NUMBER, VARIABLE, OPERATOR, r"\S"])
    pattern = re.compile(rf"{definitions}")

    tokens = re.findall(pattern, command)

    return _tokenize(tokens)


def _tokenize(tokens: list[str]) -> list[Token]:
    def helper(token: str) -> Token:
        if re.match(NUMBER, token):
            return ("NUMBER", token)
        elif re.match(r"BEG|PRINT|EXIT!|=", token):
            return ("KEYWORD", token)
        elif re.match(r"[+-]", token):
            return ("PRECEDENCE 1", token)
        elif re.match(r"[*/%]", token):
            return ("PRECEDENCE 2", token)
        elif re.match(VARIABLE, token):
            return ("VARIABLE", token)
        else:
            raise Error(f"Invalid token: {token}")

    tokenized = [helper(token) for token in tokens]
    tokenized.append(("EOF", "0"))

    return tokenized
