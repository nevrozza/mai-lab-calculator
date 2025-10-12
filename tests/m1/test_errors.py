import pytest

from src.common.utils.errors import EmptyExpressionError, NoNumbersError, FloatTogetherError, InvalidInputError, \
    NotIntegerDivisionError, InvalidExprStartError, InvalidTokenError, InvalidParenthesisError
from src.implementations.calculator_m1 import CalculatorM1
from tests.common.expressions import EMPTY_ERROR_TESTS, NO_NUMBERS_ERROR_TESTS, FLOAT_TOGETHER_ERROR_TESTS, \
    INVALID_INPUT_ERROR_TESTS, \
    LARGE_NUMS_ERROR_TESTS


def _check(expression, error):
    with pytest.raises(error):
        CalculatorM1().solve(expression)


@pytest.mark.parametrize("expression", EMPTY_ERROR_TESTS)
def test_empty_expression_error(expression):
    _check(expression, EmptyExpressionError)


@pytest.mark.parametrize("expression",
                         NO_NUMBERS_ERROR_TESTS + ["(+)",
                                                   "(-)", ]
                         )
def test_no_numbers_error(expression):
    _check(expression, NoNumbersError)


@pytest.mark.parametrize("expression", FLOAT_TOGETHER_ERROR_TESTS)
def test_float_together_error(expression):
    _check(expression, FloatTogetherError)


@pytest.mark.parametrize("expression", INVALID_INPUT_ERROR_TESTS)
def test_invalid_input_error(expression):
    _check(expression, InvalidInputError)


@pytest.mark.parametrize("expression", [
    "5.5 // 2",
    "10 // 2.5",
    "3.14 // 1.5",
    "1.1 // 2.2",
    "(5.5 + 2) // 3",
])
def test_not_integer_division_error_floor_div(expression):
    _check(expression, NotIntegerDivisionError)


@pytest.mark.parametrize("expression", [
    "5.5 % 2",
    "10 % 2.5",
    "3.14 % 1.5",
    "1.1 % 2.2",
    "(5.5 + 2) % 3",
])
def test_not_integer_division_error_modulo(expression):
    _check(expression, NotIntegerDivisionError)


@pytest.mark.parametrize("expression", [
    "* 5 + 2",
    "/ 10",
    ") 2 + 3",
    "** 5",
    "// 10",
    "% 3",
    ")5 + 3(",
    ")(2 + 3)(",
])
def test_invalid_expr_start_error(expression):
    _check(expression, InvalidExprStartError)


@pytest.mark.parametrize("expression", [
    "2 + * 3",
    "(5 + ) 3",
    "10 * (2 + )",
    "2 ** * 3",
    "5 // / 2",
    "2 + (3 *)",
])
def test_invalid_token_error(expression):
    _check(expression, InvalidTokenError)


@pytest.mark.parametrize("expression", [
    "(2 + 3))",
    "((2+3)))",
    "2+(3* 4))",
    "((1+2)) + 3)",
    "1 + (2 + 3)))",
    "(32131))(",
])
def test_invalid_parenthesis_error_extra_closing(expression):
    _check(expression, InvalidParenthesisError)


@pytest.mark.parametrize("expression", [
    "(2 + 3",
    "((2 + 3) *(4-1",
    "(((5 + 2) * 3",
    "(1 + (2 * (3 + 4)",
    "((1+2)*(3+4)",
    "(((5+2)*3",
])
def test_invalid_parenthesis_error_unclosed(expression):
    _check(expression, InvalidParenthesisError)


@pytest.mark.parametrize("expression", [
    "5 / 0",
    "10 / (5 - 5)",
    "(2 + 3) / 0",
    "1 / (2 - 1 - 1)",
    "100 / (10 * 0)",
    "(5 * 2) / 0",
    "1.5 / 0",
    "0.0 / 0.0",
    "0**-1"
])
def test_zero_division_error_regular_div(expression):
    _check(expression, ZeroDivisionError)


@pytest.mark.parametrize("expression", [
    "5 // 0",
    "10 // (3 - 3)",
    "(15 + 5) // 0",
    "100 // (10 * 0)",
    "25 // (5 - 5)",
])
def test_zero_division_error_floor_div(expression):
    _check(expression, ZeroDivisionError)


@pytest.mark.parametrize("expression", [
    "5 % 0",
    "10 % (2 - 2)",
    "(20 + 4) % 0",
    "100 % (25 * 0)",
    "15 % (3 - 3)",
])
def test_zero_division_error_modulo(expression):
    _check(expression, ZeroDivisionError)


@pytest.mark.parametrize("expression", LARGE_NUMS_ERROR_TESTS + [
    "2.1**1000"
])
def test_large_number_conversion_error(expression):
    _check(expression, (ValueError, OverflowError))
