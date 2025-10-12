import re

DEBUG_TAG: str = "DEBUG"
WARNING_TAG: str = "WARNING"
ERROR_TAG: str = "ОШИБКА"

EASY_TOKEN_PATTERN = r"""
\s*                  # пропускаем пробелы перед каждым токеном
(
    \d*\.?\d+        # число: целое, с точкой, или начинающееся с точки (.5)
  | [+\-*/]          # один из операторов: + - * /
)
"""

EASY_TOKEN_RE = re.compile(EASY_TOKEN_PATTERN, re.VERBOSE)

MEDIUM_TOKEN_PATTERN = r"""
    \s*
    (
        \d*\.?\d+        # число: целое, с точкой, или начинающееся с точки (.5)
      | \*\*                   # ** (обязательно раньше *)
      | //                       # //
      | [%()+\-*/]              # одиночные токены
    )
"""

MEDIUM_TOKEN_RE = re.compile(MEDIUM_TOKEN_PATTERN, re.VERBOSE)
