from dataclasses import dataclass

from .token import Token, TokenKind, Dialect, Scope
from .dictionary import lookup_keyword


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

            if not (char.isalnum() or char == "_"):
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

        return tokens