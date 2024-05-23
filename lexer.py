import re
from typing import Generator
from interfaces import Token

NUMBER = r'\d+\.?\d*'
VARIABLE = r'[a-zA-Z]+[0-9a-zA-Z]*'
OPERATOR = r'[=+-/*%]'

def lexer(command: str) -> Generator[Token, list[str], None]:
    definitions = '|'.join([
        'BEG',
        'PRINT',
        'EXIT!',         
        NUMBER,
        VARIABLE,
        OPERATOR
    ])
    pattern = re.compile(rf"{definitions}")

    tokens = re.findall(pattern, command)

    return _tokenize(tokens)

def _tokenize(tokens: list) -> Generator[Token, list[str], None]:
    for token in tokens:
        if re.match(NUMBER, token):
            yield ('NUMBER', token)
        elif re.match(r'BEG|PRINT|EXIT!|=', token):
            yield ('KEYWORD', token)
        elif re.match(r'[+-]', token):
            yield ('PRECEDENCE 1', token)
        elif re.match(r'[*/%]', token):
            yield ('PRECEDENCE 2', token)
        elif re.match(VARIABLE, token):
            yield ('VARIABLE', token)
    yield ('EOF', "0")
