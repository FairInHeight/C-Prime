from dataclasses import dataclass
from ..token import Dialect, TokenKind

@dataclass(frozen=True)
class KeywordInfo:
    lexeme: str
    kind: TokenKind
    dialect: Dialect
    category: str

from .keywords import (
    CONTROL_FLOW,
    STORAGE,
    TYPES,
    TYPE_MODIFIERS,
    QUALIFIERS,
    COMPOUND_TYPES,
    TYPE_OPERATORS,
    C_SPECIAL,

    PRIME_CONTROL_FLOW,
    PRIME_ACCESS,
    PRIME_DECLARATIONS,
    PRIME_TYPES,
    PRIME_MODIFIERS,
    PRIME_COMPOUNDS,
    PRIME_POLYMORPHISM,
    PRIME_SPECIAL,
)

C_KEYWORD_CATEGORIES = {
    "CONTROL_FLOW": CONTROL_FLOW,
    "STORAGE": STORAGE,
    "TYPES": TYPES,
    "TYPE_MODIFIERS": TYPE_MODIFIERS,
    "QUALIFIERS": QUALIFIERS,
    "COMPOUND_TYPES": COMPOUND_TYPES,
    "TYPE_OPERATORS": TYPE_OPERATORS,
    "C_SPECIAL": C_SPECIAL,
}

PRIME_KEYWORD_CATEGORIES = {
    "PRIME_CONTROL_FLOW": PRIME_CONTROL_FLOW,
    "PRIME_ACCESS": PRIME_ACCESS,
    "PRIME_DECLARATIONS": PRIME_DECLARATIONS,
    "PRIME_TYPES": PRIME_TYPES,
    "PRIME_MODIFIERS": PRIME_MODIFIERS,
    "PRIME_COMPOUNDS": PRIME_COMPOUNDS,
    "PRIME_POLYMORPHISM": PRIME_POLYMORPHISM,
    "PRIME_SPECIAL": PRIME_SPECIAL,
}

KEYWORDS = {}

for category, words in C_KEYWORD_CATEGORIES.items():
    for word in words:
        KEYWORDS[word] = KeywordInfo(
            lexeme=word,
            kind=TokenKind.TYPE if category == "TYPES" else TokenKind.KEYWORD,
            dialect=Dialect.C,
            category=category,
        )

for category, words in PRIME_KEYWORD_CATEGORIES.items():
    for word in words:
        KEYWORDS[word] = KeywordInfo(
            lexeme=word,
            kind=TokenKind.TYPE if category == "PRIME_TYPES" else TokenKind.KEYWORD,
            dialect=Dialect.PRIME,
            category=category,
        )

def lookup_keyword(lexeme: str) -> KeywordInfo | None:
    return KEYWORDS.get(lexeme)