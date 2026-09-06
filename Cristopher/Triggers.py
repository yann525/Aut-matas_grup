import re

print("Analizador de Procedimientos, Funciones y Triggers")
texto = input("Ingrese su consulta: ").strip()

patron_procedure = r'CREATE\s+PROCEDURE\s+[A-Za-z_][A-Za-z0-9_]*\s+BEGIN\s+.*?\s*END;'

patron_trigger = r'CREATE\s+TRIGGER\s+[A-Za-z_][A-Za-z0-9_]*\s+(?:BEFORE|AFTER)\s+(?:INSERT|UPDATE|DELETE)\s+ON\s+[A-Za-z_][A-Za-z0-9_]*\s+BEGIN\s+.*?\s*END;'

patron_function = r'CREATE\s+FUNCTION\s+[A-Za-z_][A-Za-z0-9_]*\s*\(\)\s+RETURNS\s+[A-Za-z_][A-Za-z0-9_]*\s+BEGIN\s+.*?\s*END;'

if re.fullmatch(patron_procedure, texto, re.I):
    print("Consulta validada: Procedimiento Almacenado")
elif re.fullmatch(patron_trigger, texto, re.I):
    print("Consulta validada: Trigger")
elif re.fullmatch(patron_function, texto, re.I):
    print("Consulta validada: Función")
else:
    print("Error sintactico")