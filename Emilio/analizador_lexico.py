
import re



# PALABRAS RESERVADAS DEL LENGUAJE

reservadas = [
    # DML
    "SELECT",
    "FROM",
    "WHERE",
    "INSERT",
    "INTO",
    "VALUES",
    "UPDATE",
    "SET",
    "DELETE",

    # DDL
    "CREATE",
    "ALTER",
    "DROP",
    "TRUNCATE",
    "TABLE",
    "ADD",
    "COLUMN",

    # PROCEDIMIENTOS Y FUNCIONES
    "PROCEDURE",
    "FUNCTION",
    "RETURNS",
    "RETURN",
    "BEGIN",
    "END",

    # TRIGGERS
    "TRIGGER",
    "BEFORE",
    "AFTER",
    "ON",
    "FOR",
    "EACH",
    "ROW",

    # TIPOS DE DATOS
    "INT",
    "VARCHAR",
    "DECIMAL",
    "FLOAT",
    "DATE",
    "BOOLEAN",
    "CHAR",
    "TEXT",

    # RESTRICCIONES
    "PRIMARY",
    "KEY",
    "FOREIGN",
    "REFERENCES",
    "NOT",
    "NULL",
    "UNIQUE",
    "DEFAULT",

    # OPERADORES LÓGICOS
    "AND",
    "OR",

    # OTROS
    "AS",
    "JOIN",
    "INNER",
    "LEFT",
    "RIGHT",
    "ORDER",
    "BY",
    "GROUP",
    "HAVING",
    "ASC",
    "DESC"
]


# PATRÓN GENERAL

patron = r"""
    '[^']*'
    |
    \d+\.\d+
    |
    \d+
    |
    >=|<=|<>|!=|=|>|<
    |
    \+|\-|\*|/
    |
    \(|\)
    |
    ,
    |
    ;
    |
    \.
    |
    [A-Za-z_][A-Za-z0-9_]*
"""


# BUSCAR LOS TOKENS
def analizar_lexico(texto):
    tokens = re.findall(
    patron,
    texto,
    re.VERBOSE | re.IGNORECASE
)

    resultado = []


    for token in tokens:

    # PALABRAS RESERVADAS
        if token.upper() in reservadas:
            resultado.append((token.upper(), "PALABRA RESERVADA"))

        # CADENAS
        elif re.fullmatch(r"'[^']*'", token):
            resultado.append((token, "CADENA"))

        # DECIMALES
        elif re.fullmatch(r"\d+\.\d+", token):
            resultado.append((token, "DECIMAL"))

        # NUMEROS ENTEROS
        elif re.fullmatch(r"\d+", token):
            resultado.append((token, "NUMERO"))

        # OPERADORES RELACIONALES
        elif re.fullmatch(r">=|<=|<>|!=|=|>|<", token):
            resultado.append((token, "OPERADOR RELACIONAL"))

        # OPERADORES ARITMETICOS
        elif re.fullmatch(r"\+|\-|\*|/", token):
            resultado.append((token, "OPERADOR ARITMETICO"))

        # PARENTESIS
        elif token == "(":
            resultado.append((token, "PARENTESIS IZQUIERDO"))

        elif token == ")":
            resultado.append((token, "PARENTESIS DERECHO"))

        # COMA
        elif token == ",":
            resultado.append((token, "COMA"))

        # PUNTO Y COMA
        elif token == ";":
            resultado.append((token, "FIN DE SENTENCIA"))

        # PUNTO
        elif token == ".":
            resultado.append((token, "PUNTO"))

        # IDENTIFICADORES
        elif re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token):
            resultado.append((token, "IDENTIFICADOR"))
    return resultado