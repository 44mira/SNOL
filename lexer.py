import re
from interfaces import Token

NUMBER = r'\d+\.?\d*'
VARIABLE = r'[a-zA-Z]+[0-9a-zA-Z]*'
OPERATOR = r'[=+-/*%]'

def lexer(command: str):
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

def _tokenize(tokens: list):
    for token in tokens:
        if re.match(NUMBER, token):
            yield Token('NUMBER', token)
        elif re.match(r'BEG|PRINT|EXIT!|=', token):
            yield Token('KEYWORD', token)
        elif re.match(r'[+-]', token):
            yield Token('PRECEDENCE 1', token)
        elif re.match(r'[*/%]', token):
            yield Token('PRECEDENCE 2', token)
        elif re.match(VARIABLE, token):
            yield Token('VARIABLE', token)
    yield Token('EOF', "0")
