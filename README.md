# SNOL

by Danica Apostol, Legolas Tyrael Lada, Chris Samuel Salcedo, Mohammad Muraya
Tampugao

## GRAMMAR (modified EBNF):

- Colon `:` denote assignment
- Angle Brackets `< >` denote definitions
- Definitions that contain only uppercase letters, or only symbols, are
  terminal definitions
- Braces `{ }` denote 0 or more
- Parentheses `( )` denote grouping of definitions
- Square Brackets `[ ]` denote optional definitions
- Pipe `|` denote alternative definitions
- Double dots denote a range of alternative definitions
  i.e. `0..4` is equal to `<0> | <1> | <2> | <3> | <4>`
- /EOF/ denotes end of line, or epsilon in EBNF

<hr>

    <command> : ( <expression> 
                | <assignment> 
                | <output> 
                | <EXIT!> 
                ) /EOF/
<hr>

> The precedence rules
> Though cannot be stated in the grammar; <variable> must exist in the
> environment in order to be a valid definition of <factor>.

    <expression> : <term> { <precedence_1> <term> }
    <term> : <factor> { <precedence_2> <factor> }
    <factor> : <number> 
             | <variable>
             | <(> expression <)>
    <number> : <int> | <float>

> The definition of main types

    <int> : [<->] <digit> { <digit> }
    <float> : <int> <.> { <digit> }
    <digit> : 0..9

<hr>

> The definition of assignment, note that though cannot be stated in the
> grammar; keywords are not valid variable names.

    <assignment> : <variable> <=> <expression>
                 | <BEG> <variable>
    <variable> : <letter> { ( <letter> | <digit> ) }
    <letter> : a..z | A..Z

    <output> := <PRINT> ( <variable> | <number> )

