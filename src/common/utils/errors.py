from src.common.utils.messages import error
from src.common.utils.vars import ERROR_TAG


class CalcError(Exception):
    """Класс кастомных ошибок калькулятора"""

    def print_error(self):
        error(self)


# Known errors: (их нет смысла добавлять)
# - ValueError: Exceeds the limit (4300 digits) for integer string conversion
# - ZeroDivisionError

# TODO: ZeroDivisionError: 0.0 cannot be raised to a negative power

class EmptyExpressionError(CalcError):
    def __init__(self):
        super().__init__("Пустое выражение")


class NoNumbersError(CalcError):
    def __init__(self):
        super().__init__("Где числа")


class SpaceBetweenFloatsError(CalcError):
    def __init__(self, f1, f2):
        super().__init__(f"Пробел c дробным числом: {f1} и {f2}")


class InvalidInputError(CalcError):
    def __init__(self, unexpected_input):
        super().__init__(f"Некорректный ввод около: {unexpected_input}")


class NotIntegerDivisionError(CalcError):
    """Ошибка при использовании // или % с нецелыми числами"""

    def __init__(self, division_symbol: str):
        super().__init__(f"{division_symbol} только для целых")


class InvalidExprStartError(CalcError):
    def __init__(self, start_symbol: str):
        super().__init__(f"Выражение должно начинаться с '+', '-' или '(' [получено: '{start_symbol}']")


class InvalidTokenError(CalcError):
    def __init__(self, expr: str, pos: int):
        message = "Некорректный ввод: "
        super().__init__(f"{message}{expr}\n" + ' ' * (pos + len(message) + len(ERROR_TAG) + 3) + "^ здесь")


class NotClosedParenthesisError(CalcError):
    def __init__(self):
        super().__init__("Не все открытые скобки были закрыты")
