# Módulos 
from Emilio.analizador_lexico import analizar_lexico        # Emilio
from Erick.parser_dml import AnalizadorDML                   # Erick
from Cristopher.Triggers import validar_programacion         # Cristopher
from Jonathan.semantic import analizar_semantico, obtener_tablas_registradas, reiniciar_catalogo # Jonathan
# Instancia de DML
parser_dml = AnalizadorDML()

def procesar_consulta(consulta):
    print("\n" + "="*50)
    print(f" PROCESANDO CONSULTA")
    print("="*50)

    # 1. ANÁLISIS LÉXICO
    print("\n--- 1. ANÁLISIS LÉXICO ---")
    tokens = analizar_lexico(consulta)
    if not tokens:
        print(" Error léxico: No se pudieron extraer tokens.")
        return
    
    print(f"Tokens generados ({len(tokens)}):")
    for token, tipo in tokens:
        print(f"  {token:<20} -> {tipo}")

    # 2. ANÁLISIS SINTÁCTICO
    print("\n--- 2. ANÁLISIS SINTÁCTICO ---")
    
    # Identificar tipo de sentencia para enrutar
    primera_palabra = consulta.strip().split()[0].upper() if consulta.strip() else ""
    sintaxis_valida = False
    
    if primera_palabra in ["SELECT", "INSERT", "UPDATE", "DELETE"]:
        sintaxis_valida = parser_dml.validar(consulta)
        tipo_sintaxis = "DML"
    elif primera_palabra == "CREATE":
        # Puede ser CREATE TABLE (DDL) o CREATE PROCEDURE/TRIGGER/FUNCTION
        valido_prog, tipo_prog = validar_programacion(consulta)
        if valido_prog:
            sintaxis_valida = True
            tipo_sintaxis = f"Programación ({tipo_prog})"
        else:
            # Asumimos que es DDL si no es programación
            sintaxis_valida = True
            tipo_sintaxis = "DDL / General"
    else:
        # Otros comandos (DROP, ALTER, TRUNCATE, etc.)
        sintaxis_valida = True
        tipo_sintaxis = "DDL / General"

    if sintaxis_valida:
        print(f"Sintaxis válida identificada como: {tipo_sintaxis}")
    else:
        print(" Error Sintáctico: La estructura gramatical no es válida.")

    # 3. ANÁLISIS SEMÁNTICO
    print("\n--- 3. ANÁLISIS SEMÁNTICO ---")
    semantico_valido, errores = analizar_semantico(consulta)
    if semantico_valido:
        print("Semántica correcta. Tablas y columnas verificadas.")
    else:
        print(" Error Semántico:")
        for err in errores:
            print(f"   {err}")

    # RESULTADO GENERAL
    print("\n" + "-"*50)
    if semantico_valido and sintaxis_valida:
        print("RESULTADO FINAL: CONSULTA VÁLIDA Y CORRECTA")
    else:
        print("RESULTADO FINAL: CONSULTA CON ERRORES")
    print("-"*50 + "\n")

def menu():
    while True:
        print("===================================")
        print(" ANALIZADOR SQL - MENU (WILLIAM, EMILIO, ERICK, JONATHAN, CRISTOPHER) ")
        print("===================================")
        print("1. Analizar consulta SQL")
        print("2. Ver catálogo de tablas en memoria")
        print("3. Reiniciar catálogo de tablas")
        print("4. Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            sql = input("\nIngrese la consulta SQL (ej: SELECT * FROM usuarios;): ")
            procesar_consulta(sql)
        elif opcion == "2":
            tablas = obtener_tablas_registradas()
            print("\n--- TABLAS ACTUALMENTE EN MEMORIA ---")
            for tabla, columnas in tablas.items():
                print(f"  - {tabla}: {columnas}")
            print()
        elif opcion == "3":
            mensaje = reiniciar_catalogo()
            print(f"\n{mensaje}\n")
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida, intente de nuevo.\n")

if __name__ == "__main__":
    menu()