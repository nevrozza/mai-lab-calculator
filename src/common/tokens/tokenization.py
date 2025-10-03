from src.common.tokens.regex import EASY_TOKEN_RE
from src.common.tokens.tokens import Token, get_token_type, TOKEN_TYPES
from src.common.utils import CalcError, debug


def easy_tokenize(expr: str) -> list[Token]:
    """
    # TODO дока
    Используется для задачек Easy
    :param expr: выражение для токенизации
    :return: список токенов
    """
    if not expr.strip():
        raise CalcError("Пустой ввод")

    tokens: list[Token] = []

    pos = 0

    while pos < len(expr):
        matched = EASY_TOKEN_RE.match(expr, pos)
        if not matched:
            raise CalcError(f"Некорректный ввод около: '{expr[pos:]}'")

        element = matched.group(1)
        pos = matched.end()
        tokens.append(get_token_type(element))

    tokens.append(Token(TOKEN_TYPES.EOF))
    debug(expr)
    debug(tokens)
    return tokens
