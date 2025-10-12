import pytest

from src.common.utils.errors import EmptyExpressionError, NoNumbersError, FloatTogetherError, InvalidInputError, \
    InvalidExprStartError, InvalidTokenError
from src.implementations.calculator_e1 import CalculatorE1
from tests.common.expressions import EMPTY_ERROR_TESTS, NO_NUMBERS_ERROR_TESTS, FLOAT_TOGETHER_ERROR_TESTS, INVALID_INPUT_ERROR_TESTS, \
    LARGE_NUMS_ERROR_TESTS


def _check(expression, error):
    with pytest.raises(error):
        CalculatorE1().solve(expression)


@pytest.mark.parametrize("expression", EMPTY_ERROR_TESTS)
def test_empty_expression_error(expression):
    _check(expression, EmptyExpressionError)


@pytest.mark.parametrize("expression", NO_NUMBERS_ERROR_TESTS)
def test_no_numbers_error(expression):
    _check(expression, NoNumbersError)


@pytest.mark.parametrize("expression", FLOAT_TOGETHER_ERROR_TESTS)
def test_float_together_error(expression):
    _check(expression, FloatTogetherError)


# "11//12"
@pytest.mark.parametrize("expression", INVALID_INPUT_ERROR_TESTS + ["(1+10)", "10%3",
                                                              "% 3", ])
def test_invalid_input_error(expression):
    _check(expression, InvalidInputError)


@pytest.mark.parametrize("expression", [
    "* 5 + 2",
    "/ 10",
    "** 5",
    "// 10",
])
def test_invalid_expr_start_error(expression):
    _check(expression, InvalidExprStartError)


@pytest.mark.parametrize("expression", [
    "2 + * 3",
    "10 / * 2",
    "2 * / 3",
    "+ * 5",
    "- / 3",
])
def test_invalid_token_error(expression):
    _check(expression, InvalidTokenError)


@pytest.mark.parametrize("expression", [
    "5 / 0",
    "1 / 0",
    "100 / .0",
    "0 / 0.0",
    "1.5 / 0",
])
def test_zero_division_error(expression):
    _check(expression, ZeroDivisionError)


@pytest.mark.parametrize("expression", LARGE_NUMS_ERROR_TESTS)
def test_large_number_conversion_error(expression):
    _check(expression, ValueError)
