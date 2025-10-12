from src.common.tokenization.tokens import TOKEN_TYPES
from src.common.utils.errors import NotIntegerDivisionError, HardToCalculateExpression
from src.common.utils.vars import POW_LIMIT

BASIC_OPERATORS = {
    TOKEN_TYPES.PLUS: lambda a, b: a + b,
    TOKEN_TYPES.MINUS: lambda a, b: a - b
}

MUL_DIV_OPERATORS = {
    TOKEN_TYPES.MUL: lambda a, b: a * b,
    TOKEN_TYPES.DIV: lambda a, b: a / b
}

FLOOR_DIV_OPERATOR = {
    TOKEN_TYPES.FLOOR_DIV: lambda a, b: _floor_div_fun(a, b)
}

MOD_OPERATOR = {
    TOKEN_TYPES.MOD: lambda a, b: _mod_fun(a, b)
}

POW_OPERATOR = {
    TOKEN_TYPES.POW: lambda a, b: _pow_div_fun(a, b)
}


def _pow_div_fun(a, b):
    if b > POW_LIMIT:
        raise HardToCalculateExpression
    return a ** b


def _floor_div_fun(a, b):
    if not a.is_integer() or not b.is_integer():
        raise NotIntegerDivisionError("//")
    return a // b


def _mod_fun(a, b):
    if not a.is_integer() or not b.is_integer():
        raise NotIntegerDivisionError("%")
    return a % b
