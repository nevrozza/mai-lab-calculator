import pytest

from src.implementations.calculator_e1 import CalculatorE1
from tests.common.expressions import BASIC_TESTS, PRIORITY_TESTS, UNARY_TESTS


def _check(expression):
    assert CalculatorE1().solve(expression) == eval(expression)


@pytest.mark.parametrize("expression", BASIC_TESTS)
def test_basic_operations(expression): _check(expression)


@pytest.mark.parametrize("expression", PRIORITY_TESTS)
def test_operator_priority(expression): _check(expression)


@pytest.mark.parametrize("expression", UNARY_TESTS)
def test_unary_operators(expression): _check(expression)
