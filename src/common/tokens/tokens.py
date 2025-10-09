from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Token:
    """
    Дата класс, хранящий данные о токене (тип и значение)

    ВАЖНО: если тип != NUM, то value = None
    """
    type: 'TOKEN_TYPES'
    value: int | float | None = None

    def __str__(self):
        if self.type == TOKEN_TYPES.NUM:
            return f"Token(NUM, {self.value})"
        else:
            return f"Token({self.type.value})"

    def __repr__(self):
        return self.__str__()


# noinspection PyPep8Naming
class TOKEN_TYPES(Enum):
    """
        ENUM класс, который используется для хранения констант:
        NUM, PLUS, MINUS, MUL(*), DIV(/), EOF
    """
    NUM = "NUM"
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    EOF = "EOF"
