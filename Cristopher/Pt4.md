# Analizador Sintáctico de Procedimientos, Funciones y Triggers SQL

### Descripción

En este proyecto desarrollé un analizador sintáctico para sentencias de programación avanzada en SQL (Procedimientos Almacenados, Triggers y Funciones) utilizando Python y expresiones regulares (`re`).
El programa recibe una consulta SQL desde la consola y valida si la estructura gramatical de la instrucción está escrita correctamente, aceptando bloques de código que abarcan múltiples líneas.

### ¿Qué realicé?

* Implementé la lectura de consultas SQL desde la consola.
* Diseñé expresiones regulares complejas para validar la sintaxis completa de bloques de programación SQL.
* Implementé la identificación y validación estructural de:
* **Procedimientos Almacenados:** Validación de la estructura `CREATE PROCEDURE ... BEGIN ... END;`.
* **Triggers:** Validación de la estructura `CREATE TRIGGER ... BEFORE/AFTER ... ON ... BEGIN ... END;`.
* **Funciones:** Validación de la estructura `CREATE FUNCTION ... RETURNS ... BEGIN ... END;`.


* Clasifiqué el tipo de sentencia ingresada y mostré un mensaje de validación o de error sintáctico en consola.

### Estructuras validadas

El analizador contempla la validación de las siguientes gramáticas (versión simplificada para el lenguaje del proyecto):

* **Procedimientos Almacenados:**
Requiere obligatoriamente las palabras reservadas `CREATE PROCEDURE`, seguido de un identificador válido, y encapsulando el código entre `BEGIN` y `END;`.
* **Triggers (Disparadores):**
Requiere `CREATE TRIGGER`, un identificador, el momento de ejecución (`BEFORE` o `AFTER`), el evento DML (`INSERT`, `UPDATE` o `DELETE`), la cláusula `ON` referenciando una tabla, y el bloque de código entre `BEGIN` y `END;`.
* **Funciones:**
Requiere `CREATE FUNCTION`, un identificador seguido de paréntesis `()`, la cláusula `RETURNS` indicando un tipo de dato (identificador), y el bloque de código entre `BEGIN` y `END;`.

### Funcionamiento

El programa sigue este proceso:

1. Solicita al usuario que ingrese una sentencia SQL.
2. Limpia los espacios en blanco iniciales o finales de la entrada.
3. Aplica la función `re.fullmatch()` comparando la entrada contra los tres patrones de expresiones regulares definidos (Procedimientos, Triggers y Funciones).
4. Determina qué tipo de estructura se ingresó.
5. Muestra el resultado en consola ("Consulta validada" con su tipo, o "Error sintáctico").

### Ejemplos

**Ejemplo 1: Procedimiento Almacenado**

*Entrada:*

```sql
CREATE PROCEDURE reporte_usuarios
BEGIN
    SELECT * FROM usuarios;
END;

```

*Salida esperada:*

```text
 Analizador de Procedimientos, Funciones y Triggers 
Consulta validada: Procedimiento Almacenado

```

**Ejemplo 2: Trigger con error sintáctico**

*Entrada:*

```sql
CREATE TRIGGER mi_trigger
INSERT ON usuarios
BEGIN
END;

```

*(Falta definir si es BEFORE o AFTER)*

*Salida esperada:*

```text
 Analizador de Procedimientos, Funciones y Triggers 
Error sintactico

```

### Tecnologías utilizadas

* Python 3
* Módulo `re` (Expresiones regulares)
* Git / GitHub

### Objetivo

El objetivo de mi módulo es aplicar los conceptos de análisis sintáctico (parsing) para validar sentencias de programación avanzadas dentro de SQL. Al asegurar que la estructura gramatical de los bloques `BEGIN...END` está correctamente escrita, se garantiza que el código está listo para pasar al Analizador Semántico desarrollado por el resto del equipo.