from abc import ABC, abstractmethod
from re import Pattern

from src.common.tokens.tokens import Token, TOKEN_TYPES
from src.common.utils import CalcError


class Tokenizator(ABC):
    """
    Абстрактный класс для токенизаторов

    Реализует общую логику токенизации
    """

    def __init__(self):
        self.tokens: list[Token] = []
        self.pos: int = 0
        self.expr: str = ""

    @abstractmethod
    def tokenize(self, expr: str) -> list[Token]:
        """
        Переводит выражение в список токенов

        :param expr: Строка с выражением
        :return: Список токенов из выражения
        """

        pass

    def _reinit(self, expr: str):
        """
        Переинициализирует токенизатор для нового выражения
        :param expr: Строка с выражением
        :return: Данная функция ничего не возвращает
        :raises CalcError: Если пустой ввод
        """
        if not expr.strip():
            raise CalcError("Пустой ввод")
        self.tokens.clear()
        self.pos = 0
        self.expr = expr

    def _add_token(self, element: str):
        """
        Преобразовывает элемент в токен(ы) и добавляет его в self.tokens

        ВАЖНО:
        - Число с унарным минусом преобразуется в два токена: MINUS и abs(NUM)
        - Запятые меняются на точки

        :param element: Элемент для преобразования (число, символ)
        """

        element = element.replace(",", ".")
        if element.replace("-", "").replace("+", "").replace(".", "").isdigit():  # TODO: Regex
            value = float(element) if '.' in element else int(element)
            num_token = Token(TOKEN_TYPES.NUM, abs(value))

            if (unary := element[0]) in (TOKEN_TYPES.MINUS.value, TOKEN_TYPES.PLUS.value):
                self.tokens += [Token(TOKEN_TYPES(unary)), num_token]
            else:
                self.tokens.append(num_token)
        else:
            self.tokens.append(Token(TOKEN_TYPES(element)))

    def _get_next_element(self) -> str | None:
        """
        Извлекает следующий элемент выражения с использованием regex паттерна.

        :return: Элемент или None, если достигли последнего элемента
        :raises CalcError: Если не найден следующий элемент.
        """
        if self.pos >= len(self.expr):  # for `outside` while cycle
            return None

        matched = self._token_regex.match(self.expr, self.pos)
        if not matched:
            raise CalcError(f"Некорректный ввод около: '{self.expr[self.pos:]}'")

        element = matched.group(1)
        self.pos = matched.end()
        return element

    @property
    @abstractmethod
    def _token_regex(self) -> Pattern[str]:
        """:return: Regex паттерн для деления выражения на элементы"""
        pass

    @abstractmethod
    def _simplify_tokens(self) -> list[Token]:
        """
        Упрощает токены согласно правилам математики

        Примеры:
            - "---" -> "-"
            - "+-"  -> "-"
            - "++"  -> "+"

        O(N), клянусь
        :return: Список токенов с упрощением
        """
        pass
