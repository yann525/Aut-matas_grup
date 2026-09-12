import re



patron_procedure = r'CREATE\s+PROCEDURE\s+[A-Za-z_][A-Za-z0-9_]*\s+BEGIN\s+.*?\s*END;'
patron_trigger = r'CREATE\s+TRIGGER\s+[A-Za-z_][A-Za-z0-9_]*\s+(?:BEFORE|AFTER)\s+(?:INSERT|UPDATE|DELETE)\s+ON\s+[A-Za-z_][A-Za-z0-9_]*\s+BEGIN\s+.*?\s*END;'
patron_function = r'CREATE\s+FUNCTION\s+[A-Za-z_][A-Za-z0-9_]*\s*\(\)\s+RETURNS\s+[A-Za-z_][A-Za-z0-9_]*\s+BEGIN\s+.*?\s*END;'

def validar_programacion(texto):
    texto_limpio = texto.strip()

# re.DOTALL permite evaluar bloques de código multilínea (BEGIN ... END;)
    if re.fullmatch(patron_procedure, texto_limpio, re.I | re.DOTALL):
        return True, "Procedimiento Almacenado"
    elif re.fullmatch(patron_trigger, texto_limpio, re.I | re.DOTALL):
        return True, "Trigger"
    elif re.fullmatch(patron_function, texto_limpio, re.I | re.DOTALL):
        return True, "Función"
    else:
        return False, "Error sintáctico"


