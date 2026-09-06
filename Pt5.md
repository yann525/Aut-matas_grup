# Parte 5: Analizador Semantico

Autor: Jonathan

## Para que sirve esta parte?

Dentro del proyecto del Analizador SQL, mi trabajo fue construir la ultima capa de validacion: el **analisis semantico**. Mientras que el analisis lexico revisa que los simbolos esten bien escritos y el sintactico revisa que la estructura de la sentencia sea correcta, el semantico responde una pregunta distinta: **la consulta tiene sentido en el mundo real?**

Por ejemplo, `SELECT nombre FROM usuarios;` puede estar perfectamente escrita (lexica y sintacticamente), pero si la tabla `usuarios` no existe, o si `nombre` no es una columna de esa tabla, la consulta sigue siendo invalida. De eso se encarga mi modulo.

## Como lo resolvi

En lugar de depender de una base de datos real, simule una con un diccionario de Python al que llame `catalogo`:

```python
catalogo = {
    "usuarios": ["id", "nombre", "edad"],
    "productos": ["id", "nombre", "precio"],
    "ventas": ["id", "usuario_id", "producto_id", "cantidad", "fecha"],
}
```

Cada llave es una tabla y su valor es la lista de columnas que contiene. A partir de ahi, escribi una funcion distinta para cada tipo de sentencia (`_analizar_select`, `_analizar_insert`, `_analizar_update`, `_analizar_delete`, `_analizar_drop`, `_analizar_truncate`, `_analizar_create`, `_analizar_alter`), y una funcion publica, `analizar_semantico(consulta)`, que decide cual usar segun la primera palabra de la consulta.

Cada una de esas funciones usa `re.search` para sacar el nombre de la tabla (y las columnas, cuando aplica) directamente del texto de la consulta, sin depender de que otro modulo se la entregue ya separada. Esto la hace independiente: se puede probar sola, sin esperar a que el analizador sintactico de mis companeros este terminado.

## Algo que agregue por mi cuenta

El PDF del proyecto solo pedia detectar tablas y columnas inexistentes. Pero note que si el catalogo nunca cambia, sentencias como `CREATE TABLE` o `ALTER TABLE ADD` nunca podrian usarse de verdad. Asi que hice que el catalogo se actualice en memoria:

- `CREATE TABLE` agrega la tabla nueva (y falla si ya existe).
- `ALTER TABLE ... ADD` agrega una columna nueva a una tabla existente (y falla si la columna ya esta).
- `DROP TABLE` borra la tabla del catalogo (y falla si no existia).

Con esto, el catalogo se comporta mas como una base de datos de verdad a lo largo de una sesion, en vez de ser un diccionario fijo.

## Casos que valida

| Situacion | Que revisa? |
|---|---|
| `SELECT`, `INSERT`, `UPDATE` | Que la tabla exista y que las columnas usadas pertenezcan a ella |
| `DELETE` | Que la tabla exista |
| `DROP TABLE` / `TRUNCATE TABLE` | Que la tabla exista antes de eliminarla o vaciarla |
| `CREATE TABLE` | Que no exista ya una tabla con ese nombre |
| `ALTER TABLE ADD` | Que la tabla exista y que la columna nueva no este repetida |

## Ejemplos reales de la consola

```
>>> SELECT apellido FROM usuarios;
Error semantico:
La columna "apellido" no existe en la tabla usuarios.

>>> DROP TABLE empleados;
Error semantico:
No se puede eliminar la tabla porque no existe.

>>> SELECT nombre, edad FROM usuarios WHERE edad > 18;
CONSULTA SEMANTICAMENTE CORRECTA
```

## Como se conecta con el resto del proyecto

Todo vive en `semantic.py` y se expone a traves de una sola funcion:

```python
es_valida, errores = analizar_semantico(consulta)
```

William solo necesita importar esa funcion en `main.py` y llamarla despues de que la consulta pase por el analisis lexico y sintactico de los demas. Si `es_valida` es `False`, `errores` trae la lista de mensajes listos para mostrarse tal cual en pantalla.

Tambien deje el archivo preparado para probarse solo, sin depender del menu final: si se ejecuta directamente con `python semantic.py`, pide una consulta por consola y muestra el resultado, tal como hicimos con el analizador lexico de Emilio.
