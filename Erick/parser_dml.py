import re

class AnalizadorDML:
    """
    Clase encargada de validar la estructura sintáctica de sentencias DML básicas de SQL:
    SELECT, INSERT, UPDATE, DELETE.
    """
    def __init__(self):
        # Componentes básicos de las expresiones regulares
        identificador = r'[a-zA-Z_][a-zA-Z0-9_]*'
        condicion = r'[^;]+'
        
        # Patrón para SELECT:
        # SELECT * o columnas FROM tabla [WHERE condicion];
        self.patron_select = re.compile(
            rf"^\s*SELECT\s+(?:\*|{identificador}(?:\s*,\s*{identificador})*)\s+FROM\s+{identificador}(?:\s+WHERE\s+{condicion})?\s*;\s*$",
            re.IGNORECASE
        )
        
        # Patrón para INSERT:
        # INSERT INTO tabla (columna1, ...) VALUES (valor1, ...);
        self.patron_insert = re.compile(
            rf"^\s*INSERT\s+INTO\s+{identificador}\s*\(\s*{identificador}(?:\s*,\s*{identificador})*\s*\)\s*VALUES\s*\(\s*[^)]+\s*\)\s*;\s*$",
            re.IGNORECASE
        )
        
        # Patrón para UPDATE:
        # UPDATE tabla SET col = valor [, col2 = valor2] [WHERE condicion];
        asignacion = rf"{identificador}\s*=\s*(?:'[^']*'|\"[^\"]*\"|[^,;\s]+(?:(?!\s+WHERE\s+)[^,;])*)"
        self.patron_update = re.compile(
            rf"^\s*UPDATE\s+{identificador}\s+SET\s+{asignacion}(?:\s*,\s*{asignacion})*(?:\s+WHERE\s+{condicion})?\s*;\s*$",
            re.IGNORECASE
        )
        
        # Patrón para DELETE:
        # DELETE FROM tabla [WHERE condicion];
        self.patron_delete = re.compile(
            rf"^\s*DELETE\s+FROM\s+{identificador}(?:\s+WHERE\s+{condicion})?\s*;\s*$",
            re.IGNORECASE
        )

    def validar(self, consulta: str) -> bool:
        """
        Valida si la consulta coincide con alguno de los patrones DML soportados.
        """
        consulta_limpia = consulta.strip()
        
        if self.patron_select.match(consulta_limpia):
            return True
        if self.patron_insert.match(consulta_limpia):
            return True
        if self.patron_update.match(consulta_limpia):
            return True
        if self.patron_delete.match(consulta_limpia):
            return True
            
        return False

def main():
    analizador = AnalizadorDML()
    
    # Pruebas requeridas
    consultas = [
        "SELECT * FROM usuarios;",
        "SELECT nombre, edad FROM usuarios WHERE edad > 18;",
        "INSERT INTO usuarios (nombre, edad) VALUES ('Carlos', 25);",
        "UPDATE usuarios SET nombre = 'Carlos' WHERE id = 1;",
        "DELETE FROM usuarios WHERE id = 1;",
        "SELECT FROM usuarios;",
        "UPDATE usuarios nombre = 'Carlos';",
        "DELETE usuarios WHERE id = 1;"
    ]
    
    print("Iniciando validación de consultas DML...")
    print("-" * 50)
    for consulta in consultas:
        resultado = analizador.validar(consulta)
        estado = "VÁLIDA" if resultado else "ERROR "
        print(f"[{estado}] {consulta}")

if __name__ == '__main__':
    main()
