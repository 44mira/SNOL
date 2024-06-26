from typing import Dict, TypeAlias

"""
GRAMMAR (modified EBNF):

- Colon `:` denote assignment
- Angle Brackets `< >` denote definitions
- Definitions that contain only uppercase letters, or only symbols, are
  terminal definitions
- Braces `{ }` denote 0 or more
- Parentheses `( )` denote grouping of definitions
- Square Brackets `[ ]` denote optional definitions
- Pipe `|` denote alternative definitions
- Double dots denote a range of alternative definitions
  i.e. 0..4 is equal to <0> | <1> | <2> | <3> | <4>
- Double Hashtags `##` denote comments
- /EOF/ denotes end of line, or epsilon in EBNF

## ########################################################################

<command> : ( <expression> 
            | <assignment> 
            | <output> 
            | <EXIT!> 
            ) /EOF/

## ########################################################################

## The precedence rules
## Though cannot be stated in the grammar; <variable> must exist in the
## environment in order to be a valid definition of <factor>.

<expression> : <term> { <precedence_1> <term> }
<term> : <factor> { <precedence_2> <factor> }
<factor> : <number> 
         | <variable>
         | <(> expression <)>
<number> : <int> | <float>

## The definition of main types

<int> : [<->] <digit> { <digit> }
<float> : <int> <.> { <digit> }
<digit> : 0..9

## ########################################################################

## The definition of assignment, note that though cannot be stated in the
## grammar; keywords are not valid variable names.

<assignment> : <variable> <=> <expression>
             | <BEG> <variable>
<variable> : <letter> { ( <letter> | <digit> ) }
<letter> : a..z | A..Z

<output> := <PRINT> ( <variable> | <number> )

"""


class Node:
    def __init__(self, value: str | None, node_type: str, children=[]) -> None:
        self.value = value
        self.node_type = node_type
        self.children = children

    def __str__(self) -> str:
        if not self.children:
            return f"<{self.node_type} {self.value}>"

        children = ", ".join([f"{child}" for child in self.children])

        return f"<{self.node_type} {self.value}> ({children})"

    def __eq__(self, other) -> bool:
        tests = [
            self.value == other.value,
            self.node_type == other.node_type,
            self.children == other.children,
        ]

        return all(tests)


class Error(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


# An Environment consists of str-Variable pairs,
# denoting name and their value in memory.
Environment: TypeAlias = Dict[str, int | float]

# A Token is a tuple of two strings, the type of the token, and the value
Token: TypeAlias = tuple[str, str]
