from abc import ABC, abstractmethod
from re import Pattern

from src.common.tokenization.tokens import Token, TOKEN_TYPES
from src.common.utils.errors import EmptyExpressionError, InvalidInputError, NoNumbersError, InvalidExprStartError, \
    SpaceBetweenFloatsError


class Tokenizator(ABC):
    """
    Абстрактный класс для токенизаторов

    Реализует общую логику токенизации
    """

    def __init__(self):
        self.tokens: list[Token] = []
        self.pos: int = 0
        self.expr: str = ""
        self.warning_messages: set[str] = set()

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
            raise EmptyExpressionError()
        self.tokens.clear()
        self.warning_messages.clear()
        self.pos = 0
        self.expr = expr.replace(",", ".")

    def _add_token(self, element: str):
        """
        Преобразовывает элемент в токен(ы) и добавляет его в self.tokenization

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
            raise InvalidInputError(self.expr[self.pos:])

        element = matched.group(1)
        self.pos = matched.end()
        return element

    @property
    @abstractmethod
    def _token_regex(self) -> Pattern[str]:
        """:return: Regex паттерн для деления выражения на элементы"""
        pass

    def _validate_and_simplify_tokens(self) -> list[Token]:
        """
        Упрощает токены согласно правилам математики

        Примеры:
            - "---" -> "-"
            - "+-"  -> "-"
            - "++"  -> "+"

        O(N), клянусь
        :return: Список токенов с упрощением
        """

        result = []
        i = 0

        if TOKEN_TYPES.NUM not in [t.type for t in self.tokens]:
            raise NoNumbersError()

        if (first_token_type := self.tokens[i].type) not in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS, TOKEN_TYPES.NUM):
            raise InvalidExprStartError(first_token_type.value)

        while i < len(self.tokens):
            current_type = self.tokens[i].type

            if current_type in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS):
                """
                Обрабатываем ситуации аля
                '---' -> '-'
                '+-' -> '-'
                '--' -> '+'
                """
                sign = 1
                count = 0
                while i < len(self.tokens) and self.tokens[i].type in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS):
                    if self.tokens[i].type == TOKEN_TYPES.MINUS:
                        sign *= -1
                    count += 1
                    i += 1
                if count > 1:
                    self.warning_messages.add("Выражение было упрощено")
                if sign == -1:
                    result.append(Token(TOKEN_TYPES.MINUS))
                elif result:  # Добавляем плюс, только если он НЕ в начале выражения
                    result.append(Token(TOKEN_TYPES.PLUS))
            elif current_type == TOKEN_TYPES.NUM:
                # Обрабатываем числа с пробелом: "1 2" -> "12"
                number_value = self.tokens[i].value
                i += 1

                # Пока следующие токены - числа, совмещаем их
                while i < len(self.tokens) and self.tokens[i].type == TOKEN_TYPES.NUM:
                    next_num = self.tokens[i]
                    if isinstance(number_value, float) or isinstance(next_num.value, float):
                        raise SpaceBetweenFloatsError(number_value, next_num.value)
                    else:
                        number_value = int(str(number_value) + str(next_num.value))
                        self.warning_messages.add("Пробел между числами убран")
                    i += 1

                result.append(Token(TOKEN_TYPES.NUM, number_value))
            else:
                result.append(self.tokens[i])
                i += 1

        while result and result[-1].type in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS,
                                             TOKEN_TYPES.MUL, TOKEN_TYPES.DIV):
            self.warning_messages.add("Удалены лишние операторы в конце")
            result.pop()

        result.append(Token(TOKEN_TYPES.EOF))

        return result
