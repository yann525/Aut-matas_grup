import re


catalogo = {
    "usuarios": ["id", "nombre", "edad"],
    "productos": ["id", "nombre", "precio"],
    "ventas": ["id", "usuario_id", "producto_id", "cantidad", "fecha"],
}


def _limpiar(consulta):
    consulta = consulta.strip()
    if consulta.endswith(";"):
        consulta = consulta[:-1]
    return consulta.strip()


def _tabla_existe(tabla):
    return tabla.lower() in catalogo


def _columnas_de(tabla):
    return catalogo.get(tabla.lower(), [])


def _extraer_columnas_lista(texto):
    columnas = [c.strip() for c in texto.split(",")]
    return [c for c in columnas if c]


def _analizar_select(consulta):
    errores = []
    match = re.search(
        r"SELECT\s+(.*?)\s+FROM\s+([A-Za-z_][A-Za-z0-9_]*)",
        consulta, re.IGNORECASE | re.DOTALL
    )
    if not match:
        return ["Error semantico:\nNo se pudo identificar la tabla en el SELECT."]
    columnas_texto = match.group(1).strip()
    tabla = match.group(2).strip()
    if not _tabla_existe(tabla):
        errores.append(f'Error semantico:\nLa tabla "{tabla}" no existe.')
        return errores
    if columnas_texto != "*":
        columnas_pedidas = _extraer_columnas_lista(columnas_texto)
        columnas_validas = _columnas_de(tabla)
        for col in columnas_pedidas:
            if col.lower() not in [c.lower() for c in columnas_validas]:
                errores.append(
                    f'Error semantico:\nLa columna "{col}" no existe en la tabla {tabla}.'
                )
    return errores


def _analizar_insert(consulta):
    errores = []
    match = re.search(
        r"INSERT\s+INTO\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)",
        consulta, re.IGNORECASE | re.DOTALL
    )
    if not match:
        return ["Error semantico:\nNo se pudo identificar la tabla en el INSERT."]
    tabla = match.group(1).strip()
    columnas_texto = match.group(2).strip()
    if not _tabla_existe(tabla):
        errores.append(f'Error semantico:\nLa tabla "{tabla}" no existe.')
        return errores
    columnas_pedidas = _extraer_columnas_lista(columnas_texto)
    columnas_validas = _columnas_de(tabla)
    for col in columnas_pedidas:
        if col.lower() not in [c.lower() for c in columnas_validas]:
            errores.append(
                f'Error semantico:\nLa columna "{col}" no existe en la tabla {tabla}.'
            )
    return errores


def _analizar_update(consulta):
    errores = []
    match = re.search(
        r"UPDATE\s+([A-Za-z_][A-Za-z0-9_]*)\s+SET\s+(.*?)(?:\s+WHERE\s+.*)?$",
        consulta, re.IGNORECASE | re.DOTALL
    )
    if not match:
        return ["Error semantico:\nNo se pudo identificar la tabla en el UPDATE."]
    tabla = match.group(1).strip()
    set_texto = match.group(2).strip()
    if not _tabla_existe(tabla):
        errores.append(f'Error semantico:\nLa tabla "{tabla}" no existe.')
        return errores
    asignaciones = _extraer_columnas_lista(set_texto)
    columnas_validas = _columnas_de(tabla)
    for asignacion in asignaciones:
        col = asignacion.split("=")[0].strip()
        if col.lower() not in [c.lower() for c in columnas_validas]:
            errores.append(
                f'Error semantico:\nLa columna "{col}" no existe en la tabla {tabla}.'
            )
    return errores


def _analizar_delete(consulta):
    errores = []
    match = re.search(
        r"DELETE\s+FROM\s+([A-Za-z_][A-Za-z0-9_]*)",
        consulta, re.IGNORECASE
    )
    if not match:
        return ["Error semantico:\nNo se pudo identificar la tabla en el DELETE."]
    tabla = match.group(1).strip()
    if not _tabla_existe(tabla):
        errores.append(f'Error semantico:\nLa tabla "{tabla}" no existe.')
    return errores


