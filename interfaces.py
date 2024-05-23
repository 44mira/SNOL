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

class Error(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

# A Variable is a tuple of a string and an int or a float,
# denoting the name of the variable and its value.
type Variable = tuple[str, int | float]

# An Environment consists of str-Variable pairs,
# denoting name and their value in memory.
type Environment = Dict[str, Variable]

# A Token is a tuple of two strings, the type of the token, and the value
type Token = tuple[str, str]
