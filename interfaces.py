from typing import Dict

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


class Token:
    def __init__(self, token_type: str, value: str):
        """
        A Token is defined by its token type and its value.

        These are delimited by spaces or the occurence of a non-conforming
        character
        """
        self.token_type = token_type
        self.value = value


class Variable:
    def __init__(self, var_type: str, value: int | float):
        """
        A Variable is defined by its type and its value.
        """
        self.var_type = var_type
        self.value = value

    def __str__(self) -> str:
        """
        The string representation of a variable is its value and its type
        separated by a colon and wrapped by angle brackets < >.

        :return: string representation of a Variable
        """
        return f"<{self.value} : {self.var_type}>"


# An Environment consists of str-Variable pairs,
# denoting name and their value in memory.
type Environment = Dict[str, Variable]
