# ========================================
# C KEYWORDS
# ========================================

# Control flow
CONTROL_FLOW = {
    "if",
    "else",
    "switch",
    "case",
    "default",
    "for",
    "while",
    "do",
    "break",
    "continue",
    "goto",
    "return",
}

# Storage class specifiers
STORAGE = {
    "typedef",
    "extern",
    "static",
    "auto",
    "register",
    "thread_local",
}

# Types
TYPES = {
    "void",
    "char",
    "int",
    "float",
    "double",
    "_Bool",
    "bool",
}

# Type specifiers / modifiers
TYPE_MODIFIERS = {
    "signed",
    "unsigned",
    "short",
    "long",
}

# Type qualifiers
QUALIFIERS = {
    "const",
    "volatile",
    "restrict",
    "_Atomic",
}

# Compound types
COMPOUND_TYPES = {
    "struct",
    "union",
    "enum",
}

TYPE_OPERATORS = {
    "typeof",
    "typeof_unqual",
}

# C special keywords / constructs
C_SPECIAL = {
    "true",
    "false",
    "sizeof",
    "_Alignof",
    "_Generic",
    "_Static_assert",
    "_Static_assert",
    "nullptr",
    "constexpr",
}


# ========================================
# C PRIME KEYWORDS
# ========================================

# Prime control flow
PRIME_CONTROL_FLOW = {
    "when",
}

# Access control
PRIME_ACCESS = {
    "public",
    "protected",
    "private",
}

# Prime storage / declarations
PRIME_DECLARATIONS = {
    "let",
    "shared",
    "global",
}

# Prime types
PRIME_TYPES = {
    "half",
    "quad",
    "wide",
    "unic",
    "bool",
}

# Prime modifiers
PRIME_COMPOUNDS = {
    "class",
    "final",
}

PRIME_POLYMORPHISM = {
    "morph",
    "ptype",
}

# Prime special keywords / constructs
PRIME_SPECIAL = {
    "event",
    "proc",
}