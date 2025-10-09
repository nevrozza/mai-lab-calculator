import re

EASY_TOKEN_PATTERN = r"""
\s*
(
  [+-]?\d+(?:\.\d+)?
  | [+\-*/]
)
"""

EASY_TOKEN_RE = re.compile(EASY_TOKEN_PATTERN, re.VERBOSE)
