from re import Pattern

from src.common.tokenization.tokens import Token, TOKEN_TYPES
from src.common.utils.errors import EmptyExpressionError, InvalidInputError, NoNumbersError, InvalidExprStartError, \
    SpaceBetweenFloatsError, InvalidParenthesisError
from src.common.utils.messages import debug, warning


class Tokenizator:
    """
    Абстрактный класс для токенизаторов

    Реализует общую логику токенизации
    """

    def __init__(self, token_regex: Pattern[str]):
        self._tokens: list[Token] = []
        self._pos: int = 0
        self._expr: str = ""
        self._warning_messages: set[str] = set()
        self._token_regex = token_regex

    def tokenize(self, expr: str) -> list[Token]:
        """
        Переводит выражение в список токенов

        :param expr: Строка с выражением
        :return: Список токенов из выражения
        """
        self._reinit(expr)

        while (element := self._get_next_element()) is not None:
            self._add_token(element)

        debug(expr)
        debug(self._tokens)

        simplified_tokens = self._validate_and_simplify_tokens()
        debug(f"После упрощения: ${simplified_tokens}")

        if self._warning_messages:
            warning(*self._warning_messages)

        return simplified_tokens

    def _reinit(self, expr: str):
        """
        Переинициализирует токенизатор для нового выражения
        :param expr: Строка с выражением
        :return: Данная функция ничего не возвращает
        :raises CalcError: Если пустой ввод
        """
        if not expr.strip():
            raise EmptyExpressionError()
        self._tokens.clear()
        self._warning_messages.clear()
        self._pos = 0
        self._expr = expr.replace(",", ".")

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
                self._tokens += [Token(TOKEN_TYPES(unary)), num_token]
            else:
                self._tokens.append(num_token)
        else:
            self._tokens.append(Token(TOKEN_TYPES(element)))

    def _get_next_element(self) -> str | None:
        """
        Извлекает следующий элемент выражения с использованием regex паттерна.

        :return: Элемент или None, если достигли последнего элемента
        :raises CalcError: Если не найден следующий элемент.
        """
        if self._pos >= len(self._expr):  # for `outside` while cycle
            return None

        matched = self._token_regex.match(self._expr, self._pos)
        if not matched:
            raise InvalidInputError(self._expr[self._pos:])

        element = matched.group(1)
        self._pos = matched.end()
        return element

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

        parenthesis_stack = []
        result = []
        i = 0

        if TOKEN_TYPES.NUM not in [t.type for t in self._tokens]:
            raise NoNumbersError()

        if (first_token_type := self._tokens[i].type) not in (
        TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS, TOKEN_TYPES.NUM, TOKEN_TYPES.L_PARENTHESIS):
            raise InvalidExprStartError(first_token_type.value)

        while i < len(self._tokens):
            current_token = self._tokens[i]
            current_type = current_token.type

            match current_token.type:
                case TOKEN_TYPES.L_PARENTHESIS:
                    parenthesis_stack.append(TOKEN_TYPES.L_PARENTHESIS.value)
                case TOKEN_TYPES.R_PARENTHESIS:
                    if len(parenthesis_stack) == 0:
                        raise InvalidParenthesisError(True)
                    else:
                        parenthesis_stack.pop()

            if current_type in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS):
                """
                Обрабатываем ситуации аля
                '---' -> '-'
                '+-' -> '-'
                '--' -> '+'
                """
                sign = 1
                count = 0
                while i < len(self._tokens) and self._tokens[i].type in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS):
                    if self._tokens[i].type == TOKEN_TYPES.MINUS:
                        sign *= -1
                    count += 1
                    i += 1
                if count > 1:
                    self._warning_messages.add("Выражение было упрощено")
                if sign == -1:
                    result.append(Token(TOKEN_TYPES.MINUS))
                elif result:  # Добавляем плюс, только если он НЕ в начале выражения
                    result.append(Token(TOKEN_TYPES.PLUS))
            elif current_type == TOKEN_TYPES.NUM:
                # Обрабатываем числа с пробелом: "1 2" -> "12"
                number_value = current_token.value
                i += 1

                # Пока следующие токены - числа, совмещаем их
                while i < len(self._tokens) and self._tokens[i].type == TOKEN_TYPES.NUM:
                    next_num = self._tokens[i]
                    if isinstance(number_value, float) or isinstance(next_num.value, float):
                        raise SpaceBetweenFloatsError(number_value, next_num.value)
                    else:
                        number_value = int(str(number_value) + str(next_num.value))
                        self._warning_messages.add("Пробел между числами убран")
                    i += 1
                result.append(Token(TOKEN_TYPES.NUM, number_value))

                if i < len(self._tokens) and self._tokens[i].type == TOKEN_TYPES.L_PARENTHESIS:
                    result.append(Token(TOKEN_TYPES.MUL))

            elif (current_type == TOKEN_TYPES.R_PARENTHESIS and i + 1 < len(self._tokens)
                  and self._tokens[i + 1].type in (TOKEN_TYPES.L_PARENTHESIS, TOKEN_TYPES.NUM)):
                result.append(current_token)
                result.append(Token(TOKEN_TYPES.MUL))
                i += 1

            else:
                result.append(current_token)
                i += 1

        if parenthesis_stack:
            raise InvalidParenthesisError(False)

        while result and result[-1].type in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS,
                                             TOKEN_TYPES.MUL, TOKEN_TYPES.DIV):
            self._warning_messages.add("Удалены лишние операторы в конце")
            result.pop()

        result.append(Token(TOKEN_TYPES.EOF))

        return result
