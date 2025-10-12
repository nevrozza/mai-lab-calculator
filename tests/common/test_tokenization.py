import pytest

from src.common.tokenization.tokenizator import Tokenizator
from src.common.tokenization.tokens import tokens_to_expression
from src.common.utils.vars import MEDIUM_TOKEN_RE


def _check(expression: str, exception):
    assert tokens_to_expression(Tokenizator(MEDIUM_TOKEN_RE).tokenize(expression)) == exception


@pytest.mark.parametrize("expression, exception",
                         [
                             ("1,5 + 2,5", "1.5+2.5"),
                             ("10,0 * 2,0", "10.0*2.0"),
                         ]
                         )
def test_comma_to_dot_replacement(expression, exception):
    _check(expression, exception)


@pytest.mark.parametrize("expression, expected",
                         [("-5", "-5"), ("+10", "10"), ("5", "5"), ("-3.14", "-3.14"),
                          ("--2", "2"), ("-+-5", "5"), ("++3", "3"), ("+-+4", "-4"),
                          ("+++2", "2"), ("---3", "-3"), ("-+-+-5", "-5"),
                          ("+5", "5"), ("-10", "-10"), ("+ 3", "3")])
def test_unary_processing(expression, expected):
    _check(expression, expected)


@pytest.mark.parametrize("expression, expected", [("1 2 3", "123"), ("4 5 + 6", "45+6"), ("7 8 9", "789"),
                                                  ("2 3 + 4 5", "23+45"), ("1 0 0", "100"), ("9 9", "99")])
def test_number_concatenation(expression, expected):
    _check(expression, expected)


@pytest.mark.parametrize("expression, expected", [("2(3)", "2*(3)"), ("3(4+5)", "3*(4+5)"), ("(1+1)(2+2)", "(1+1)*(2+2)")])
def test_implicit_multiplication(expression, expected):
    _check(expression, expected)


@pytest.mark.parametrize("expression, expected",
                         [("5+", "5"), ("3*/", "3"), ("1-+", "1"), ("2*", "2"), ("5 + 3 *", "5+3"),
                          ("(2 + 3) *", "(2+3)")])
def test_end_operators_cleanup(expression, expected):
    _check(expression, expected)


@pytest.mark.parametrize("expression, expected",
                         [("2 + 3 * 4", "2+3*4"), ("(2+3)*4", "(2+3)*4"), ("10/2+5", "10/2+5"), ("2**3", "2**3"),
                          ("5//2", "5//2"), ("10%3", "10%3")])
def test_operator_preservation(expression, expected):  # ну мало ли
    _check(expression, expected)
