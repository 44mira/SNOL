from typing import Dict


class Variable:
    def __init__(self, var_type, value):
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
