# Analizador Sintáctico DDL

## Archivo: `parser_ddl.py`

Este archivo se encarga de analizar y validar sentencias SQL correspondientes al lenguaje **DDL (Data Definition Language)**.

El analizador verifica que las sentencias tengan una estructura sintáctica válida de acuerdo con las reglas definidas para el proyecto.

## Sentencias soportadas

El archivo permite validar las siguientes sentencias:

- `CREATE TABLE`
- `ALTER TABLE`
- `DROP TABLE`
- `TRUNCATE TABLE`

## Tipos de datos permitidos

Dentro de las sentencias `CREATE TABLE` y `ALTER TABLE`, se permiten los siguientes tipos de datos:

- `INT`
- `VARCHAR`
- `DECIMAL`
- `DATE`
- `BOOLEAN`

Los tipos `VARCHAR` y `DECIMAL` pueden recibir parámetros.

Ejemplos:

```sql
VARCHAR(100)
DECIMAL(10,2)
