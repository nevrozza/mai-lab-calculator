from src.m1.calculator_m1 import CalculatorM1

if __name__ == "__main__":
    calc = CalculatorM1()

    """
    >>> 10**10000
    Traceback (most recent call last):
      File "/Users/nevrozq/Code/mai-py-labs/calculator/src/m1/calculator_m1.py", line 107, in <module>
        print(calc.solve(tokenizator.tokenize(expr)))
        ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ValueError: Exceeds the limit (4300 digits) for integer string conversion; use sys.set_int_max_str_digits() to increase the limit
    """

    """
    >> 10 ** 100 ** 100
    Ничего не вывело...
    """  # TODO: ограничения

    """
    ZeroDivisionError: division by zero (/)
    ZeroDivisionError: integer/float(?) modulo by zero (%)
    ZeroDivisionError: integer/float(?) division or modulo by zero (//)
    """

    """
    >>> 7.5$2
    src.common.utils.errors.CalcError: Некорректный ввод около: '$2'
    """

    """
    >>> 11.5%2
    1.5
    """  # TODO: почему ограничение на только для целых? (то же самое с //)

    """
    >>> (2.5+2.5)/1
    5.0
    """  # TODO: выводить просто 5

    """
    >>> 2.73213126317236127312387128371283912938131 + 10
    12.732131263172361
    """  # TODO: добавить округление

    """
    >>> 2****10
    [Token(NUM, 2), Token(**), Token(**), Token(NUM, 10), Token(EOF)]
    src.common.utils.errors.CalcError: Ожидалось число или открывающая скобка. Получено: Token(**) | pos: 2
    """  # TODO: validate_and_simplify_tokens

    """
    >>> (2+3
    [DEBUG medium_tokenizator.py:18 (tokenize)] (2+3
    [DEBUG medium_tokenizator.py:19 (tokenize)] [Token((), Token(NUM, 2), Token(+), Token(NUM, 3), Token(EOF)]
      File "/Users/nevrozq/Code/mai-py-labs/calculator/src/common/calculator.py", line 22, in _current_token
        return self.tokens[self.pos]
               ~~~~~~~~~~~^^^^^^^^^^
    IndexError: list index out of range
    """  # TODO: безопасный _next()? Или просто ловить ошибку

    """
    >>> 2+3)
    [DEBUG medium_tokenizator.py:18 (tokenize)] 2+3)
    [DEBUG medium_tokenizator.py:19 (tokenize)] [Token(NUM, 2), Token(+), Token(NUM, 3), Token()), Token(EOF)]
    5
    """

    """
    >>> ()
    src.common.utils.errors.CalcError: Ожидалось число или открывающая скобка. Получено: Token()) | pos: 1
    """

    """
    >>> *()
    [DEBUG medium_tokenizator.py:18 (tokenize)] *()
    src.common.utils.errors.CalcError: Ожидалось число или открывающая скобка. Получено: Token(*) | pos: 0
    """

    """
    >>> (+)
    src.common.utils.errors.CalcError: Ожидалось число или открывающая скобка. Получено: Token()) | pos: 2
    """

    """
    >>> ---
    src.common.utils.errors.CalcError: Ожидалось число или открывающая скобка. Получено: Token(EOF) | pos: 3
    """

    """
    >>> 10-
    src.common.utils.errors.CalcError: Ожидалось число или открывающая скобка. Получено: Token(EOF) | pos: 2
    """

    """
    >>> 10+
    src.common.utils.errors.CalcError: Ожидалось число или открывающая скобка. Получено: Token(EOF) | pos: 2
    """

    """
    >>> 2 3
    [Token(NUM, 2), Token(NUM, 3), Token(EOF)]
    2
    """  # TODO: validate if there 2 nums подряд, на проверять EOF нужно (кидать фантомную ошибку?)

    """
    >>> 2 ** 1 ** 2
    2
    """  # TODO: Кидать ворнинг, что оно будет обработано 2 ** (1**2)

    """
    >>> 0 ** 0
    1
    """  # TODO: Подумать, допущение или выводить неопределённость

    """
    >>> 0 ** -1
    ZeroDivisionError: 0.0 cannot be raised to a negative power
    """

    """
    >>> -4 ** 0.5
    (1.2246467991473532e-16+2j) // <class 'complex'>
    """  # TODO: warning, что комплексное число

    """
    >>> (-4)**2**-1
    src.common.utils.errors.CalcError: Ожидалось число или открывающая скобка. Получено: Token(-) | pos: 7
    """

    while True:
        expr = input()
        print(calc.solve(expr))
