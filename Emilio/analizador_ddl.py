import re


# TIPOS DE DATOS PERMITIDOS
TIPOS_DATOS = [
    "INT",
    "VARCHAR",
    "DECIMAL",
    "DATE",
    "BOOLEAN"
]


def validar_create(sql):
    patron = r"^CREATE\s+TABLE\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.+)\)\s*;?$"

    resultado = re.match(patron, sql, re.IGNORECASE | re.DOTALL)

    if not resultado:
        return False, "Sintaxis incorrecta para CREATE TABLE"

    columnas = resultado.group(2).split(",")

    if not columnas:
        return False, "La tabla debe contener columnas"

    for columna in columnas:
        columna = columna.strip()

        # VARCHAR(100), DECIMAL(10,2)
        patron_columna = (
            r"^([a-zA-Z_][a-zA-Z0-9_]*)\s+"
            r"(INT|VARCHAR|DECIMAL|DATE|BOOLEAN)"
            r"(?:\(\s*\d+(?:\s*,\s*\d+)?\s*\))?$"
        )

        if not re.match(patron_columna, columna, re.IGNORECASE):
            return False, f"Columna inválida: {columna}"

    return True, "CREATE TABLE válido"


def validar_alter(sql):
    patron = (
        r"^ALTER\s+TABLE\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+"
        r"ADD\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+"
        r"(INT|VARCHAR|DECIMAL|DATE|BOOLEAN)"
        r"(?:\(\s*\d+(?:\s*,\s*\d+)?\s*\))?\s*;?$"
    )

    resultado = re.match(patron, sql, re.IGNORECASE)

    if not resultado:
        return False, "Sintaxis incorrecta para ALTER TABLE"

    return True, "ALTER TABLE válido"


def validar_drop(sql):
    patron = r"^DROP\s+TABLE\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*;?$"

    if not re.match(patron, sql, re.IGNORECASE):
        return False, "Sintaxis incorrecta para DROP TABLE"

    return True, "DROP TABLE válido"


def validar_truncate(sql):
    patron = r"^TRUNCATE\s+TABLE\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*;?$"

    if not re.match(patron, sql, re.IGNORECASE):
        return False, "Sintaxis incorrecta para TRUNCATE TABLE"

    return True, "TRUNCATE TABLE válido"


def analizar_ddl(sql):
    sql = sql.strip()

    if re.match(r"^CREATE\s+TABLE", sql, re.IGNORECASE):
        return validar_create(sql)

    elif re.match(r"^ALTER\s+TABLE", sql, re.IGNORECASE):
        return validar_alter(sql)

    elif re.match(r"^DROP\s+TABLE", sql, re.IGNORECASE):
        return validar_drop(sql)

    elif re.match(r"^TRUNCATE\s+TABLE", sql, re.IGNORECASE):
        return validar_truncate(sql)

    else:
        return False, "Sentencia DDL no reconocida"


if __name__ == "__main__":
    # PROGRAMA PRINCIPAL
    print("====================================")
    print("      ANALIZADOR SINTÁCTICO DDL")
    print("====================================")
    
    consulta = input("Ingrese una sentencia SQL: ").strip()
    
    valido, mensaje = analizar_ddl(consulta)
    
    if valido:
        print("✓", mensaje)
    else:
        print("✗", mensaje)