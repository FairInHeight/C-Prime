from dataclasses import dataclass

<<<<<<< HEAD
from .token import Token, TokenKind, Dialect, Scope
from .dictionary import lookup_keyword
=======
from .token import Dialect, Scope, Token, TokenKind
from .dictionary import lookup_keyword

class LexerMode(Enum):
    NORMAL = auto()
    STRING = auto()
    CHARACTER = auto()
    LINE_COMMENT = auto()
    BLOCK_COMMENT = auto()
>>>>>>> 42b773bd91365e627a1f5d207ccb9d72166ccd20


@dataclass
class LexerState:
    position: int = 0
    line: int = 1
    column: int = 1
    scope: Scope = Scope.FILE


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.state = LexerState()

    def peek(self, offset: int = 0) -> str:
        position = self.state.position + offset

        if position >= len(self.source):
            return ""

        return self.source[position]

    def advance(self) -> str:
        char = self.peek()

        if char == "":
            return ""

        self.state.position += 1

        if char == "\n":
            self.state.line += 1
            self.state.column = 1
        else:
            self.state.column += 1

        return char

    def scan_identifier(self) -> Token:
        start = self.state.position
        line = self.state.line
        column = self.state.column

        while True:
            char = self.peek()

<<<<<<< HEAD
            if not (char.isalnum() or char == "_"):
=======
        lexeme = self.source[start:self.state.position]
        keyword = lookup_keyword(lexeme)

        if keyword:
            kind = keyword.kind
            dialect = keyword.dialect
        else:
            kind = TokenKind.IDENTIFIER
            dialect = Dialect.C

        self.tokens.append(
            Token(
                kind=kind,
                dialect=dialect,
                scope=self.state.scope,
                lexeme=lexeme,
                line=line,
                column=column
            )
        )

    def scan_number(self):
        line = self.state.line
        column = self.state.column
        start = self.state.position

        while self.peek().isdigit():
            self.advance()

        lexeme = self.source[start:self.state.position]

        self.tokens.append(
            Token(
                kind=TokenKind.INTEGER,
                dialect=Dialect.C,
                scope=self.state.scope,
                lexeme=lexeme,
                line=line,
                column=column
            )
        )

    def scan_line_comment(self):
        line = self.state.line
        column = self.state.column
        start = self.state.position

        self.advance()
        self.advance()

        while self.peek() not in ("\n", "\0"):
            self.advance()

        lexeme = self.source[start:self.state.position]

        self.tokens.append(
            Token(
                kind=TokenKind.COMMENT,
                dialect=Dialect.C,
                scope=self.state.scope,
                lexeme=lexeme,
                line=line,
                column=column
            )
        )

    def scan_block_comment(self):
        line = self.state.line
        column = self.state.column
        start = self.state.position

        self.advance()
        self.advance()

        while self.peek() != "\0":
            if self.peek() == "*" and self.peek(1) == "/":
                self.advance()
                self.advance()
>>>>>>> 42b773bd91365e627a1f5d207ccb9d72166ccd20
                break

            self.advance()

        lexeme = self.source[start:self.state.position]

        keyword = lookup_keyword(lexeme)

        if keyword:
            kind = keyword.kind
            dialect = keyword.dialect
        else:
            kind = TokenKind.IDENTIFIER
            dialect = Dialect.C

        return Token(
            kind=kind,
            dialect=dialect,
            lexeme=lexeme,
            line=line,
            column=column,
        )

    def scan_number(self) -> Token:
        start = self.state.position
        line = self.state.line
        column = self.state.column

        is_float = False

        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek(1).isdigit():
            is_float = True
            self.advance()

            while self.peek().isdigit():
                self.advance()

        lexeme = self.source[start:self.state.position]

        return Token(
            kind=TokenKind.FLOAT if is_float else TokenKind.INTEGER,
            dialect=Dialect.C,
            lexeme=lexeme,
            line=line,
            column=column,
        )

    def scan_comment(self) -> Token:
        start = self.state.position
        line = self.state.line
        column = self.state.column

        self.advance()
        self.advance()

        while self.peek() not in ("", "\n"):
            self.advance()

        lexeme = self.source[start:self.state.position]

        return Token(
            kind=TokenKind.COMMENT,
            dialect=Dialect.C,
            lexeme=lexeme,
            line=line,
            column=column,
        )

    def scan_string(self) -> Token:
        start = self.state.position
        line = self.state.line
        column = self.state.column

        self.advance()

        while self.peek() not in ('', '"'):
            self.advance()

        if self.peek() == '"':
            self.advance()

        lexeme = self.source[start:self.state.position]

        return Token(
            kind=TokenKind.STRING,
            dialect=Dialect.C,
            lexeme=lexeme,
            line=line,
            column=column,
        )

    def scan_character(self) -> Token:
        start = self.state.position
        line = self.state.line
        column = self.state.column

        self.advance()

        while self.peek() not in ("", "'"):
            self.advance()

        if self.peek() == "'":
            self.advance()

        lexeme = self.source[start:self.state.position]

        return Token(
            kind=TokenKind.CHARACTER,
            dialect=Dialect.C,
            lexeme=lexeme,
            line=line,
            column=column,
        )

    def scan(self) -> list[Token]:
        tokens = []

        while self.state.position < len(self.source):
            char = self.peek()

            if char.isspace():
                self.advance()
                continue

            if char.isalpha() or char == "_":
                tokens.append(self.scan_identifier())
                continue

            if char.isdigit():
                tokens.append(self.scan_number())
                continue

            if char == "/" and self.peek(1) == "/":
                tokens.append(self.scan_comment())
                continue

            if char == '"':
                tokens.append(self.scan_string())
                continue

            if char == "'":
                tokens.append(self.scan_character())
                continue

            if char in "{}[]();,.":
                line = self.state.line
                column = self.state.column
                lexeme = self.advance()

                tokens.append(
                    Token(
                        kind=TokenKind.PUNCTUATION,
                        dialect=Dialect.C,
                        lexeme=lexeme,
                        line=line,
                        column=column,
                    )
                )
                continue

            line = self.state.line
            column = self.state.column
            lexeme = self.advance()

            tokens.append(
                Token(
                    kind=TokenKind.OPERATOR,
                    dialect=Dialect.C,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                )
            )

        tokens.append(
            Token(
                kind=TokenKind.EOF,
                dialect=Dialect.C,
                lexeme="",
                line=self.state.line,
                column=self.state.column,
            )
        )

<<<<<<< HEAD
        return tokens
=======
    def scan_operator_or_punctuation(self):
        line = self.state.line
        column = self.state.column
        character = self.advance()

        punctuation = "{}[]();,. :".replace(" ", "")

        if character in punctuation:
            kind = TokenKind.PUNCTUATION
        else:
            kind = TokenKind.OPERATOR

        self.tokens.append(
            Token(
                kind=kind,
                dialect=Dialect.C,
                scope=self.state.scope,
                lexeme=character,
                line=line,
                column=column
            )
        )
>>>>>>> 42b773bd91365e627a1f5d207ccb9d72166ccd20
