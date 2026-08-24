from enum import Enum, auto
from dataclasses import dataclass

class Dialect(Enum):
    C = auto()
    PRIME = auto()


class TokenKind(Enum):
    IDENTIFIER = auto()

    KEYWORD = auto()
    TYPE = auto()

    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    CHARACTER = auto()

    OPERATOR = auto()
    PUNCTUATION = auto()

    COMMENT = auto()

    EOF = auto()

class Scope(Enum):
    FILE = auto()
    CLASS = auto()
    BLOCK = auto()


@dataclass
class Token:
    kind: TokenKind
    dialect: Dialect
    scope: Scope
    lexeme: str
    line: int
    column: int