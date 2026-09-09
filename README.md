# Grupo 4 
# Proyecto: Analizador SQL

La idea sería crear un programa con una interfaz o menú donde el usuario pueda seleccionar el tipo de sentencia SQL que desea analizar:

## ● DDL

* ○ CREATE
* ○ ALTER
* ○ DROP
* ○ TRUNCATE

## ● DML

* ○ SELECT
* ○ INSERT
* ○ UPDATE
* ○ DELETE

## ● Programación SQL

* ○ Procedimientos almacenados (`CREATE PROCEDURE`)
* ○ Funciones
* ○ Triggers

El sistema recibiría una consulta y realizaría:

1. **Análisis léxico** → identificar tokens y palabras reservadas.
2. **Análisis sintáctico** → validar si la estructura de la consulta es correcta.
3. **Análisis semántico** → detectar errores lógicos o reglas inválidas dentro del lenguaje definido.

## Componentes del Proyecto
- [Diseño del lenguaje y Analizador Léxico (Emilio)](./Emilio)
- [Analizador Sintáctico DML (Erick)](./Erick)
- [Analizador Sintáctico para DDL (Emilio)](./Emilio)
- [Procedimientos, Funciones y Triggers (Cristopher)](./Cristopher)
- [Analizador Semántico (Jonathan)](./Jonathan)
- [Interfaz, Menú e Integración (William)](./William)
