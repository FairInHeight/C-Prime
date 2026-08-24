from enum import Enum, auto

from .token import Dialect, Scope, Token, TokenKind


class LexerMode(Enum):
    NORMAL = auto()
    STRING = auto()
    CHARACTER = auto()
    LINE_COMMENT = auto()
    BLOCK_COMMENT = auto()


class LexerState:
    def __init__(self):
        self.position = 0
        self.line = 1
        self.column = 1
        self.scope_stack = [Scope.FILE]
        self.mode = LexerMode.NORMAL

    @property
    def scope(self):
        return self.scope_stack[-1]


class Lexer:
    def __init__(self, source):
        self.source = source
        self.state = LexerState()
        self.tokens = []

    def tokenize(self):
        while self.state.position < len(self.source):
            self.scan_token()

        self.tokens.append(
            Token(
                kind=TokenKind.EOF,
                dialect=Dialect.C,
                scope=self.state.scope,
                lexeme="",
                line=self.state.line,
                column=self.state.column
            )
        )

        return self.tokens

    def peek(self, offset=0):
        position = self.state.position + offset

        if position >= len(self.source):
            return "\0"

        return self.source[position]

    def advance(self):
        character = self.peek()

        if character == "\0":
            return character

        self.state.position += 1

        if character == "\n":
            self.state.line += 1
            self.state.column = 1
        else:
            self.state.column += 1

        return character

    def scan_token(self):
        character = self.peek()

        if character.isspace():
            self.advance()
            return

        if character == "/" and self.peek(1) == "/":
            self.scan_line_comment()
            return

        if character == "/" and self.peek(1) == "*":
            self.scan_block_comment()
            return

        if character == '"':
            self.scan_string()
            return

        if character == "'":
            self.scan_character()
            return

        if character.isalpha() or character == "_":
            self.scan_identifier()
            return

        if character.isdigit():
            self.scan_number()
            return

        self.scan_operator_or_punctuation()

    def scan_identifier(self):
        line = self.state.line
        column = self.state.column
        start = self.state.position

        while self.peek().isalnum() or self.peek() == "_":
            self.advance()

        lexeme = self.source[start:self.state.position]

        self.tokens.append(
            Token(
                kind=TokenKind.IDENTIFIER,
                dialect=Dialect.C,
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
                break

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

    def scan_string(self):
        line = self.state.line
        column = self.state.column
        start = self.state.position

        self.advance()

        while self.peek() not in ('"', "\0"):
            if self.peek() == "\\":
                self.advance()

                if self.peek() != "\0":
                    self.advance()
            else:
                self.advance()

        if self.peek() == '"':
            self.advance()

        lexeme = self.source[start:self.state.position]

        self.tokens.append(
            Token(
                kind=TokenKind.STRING,
                dialect=Dialect.C,
                scope=self.state.scope,
                lexeme=lexeme,
                line=line,
                column=column
            )
        )

    def scan_character(self):
        line = self.state.line
        column = self.state.column
        start = self.state.position

        self.advance()

        while self.peek() not in ("'", "\0"):
            if self.peek() == "\\":
                self.advance()

                if self.peek() != "\0":
                    self.advance()
            else:
                self.advance()

        if self.peek() == "'":
            self.advance()

        lexeme = self.source[start:self.state.position]

        self.tokens.append(
            Token(
                kind=TokenKind.CHARACTER,
                dialect=Dialect.C,
                scope=self.state.scope,
                lexeme=lexeme,
                line=line,
                column=column
            )
        )

    def scan_operator_or_punctuation(self):
        line = self.state.line
        column = self.state.column
        character = self.advance()

        punctuation = "{}[]();,.:"

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