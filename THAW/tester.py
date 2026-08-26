from pathlib import Path

from .lexer import Lexer


source_path = Path(__file__).parent.parent / "test.cp"
source = source_path.read_text(encoding="utf-8")

lexer = Lexer(source)
tokens = lexer.scan()

for token in tokens:
    print(
        f"{token.line}:{token.column} "
        f"{token.scope.name:<5} "
        f"{token.dialect.name:<5} "
        f"{token.kind.name:<12} "
        f"{token.lexeme!r}"
    )