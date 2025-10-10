import re

IS_DEBUG_MODE: bool = True  # TODO
DEBUG_TAG: str = "DEBUG"

WARNING_TAG: str = "WARNING"

EASY_TOKEN_PATTERN = r"""
\s*                  # пропускаем пробелы перед каждым токеном
(
    \d+(?:\.\d+)?    # число: целое или с точкой, например 12 или 3.14
  | [+\-*/]          # один из операторов: + - * /
)
"""

EASY_TOKEN_RE = re.compile(EASY_TOKEN_PATTERN, re.VERBOSE)

MEDIUM_TOKEN_PATTERN = r"""
    \s*
    (
        \d+(?:\.\d+)?         # число
      | \*\*                   # ** (обязательно раньше *)
      | //                       # //
      | [%()+\-*/]              # одиночные токены
    )
"""

MEDIUM_TOKEN_RE = re.compile(MEDIUM_TOKEN_PATTERN, re.VERBOSE)
