import pytest

from src.implementations.calculator_m1 import CalculatorM1
from tests.common.expressions import UNARY_TESTS, BASIC_TESTS, PRIORITY_TESTS

M1_BASIC_TESTS = BASIC_TESTS + [
    "10//3",
    "10%3",
    "-10//3",
    "-10%3",

    "10 % (2.5 * 2)",
    "2.0 % 3",
    "5 % 2.0",

    "2.0 // 3",
    "5 // 2.0",
    "10 // (2.5 * 2)",
]

M1_POWER_TESTS = [
    "2**3",
    "2**3**2",
    "(2**3)**2"
]

M1_PRIORITY_TESTS = PRIORITY_TESTS + ["(2+3)*4", "((2+3))+10"]

M1_UNARY_TESTS = UNARY_TESTS + [
    "-2**2",
    "2**-1",
    "-2**-1",
    "+2**2",
    "2**2"
]

M1_MIXED_TESTS = [
    "2+3*4-10/2",
    "(2+3)*(4-1)",
    "10-2**3+5",
    "2*3**2",
    "(2*3)**2",
    "((((12367*199)+(15+13781*1931231))*10++1000)//15)%8",
    "((2**3**2+5*((17-4)**2))//7)%13+((45*67-1234)//56)**2-987*(654//321)",
    "2**3**2**1+5*(17-4)**2//7%13+45*67-1234//56**2-987*654//321+1000",
    "(((12345*67890)+(54321-9876))**2//1000)%777+((888**3-666**2)//55)*11",
    "2**(3+4*5)-17**3//29+45*(67-89//3)**2%77-1234//56+9876*543//210",
]


def _check(expression):
    assert CalculatorM1().solve(expression) == eval(expression)


@pytest.mark.parametrize("expression", M1_BASIC_TESTS)
def test_basic_operations(expression): _check(expression)


@pytest.mark.parametrize("expression", M1_POWER_TESTS)
def test_power_operations(expression): _check(expression)


@pytest.mark.parametrize("expression", M1_PRIORITY_TESTS)
def test_operator_priority(expression): _check(expression)


@pytest.mark.parametrize("expression", M1_UNARY_TESTS)
def test_unary_operators(expression): _check(expression)


@pytest.mark.parametrize("expression", M1_MIXED_TESTS)
def test_mixed_expressions(expression): _check(expression)
