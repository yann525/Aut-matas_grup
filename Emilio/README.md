# Analizador Léxico de SQL

## Descripción

En este proyecto desarrollé un **analizador léxico básico para consultas SQL utilizando Python y expresiones regulares (`re`)**.

El programa recibe una consulta SQL mediante la consola, identifica los diferentes elementos que la componen y clasifica cada uno de ellos como un token.

## ¿Qué realicé?

* Implementé la lectura de una consulta SQL desde consola.
* Definí un conjunto de **palabras reservadas de SQL**.
* Utilicé **expresiones regulares** para reconocer los diferentes tokens.
* Implementé la identificación de:

  * Palabras reservadas.
  * Cadenas de texto.
  * Números enteros.
  * Números decimales.
  * Operadores relacionales.
  * Operadores aritméticos.
  * Paréntesis.
  * Comas.
  * Punto y coma.
  * Puntos.
  * Identificadores.
* Clasifiqué cada token encontrado y mostré su tipo en consola.

## Palabras reservadas

El analizador contempla palabras reservadas relacionadas con:

* **DML:** `SELECT`, `FROM`, `WHERE`, `INSERT`, `INTO`, `VALUES`, `UPDATE`, `SET`, `DELETE`.
* **DDL:** `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `TABLE`, `ADD`, `COLUMN`.
* **Procedimientos y funciones:** `PROCEDURE`, `FUNCTION`, `RETURNS`, `RETURN`, `BEGIN`, `END`.
* **Triggers:** `TRIGGER`, `BEFORE`, `AFTER`, `ON`, `FOR`, `EACH`, `ROW`.
* **Tipos de datos:** `INT`, `VARCHAR`, `DECIMAL`, `FLOAT`, `DATE`, `BOOLEAN`, `CHAR`, `TEXT`.
* **Restricciones:** `PRIMARY`, `KEY`, `FOREIGN`, `REFERENCES`, `NOT`, `NULL`, `UNIQUE`, `DEFAULT`.
* **Operadores lógicos:** `AND`, `OR`.
* **Otras palabras:** `AS`, `JOIN`, `INNER`, `LEFT`, `RIGHT`, `ORDER`, `BY`, `GROUP`, `HAVING`, `ASC`, `DESC`.

## Tokens reconocidos

| Token                           | Clasificación       |
| ------------------------------- | ------------------- |
| `SELECT`                        | Palabra reservada   |
| `'texto'`                       | Cadena              |
| `123`                           | Número entero       |
| `123.45`                        | Decimal             |
| `=` `>` `<` `>=` `<=` `<>` `!=` | Operador relacional |
| `+` `-` `*` `/`                 | Operador aritmético |
| `(` `)`                         | Paréntesis          |
| `,`                             | Coma                |
| `;`                             | Fin de sentencia    |
| `.`                             | Punto               |
| `nombre`                        | Identificador       |

## Funcionamiento

El programa sigue este proceso:

1. Solicita al usuario una consulta SQL.
2. Aplica una expresión regular para separar la consulta en tokens.
3. Recorre cada token encontrado.
4. Compara el token con la lista de palabras reservadas.
5. Aplica diferentes validaciones mediante `re.fullmatch()`.
6. Determina el tipo de token.
7. Muestra el resultado en consola.

## Ejemplo

### Entrada

```sql
SELECT nombre, edad FROM usuarios WHERE edad >= 18;
```

### Salida esperada

```text
--- ANALIZADOR LEXICO ---

SELECT -> PALABRA RESERVADA
nombre -> IDENTIFICADOR
, -> COMA
edad -> IDENTIFICADOR
FROM -> PALABRA RESERVADA
usuarios -> IDENTIFICADOR
WHERE -> PALABRA RESERVADA
edad -> IDENTIFICADOR
>= -> OPERADOR RELACIONAL
18 -> NUMERO
; -> FIN DE SENTENCIA
```

## Tecnologías utilizadas

* **Python 3**
* **Módulo `re` (expresiones regulares)**
* **Git / GitHub**

## Objetivo

El objetivo del proyecto es aplicar los conceptos de **análisis léxico** estudiados en la asignatura, identificando y clasificando los componentes de una consulta SQL antes de realizar un análisis sintáctico.

## Autor

Proyecto académico de **Ingeniería en Sistemas**.
