import sys
import os

# Añadir el directorio raíz al path para poder importar los módulos de los compañeros
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Emilio.analizador_lexico import analizar_lexico
from Emilio.analizador_ddl import analizar_ddl
from Erick.parser_dml import AnalizadorDML
from Cristopher.Triggers import validar_programacion
from Jonathan.semantic import analizar_semantico

parser_dml = AnalizadorDML()

def realizar_analisis(consulta):
    print("\nANÁLISIS LÉXICO:")
    tokens = analizar_lexico(consulta)
    if not tokens:
        print("✗ Error léxico: No se pudieron extraer tokens.\n")
    else:
        print("✓ Sin errores\n")
        print("TOKENS:")
        for token, tipo in tokens:
            print(f"{token} → {tipo}")
        print()

    print("ANÁLISIS SINTÁCTICO:")
    # Identificar tipo de sentencia para enrutar
    primera_palabra = consulta.strip().split()[0].upper() if consulta.strip() else ""
    sintaxis_valida = False
    
    if primera_palabra in ["SELECT", "INSERT", "UPDATE", "DELETE"]:
        sintaxis_valida = parser_dml.validar(consulta)
    elif primera_palabra in ["CREATE", "ALTER", "DROP", "TRUNCATE"]:
        valido_prog, _ = validar_programacion(consulta)
        if valido_prog:
            sintaxis_valida = True
        else:
            valido_ddl, _ = analizar_ddl(consulta)
            sintaxis_valida = valido_ddl
    else:
        sintaxis_valida = False

    if sintaxis_valida:
        print("✓ Consulta válida\n")
    else:
        print("✗ Error Sintáctico\n")

    print("ANÁLISIS SEMÁNTICO:")
    semantico_valido, errores = analizar_semantico(consulta)
    if semantico_valido:
        print("✓ Tabla existente")
        print("✓ Columnas válidas\n")
    else:
        for err in errores:
            print(f"✗ {err}")
        print()

    print("RESULTADO FINAL:")
    if tokens and sintaxis_valida and semantico_valido:
        print("✓ CONSULTA CORRECTA\n")
    else:
        print("✗ CONSULTA CON ERRORES\n")

def main():
    while True:
        print("====================================")
        print("         ANALIZADOR DE SQL")
        print("====================================")
        print("Seleccione una opción:")
        print("1. Analizar DML")
        print("2. Analizar DDL")
        print("3. Analizar Procedimientos")
        print("4. Analizar Triggers")
        print("5. Analizar consulta automáticamente")
        print("6. Ver tokens generados")
        print("7. Salir")
        
        opcion = input("\nIngrese una opción: ")
        
        if opcion == '7':
            print("Saliendo del analizador...")
            break
        elif opcion in ['1', '2', '3', '4', '5']:
            consulta = input("Ingrese consulta SQL: ")
            realizar_analisis(consulta)
        elif opcion == '6':
            consulta = input("Ingrese consulta SQL para ver tokens: ")
            tokens = analizar_lexico(consulta)
            print("\n--- Tokens Generados ---")
            if tokens:
                for token, tipo in tokens:
                    print(f"{token} → {tipo}")
                print()
            else:
                print("No se encontraron tokens.\n")
        else:
            print("\nOpción inválida. Por favor, intente de nuevo.\n")

if __name__ == "__main__":
    main()
