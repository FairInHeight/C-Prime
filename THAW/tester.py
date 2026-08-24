from .lexer import Lexer


source = """
// C Prime test

class Player
{
    int health;

    void heal()
    {
        health += 10;
    }
}
"""

lexer = Lexer(source)

for token in lexer.tokenize():
    print(
        f"{token.line}:{token.column} "
        f"{token.scope.name:<5} "
        f"{token.dialect.name:<6} "
        f"{token.kind.name:<12} "
        f"{token.lexeme!r}"
    )