from src.common.tokens.regex import EASY_TOKEN_RE
from src.common.tokens.tokens import Token, get_token, TOKEN_TYPES
from src.common.utils import CalcError, debug, warning


def easy_tokenize(expr: str) -> list[Token]:
    """
    # TODO дока
    Используется для задачек Easy
    :param expr: выражение для токенизации
    :return: список токенов
    """
    if not expr.strip():
        raise CalcError("Пустой ввод")
    expr = expr.replace("-", "- ")

    tokens: list[Token] = []

    pos = 0

    while pos < len(expr):
        matched = EASY_TOKEN_RE.match(expr, pos)
        if not matched:
            raise CalcError(f"Некорректный ввод около: '{expr[pos:]}'")

        element = matched.group(1)
        pos = matched.end()
        tokens.append(get_token(element))

    tokens.append(Token(TOKEN_TYPES.EOF))

    debug(expr)
    debug(tokens)
    validated_tokens = validate_tokens(tokens)
    debug(f"После валидации: ${validated_tokens}")
    return validated_tokens


def validate_tokens(tokens: list[Token]) -> list[Token]:
    """

    :param tokens:
    :return:
    """
    result = []
    i = 0
    while i < len(tokens):
        current_token_type = tokens[i].type
        if i + 1 < len(tokens):
            if (current_token_type == TOKEN_TYPES.PLUS and tokens[i + 1].type == TOKEN_TYPES.MINUS) or (
                current_token_type == TOKEN_TYPES.MINUS and tokens[i+1].type == TOKEN_TYPES.PLUS
            ):  # +- -> - TODO: fix --- -> +- (should be just -)
                # -+ -> -
                result.append(Token(TOKEN_TYPES.MINUS))
                warning('"+-" заменено на просто "-"')
                i += 2

            elif current_token_type == tokens[i + 1].type:
                # same token дважды
                # -- -> +
                # ++ -> +
                match current_token_type:
                    case TOKEN_TYPES.MINUS:
                        result.append(Token(TOKEN_TYPES.PLUS))
                        warning('Двойной минус был заменён на "+"')
                        i += 2
                    case TOKEN_TYPES.PLUS:
                        result.append(Token(TOKEN_TYPES.PLUS))
                        warning("Двойной плюс был заменён на просто +")
                        i += 2
        result.append(tokens[i])
        i += 1
    return result