def _analizar_drop(consulta):
    errores = []
    match = re.search(
        r"DROP\s+TABLE\s+([A-Za-z_][A-Za-z0-9_]*)",
        consulta, re.IGNORECASE
    )
    if not match:
        return ["Error semantico:\nNo se pudo identificar la tabla en el DROP."]
    tabla = match.group(1).strip()
    if not _tabla_existe(tabla):
        errores.append(
            "Error semantico:\nNo se puede eliminar la tabla porque no existe."
        )
    else:
        del catalogo[tabla.lower()]
    return errores


def _analizar_truncate(consulta):
    errores = []
    match = re.search(
        r"TRUNCATE\s+TABLE\s+([A-Za-z_][A-Za-z0-9_]*)",
        consulta, re.IGNORECASE
    )
    if not match:
        return ["Error semantico:\nNo se pudo identificar la tabla en el TRUNCATE."]
    tabla = match.group(1).strip()
    if not _tabla_existe(tabla):
        errores.append(
            "Error semantico:\nNo se puede vaciar la tabla porque no existe."
        )
    return errores


def _analizar_create(consulta):
    errores = []
    match = re.search(
        r"CREATE\s+TABLE\s+([A-Za-z_][A-Za-z0-9_]*)\s*\((.*)\)",
        consulta, re.IGNORECASE | re.DOTALL
    )
    if not match:
        return ["Error semantico:\nNo se pudo identificar la tabla en el CREATE TABLE."]
    tabla = match.group(1).strip()
    definicion = match.group(2).strip()
    if _tabla_existe(tabla):
        errores.append(f'Error semantico:\nLa tabla "{tabla}" ya existe.')
        return errores
    columnas_nuevas = []
    for parte in definicion.split(","):
        parte = parte.strip()
        if parte:
            nombre_col = parte.split()[0]
            columnas_nuevas.append(nombre_col)
    catalogo[tabla.lower()] = columnas_nuevas
    return errores


def _analizar_alter(consulta):
    errores = []
    match = re.search(
        r"ALTER\s+TABLE\s+([A-Za-z_][A-Za-z0-9_]*)\s+ADD\s+([A-Za-z_][A-Za-z0-9_]*)",
        consulta, re.IGNORECASE
    )
    if not match:
        return ["Error semantico:\nNo se pudo identificar la tabla en el ALTER TABLE."]
    tabla = match.group(1).strip()
    columna_nueva = match.group(2).strip()
    if not _tabla_existe(tabla):
        errores.append(f'Error semantico:\nLa tabla "{tabla}" no existe.')
        return errores
    if columna_nueva.lower() in [c.lower() for c in _columnas_de(tabla)]:
        errores.append(
            f'Error semantico:\nLa columna "{columna_nueva}" ya existe en la tabla {tabla}.'
        )
    else:
        catalogo[tabla.lower()].append(columna_nueva)
    return errores


def analizar_semantico(consulta):
    consulta = _limpiar(consulta)
    primera_palabra = consulta.strip().split()[0].upper() if consulta.strip() else ""
    if primera_palabra == "SELECT":
        errores = _analizar_select(consulta)
    elif primera_palabra == "INSERT":
        errores = _analizar_insert(consulta)
    elif primera_palabra == "UPDATE":
        errores = _analizar_update(consulta)
    elif primera_palabra == "DELETE":
        errores = _analizar_delete(consulta)
    elif primera_palabra == "DROP":
        errores = _analizar_drop(consulta)
    elif primera_palabra == "TRUNCATE":
        errores = _analizar_truncate(consulta)
    elif primera_palabra == "CREATE":
        errores = _analizar_create(consulta)
    elif primera_palabra == "ALTER":
        errores = _analizar_alter(consulta)
    else:
        errores = [f'Error semantico:\nSentencia no reconocida: "{primera_palabra}".']
    es_valida = len(errores) == 0
    return es_valida, errores


if __name__ == "__main__":
    print("\n--- ANALIZADOR SEMANTICO (modo de prueba) ---")
    print("Tablas disponibles en el catalogo:")
    for tabla, columnas in catalogo.items():
        print(f"  - {tabla}: {columnas}")
    consulta = input("\nIngrese su consulta SQL: ").strip()
    es_valida, errores = analizar_semantico(consulta)
    print()
    if es_valida:
        print("CONSULTA SEMANTICAMENTE CORRECTA")
    else:
        for error in errores:
            print(error)
            print()
