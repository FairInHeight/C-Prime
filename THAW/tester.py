from THAW.dictionary import lookup_keyword


tests = [
    "int",
    "bool",
    "if",
    "public",
    "morph",
    "typeof",
    "class",
    "potato",
]

for word in tests:
    result = lookup_keyword(word)
    print(f"{word}: {result}")