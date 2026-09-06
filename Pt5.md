# Analizador Semantico de SQL

## Descripcion

En este proyecto desarrolle un **analizador semantico para consultas SQL utilizando Python y expresiones regulares (`re`)**.

El programa recibe una consulta SQL (ya validada lexica y sintacticamente por los modulos de mis companeros) y verifica que tenga sentido dentro de un catalogo de tablas y columnas definido en memoria, simulando una base de datos simple.

## Que realice?

* Defini un **catalogo de tablas y columnas** (un diccionario en Python) que simula una base de datos.
* Implemente una funcion principal, `analizar_semantico(consulta)`, que identifica el tipo de sentencia y aplica las validaciones correspondientes.
* Utilice **expresiones regulares** para extraer de cada consulta la tabla y las columnas involucradas.
* Implemente la validacion semantica de:

  * `SELECT`
  * `INSERT`
  * `UPDATE`
  * `DELETE`
  * `DROP TABLE`
  * `TRUNCATE TABLE`
  * `CREATE TABLE`
  * `ALTER TABLE ... ADD`
* Hice que el catalogo se actualice dinamicamente: `CREATE TABLE` agrega una tabla nueva, `ALTER TABLE ADD` agrega una columna, y `DROP TABLE` elimina la tabla del catalogo.
* Devolvi los errores con el mismo formato que pedia la consigna del proyecto (`Error semantico:\n...`).

## Catalogo de tablas

El analizador parte de un catalogo inicial cargado en memoria:

```python
catalogo = {
    "usuarios": ["id", "nombre", "edad"],
    "productos": ["id", "nombre", "precio"],
    "ventas": ["id", "usuario_id", "producto_id", "cantidad", "fecha"],
}
```

Este catalogo puede crecer o reducirse conforme se ejecutan sentencias `CREATE`, `ALTER` y `DROP`, igual que pasaria con una base de datos real.

## Reglas semanticas validadas

* Tabla inexistente: si la sentencia usa una tabla que no esta en el catalogo.
* Columna inexistente: si se pide una columna que no pertenece a la tabla.
* DROP/TRUNCATE de tabla inexistente: no se puede eliminar o vaciar algo que no existe.
* CREATE de tabla ya existente: no se puede crear una tabla con un nombre repetido.
* ALTER agregando una columna repetida: no se puede agregar una columna que ya existe en la tabla.

## Funcionamiento

El programa sigue este proceso:

1. Recibe una consulta SQL como texto (ya limpia de espacios y del `;` final).
2. Identifica la primera palabra de la sentencia (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `DROP`, `TRUNCATE`, `CREATE` o `ALTER`).
3. Segun el tipo, extrae con una expresion regular la tabla y, si aplica, las columnas involucradas.
4. Verifica que la tabla exista en el catalogo.
5. Si la tabla existe, verifica que las columnas usadas tambien existan en ella.
6. Si es `CREATE`, `ALTER` o `DROP`, actualiza el catalogo en memoria.
7. Devuelve una tupla `(es_valida, errores)` con el resultado del analisis.

## Ejemplo

### Entrada

```sql
SELECT apellido FROM usuarios;
```

### Salida esperada

```text
Error semantico:
La columna "apellido" no existe en la tabla usuarios.
```

### Otro ejemplo

### Entrada

```sql
DROP TABLE empleados;
```

### Salida esperada

```text
Error semantico:
No se puede eliminar la tabla porque no existe.
```

### Un caso correcto

### Entrada

```sql
SELECT nombre, edad FROM usuarios WHERE edad > 18;
```

### Salida esperada

```text
CONSULTA SEMANTICAMENTE CORRECTA
```

## Tecnologias utilizadas

* **Python 3**
* **Modulo `re` (expresiones regulares)**
* **Git / GitHub**

## Objetivo

El objetivo de esta parte del proyecto es aplicar los conceptos de **analisis semantico** estudiados en la asignatura, verificando que una consulta SQL tenga sentido logico (tablas y columnas existentes) despues de haber pasado el analisis lexico y sintactico.

## Entregable

`semantic.py`, con la funcion `analizar_semantico(consulta)` lista para ser importada por `main.py`.

## Autor

Proyecto academico de **Ingenieria en Sistemas** - Jonathan.
