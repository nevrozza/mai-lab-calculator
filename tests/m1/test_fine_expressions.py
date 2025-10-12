import pytest

from src.implementations.calculator_m1 import CalculatorM1
from tests.common.expressions import UNARY_TESTS, BASIC_TESTS, PRIORITY_TESTS

M1_BASIC_EXPRESSIONS = BASIC_TESTS + [
    "10//3",
    "10%3",
    "-10//3",
    "-10%3"
]

M1_POWER_EXPRESSIONS = [
    "2**3",
    "2**3**2",
    "(2**3)**2"
]

M1_PRIORITY_EXPRESSIONS = PRIORITY_TESTS + ["(2+3)*4", "((2+3))+10"]

M1_UNARY_EXPRESSIONS = UNARY_TESTS + [
    "-2**2",
    "2**-1",
    "-2**-1",
    "+2**2",
    "2**2"
]

M1_MIXED_EXPRESSIONS = [
    "2+3*4-10/2",
    "(2+3)*(4-1)",
    "10-2**3+5",
    "2*3**2",
    "(2*3)**2"
]


def _check(expression):
    assert CalculatorM1().solve(expression) == eval(expression)


@pytest.mark.parametrize("expression", M1_BASIC_EXPRESSIONS)
def test_basic_operations(expression): _check(expression)


@pytest.mark.parametrize("expression", M1_POWER_EXPRESSIONS)
def test_power_operations(expression): _check(expression)


@pytest.mark.parametrize("expression", M1_PRIORITY_EXPRESSIONS)
def test_operator_precedence(expression): _check(expression)


@pytest.mark.parametrize("expression", M1_UNARY_EXPRESSIONS)
def test_unary_operators(expression): _check(expression)


@pytest.mark.parametrize("expression", M1_MIXED_EXPRESSIONS)
def test_mixed_expressions(expression): _check(expression)
