import re
from re import Pattern

from src.common.tokenization.tokens import Token, TOKEN_TYPES
from src.common.tokenization.tokens_validator import TokensValidator
from src.common.utils.errors import EmptyExpressionError, InvalidInputError
from src.common.utils.messages import debug, warning


class Tokenizator:

    def __init__(self, token_regex: Pattern[str]):
        """
        :type token_regex: Скомпилированное регулярное выражение для извлечения токенов
        """
        self._tokens: list[Token] = []
        self._pos: int = 0
        self._expr: str = ""
        self._token_regex = token_regex

    def _reinit(self, expr: str):
        """ВАЖНО: заменяет запятые на точки (python decimal style)"""
        self._tokens.clear()
        self._pos = 0
        self._expr = expr.replace(",", ".")

    def tokenize(self, expr: str) -> list[Token]:
        """
        Переводит выражение в список токенов

        Алгоритм:
            1) Проверка на пустоту
            2) Разбиение на токены с помощью regex
            3) Валидация и упрощение токенов

        :param expr: Строка с выражением
        :return: Список токенов из выражения
        """
        if not expr.strip():
            raise EmptyExpressionError()

        self._reinit(expr)

        while (element := self._get_next_element()) is not None:
            self._add_token(element)

        debug(expr)
        debug(self._tokens)

        tokens_validator = TokensValidator()

        simplified_tokens = tokens_validator.validate_and_simplify_tokens(self._tokens)
        debug(f"После упрощения: ${simplified_tokens}")

        if tokens_validator.warning_messages:
            warning(*tokens_validator.warning_messages)

        return simplified_tokens

    def _add_token(self, element: str):
        """
        Преобразовывает элемент в токен(ы) и добавляет его в self.tokenization

        ВАЖНО:
        - Число с унарным минусом преобразуется в два токена: MINUS и abs(NUM)

        :param element: Элемент для преобразования (число, символ)
        """

        if re.match(r'^[-+]?\d*\.?\d+$', element):
            value = float(element) if '.' in element else int(element)
            num_token = Token(TOKEN_TYPES.NUM, abs(value))

            if (unary := element[0]) in (TOKEN_TYPES.MINUS.value, TOKEN_TYPES.PLUS.value):
                self._tokens += [Token(TOKEN_TYPES(unary)), num_token]
            else:
                self._tokens.append(num_token)
        else:
            self._tokens.append(Token(TOKEN_TYPES(element)))

    def _get_next_element(self) -> str | None:
        """
        Извлекает следующий элемент выражения с использованием regex паттерна.

        :return: Элемент или None, если достигли последнего элемента
        :raises InvalidInputError: Если найден лишний символ
        """
        if self._pos >= len(self._expr):  # for `outside` while cycle
            return None

        matched = self._token_regex.match(self._expr, self._pos)
        if not matched:
            raise InvalidInputError(self._expr[self._pos:])

        element = matched.group(1)
        self._pos = matched.end()
        return element
