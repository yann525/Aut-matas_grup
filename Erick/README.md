# Analizador Sintáctico DML

Este directorio contiene el script `parser_dml.py`, el cual se encarga de validar la estructura sintáctica de comandos SQL correspondientes al Lenguaje de Manipulación de Datos (DML).

## Comandos Soportados

El analizador verifica la correcta escritura de las siguientes instrucciones:

- `SELECT`
- `INSERT`
- `UPDATE`
- `DELETE`

## Ejemplos Válidos

Las siguientes consultas son aceptadas correctamente por el analizador:

- `SELECT * FROM usuarios;`
- `SELECT nombre, edad FROM usuarios WHERE edad > 18;`
- `INSERT INTO usuarios (nombre, edad) VALUES ('Carlos', 25);`
- `UPDATE usuarios SET nombre = 'Carlos' WHERE id = 1;`
- `DELETE FROM usuarios WHERE id = 1;`

## Ejemplos de Error

Las siguientes consultas presentan errores de sintaxis y son detectadas como inválidas:

- `SELECT FROM usuarios;` (Faltan las columnas o el asterisco).
- `UPDATE usuarios nombre = 'Carlos';` (Falta la palabra reservada `SET`).
- `DELETE usuarios WHERE id = 1;` (Falta la palabra reservada `FROM`).

## Ejecución

Para ejecutar el analizador y ver los resultados de prueba, se debe correr el siguiente comando utilizando Python 3:

```bash
python parser_dml.py
```
