import re

IS_DEBUG_MODE: bool = True  # TODO
DEBUG_TAG: str = "DEBUG"

WARNING_TAG: str = "WARNING"

EASY_TOKEN_PATTERN = r"""
\s*
(
  [+-]?\d+(?:\.\d+)?
  | [+\-*/]
)
"""

EASY_TOKEN_RE = re.compile(EASY_TOKEN_PATTERN, re.VERBOSE)
