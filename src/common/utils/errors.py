from src.common.tokenization.tokens import Token, TOKEN_TYPES, tokens_to_expression
from src.common.utils.messages import error
from src.common.utils.vars import ERROR_TAG


class CalcError(Exception):
    """Класс кастомных ошибок калькулятора"""

    def print_error(self):
        error(self)


class HardToCalculateExpression(CalcError):
    def __init__(self):
        super().__init__("Сложное выражение")


class EmptyExpressionError(CalcError):
    def __init__(self):
        super().__init__("Пустое выражение")


class NoNumbersError(CalcError):
    def __init__(self):
        super().__init__("Где числа")


class FloatTogetherError(CalcError):
    def __init__(self, f1, f2):
        super().__init__(f"Дробное число рядом с другим: {f1} и {f2}")


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
    def __init__(self, tokens: list[Token], pos: int):
        message = "Некорректный ввод: "

        padding = len(message) + len(ERROR_TAG) + 3
        for i in range(pos):
            token = tokens[i]
            padding += len(str(token.value)) if token.type == TOKEN_TYPES.NUM else 1

        super().__init__(f"{message}{tokens_to_expression(tokens)}\n" + ' ' * padding + "^ здесь")


class InvalidParenthesisError(CalcError):
    """
    Ошибка, связанная с неправильным расставлением скобок

    :param has_extra_closing: Если True - значит была ситуация ()), иначе (()
    """

    def __init__(self, has_extra_closing):
        if has_extra_closing:
            message = "Скобок закрыто больше, чем надо =)"
        else:
            message = "Не все открытые скобки были закрыты"

        super().__init__(message)
