import re
from interfaces import Token

def lexer(command: str):
    NUMBER = r'\d+\.?\d*'
    VARIABLE = r'[a-zA-Z]+\d*'
    OPERATOR = r'[=+-/*%]'

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

    return tokenize(tokens)

def tokenize(tokens: list):
    for token in tokens:
        if re.match(r'\d+\.?\d*', token):
            yield Token('NUMBER', token)
        elif re.match(r'BEG|PRINT|EXIT!', token):
            yield Token('KEYWORD', token)
        elif re.match(r'[a-zA-Z]+\d*', token):
            yield Token('VARIABLE', token)
        elif re.match(r'[=+-/*%]', token):
            yield Token('OPERATOR', token)
