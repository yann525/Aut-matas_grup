
import re


texto = input("Ingrese su consulta: ").strip()


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

tokens = re.findall(
    patron,
    texto,
    re.VERBOSE | re.IGNORECASE
)


print("\n--- ANALIZADOR LEXICO ---\n")


for token in tokens:

    # PALABRAS RESERVADAS

    if token.upper() in reservadas:

        print(token.upper(), "-> PALABRA RESERVADA")


    # CADENAS

    elif re.fullmatch(r"'[^']*'", token):

        print(token, "-> CADENA")


    # DECIMALES

    elif re.fullmatch(r"\d+\.\d+", token):

        print(token, "-> DECIMAL")


    # NUMEROS ENTEROS

    elif re.fullmatch(r"\d+", token):

        print(token, "-> NUMERO")


    # OPERADORES RELACIONALES

    elif re.fullmatch(r">=|<=|<>|!=|=|>|<", token):

        print(token, "-> OPERADOR RELACIONAL")


    # OPERADORES ARITMETICOS

    elif re.fullmatch(r"\+|\-|\*|/", token):

        print(token, "-> OPERADOR ARITMETICO")


    # PARENTESIS

    elif token == "(":

        print(token, "-> PARENTESIS IZQUIERDO")


    elif token == ")":

        print(token, "-> PARENTESIS DERECHO")


    # COMA

    elif token == ",":

        print(token, "-> COMA")


    # PUNTO Y COMA

    elif token == ";":

        print(token, "-> FIN DE SENTENCIA")


    # PUNTO

    elif token == ".":

        print(token, "-> PUNTO")


    # IDENTIFICADORES

    elif re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token):

        print(token, "-> IDENTIFICADOR")

