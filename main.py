
import pygame
import pygame.scrap
import sys
import os


pygame.init()

ANCHO, ALTO = 1100, 650
P = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("ANALIZADOR SQL")

pygame.scrap.init()


F = pygame.font.SysFont("Consolas", 18)
S = pygame.font.SysFont("Arial", 15)
B = pygame.font.SysFont("Arial", 16, bold=True)

AZUL = (35, 80, 160)
NEGRO = (25, 30, 40)
GRIS = (120, 120, 120)
BLANCO = (255, 255, 255)
VERDE = (35, 140, 80)
FONDO = (245, 247, 250)
BORDE = (210, 215, 225)
SELECCION = (235, 242, 255)

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from Emilio.analizador_lexico import analizar_lexico
from Emilio.analizador_ddl import analizar_ddl
from Erick.parser_dml import AnalizadorDML
from Cristopher.Triggers import validar_programacion
from Jonathan.semantic import analizar_semantico

parser_dml = AnalizadorDML()

lineas = [""]
fila = 0
col = 0
desplazamiento_editor = 0
desplazamiento_salida = 0

salida = [
    "Bienvenido al ANALIZADOR SQL",
    "Escriba una consulta SQL y presione EJECUTAR.",
    "Tambien puede utilizar F5."
]

activo = True

btn_ej = pygame.Rect(15, 10, 135, 34)
btn_nuevo = pygame.Rect(160, 10, 110, 34)
btn_lim = pygame.Rect(280, 10, 165, 34)
btn_tokens = pygame.Rect(455, 10, 135, 34)

editor = pygame.Rect(15, 65, 690, 570)
panel = pygame.Rect(720, 65, 365, 570)


def obtener_consulta():
    return "\n".join(lineas)


def realizar_analisis(consulta, solo_tokens=False):
    resultados = ["=== ANALISIS SQL ==="]

    if not consulta.strip():
        return ["Escriba una consulta SQL antes de ejecutar."]

    try:
        tokens = analizar_lexico(consulta)

        resultados += ["", "ANALISIS LEXICO:"]

        if not tokens:
            resultados.append("ERROR: No se encontraron tokens.")
            return resultados

        tiene_error = any(
            tipo == "ERROR LEXICO"
            for token, tipo in tokens
        )

        if tiene_error:
            resultados.append("ERROR LEXICO DETECTADO")
        else:
            resultados.append("Sin errores lexicos.")

        resultados += ["", "TOKENS GENERADOS:"]

        for token, tipo in tokens:
            resultados.append(f"{token} -> {tipo}")

        if solo_tokens:
            return resultados

        if tiene_error:
            resultados += [
                "",
                "RESULTADO FINAL:",
                "CONSULTA CON ERRORES"
            ]
            return resultados

        palabras = consulta.strip().split()
        primera = palabras[0].upper() if palabras else ""

        resultados += ["", "ANALISIS SINTACTICO:"]

        sintaxis_valida = False

        if primera in ("SELECT", "INSERT", "UPDATE", "DELETE"):
            sintaxis_valida = parser_dml.validar(consulta)

        elif primera in ("CREATE", "ALTER", "DROP", "TRUNCATE"):
            valido_prog, mensaje_prog = validar_programacion(consulta)

            if valido_prog:
                sintaxis_valida = True
            else:
                valido_ddl, mensaje_ddl = analizar_ddl(consulta)
                sintaxis_valida = valido_ddl

                if not sintaxis_valida:
                    if mensaje_ddl:
                        resultados.append(str(mensaje_ddl))
                    elif mensaje_prog:
                        resultados.append(str(mensaje_prog))

        else:
            resultados.append(
                "Tipo de sentencia no reconocido para el analisis."
            )

        if sintaxis_valida:
            resultados.append("Consulta sintacticamente valida.")
        else:
            resultados.append("ERROR SINTACTICO.")

        resultados += ["", "ANALISIS SEMANTICO:"]

        semantico_valido, errores = analizar_semantico(consulta)

        if semantico_valido:
            resultados.append("Tabla existente.")
            resultados.append("Columnas validas.")
        elif errores:
            for error in errores:
                resultados.append("ERROR: " + str(error))
        else:
            resultados.append("Error semantico detectado.")

        resultados += ["", "RESULTADO FINAL:"]

        if sintaxis_valida and semantico_valido:
            resultados.append("CONSULTA CORRECTA")
        else:
            resultados.append("CONSULTA CON ERRORES")

        return resultados

    except Exception as error:
        resultados += [
            "",
            "ERROR DURANTE EL ANALISIS:",
            str(error)
        ]
        return resultados


def dibujar_boton(rect, texto, color):
    pygame.draw.rect(P, color, rect, border_radius=6)

    imagen = B.render(texto, True, BLANCO)

    P.blit(
        imagen,
        (
            rect.centerx - imagen.get_width() // 2,
            rect.centery - imagen.get_height() // 2
        )
    )


def dibujar_texto(texto, fuente, color, x, y):
    imagen = fuente.render(str(texto), True, color)
    P.blit(imagen, (x, y))


def ajustar_editor():
    global desplazamiento_editor

    visibles = 21

    if fila < desplazamiento_editor:
        desplazamiento_editor = fila

    if fila >= desplazamiento_editor + visibles:
        desplazamiento_editor = fila - visibles + 1

    desplazamiento_editor = max(0, desplazamiento_editor)


def insertar_texto(texto):
    global col

    actual = lineas[fila]

    lineas[fila] = (
        actual[:col] + texto + actual[col:]
    )

    col += len(texto)


def nueva_linea():
    global fila, col

    actual = lineas[fila]

    izquierda = actual[:col]
    derecha = actual[col:]

    lineas[fila] = izquierda
    lineas.insert(fila + 1, derecha)

    fila += 1
    col = 0

    ajustar_editor()


def borrar_caracter():
    global fila, col

    if col > 0:
        actual = lineas[fila]

        lineas[fila] = (
            actual[:col - 1] + actual[col:]
        )

        col -= 1

    elif fila > 0:
        col = len(lineas[fila - 1])

        lineas[fila - 1] += lineas[fila]

        del lineas[fila]

        fila -= 1

    ajustar_editor()


def limpiar_editor():
    global lineas, fila, col, desplazamiento_editor

    lineas = [""]
    fila = 0
    col = 0
    desplazamiento_editor = 0


def copiar_linea_actual():
    try:
        texto = lineas[fila]
        pygame.scrap.put(
            pygame.SCRAP_TEXT,
            texto.encode("utf-8") + b"\x00"
        )
    except pygame.error:
        pass


def pegar_portapapeles():
    global fila, col

    try:
        texto = pygame.scrap.get(pygame.SCRAP_TEXT)

        if not texto:
            return

        texto = texto.rstrip(b"\x00").decode(
            "utf-8",
            errors="ignore"
        )

        texto = texto.replace("\r\n", "\n").replace("\r", "\n")

        partes = texto.split("\n")

        insertar_texto(partes[0])

        for parte in partes[1:]:
            nueva_linea()
            insertar_texto(parte)

        ajustar_editor()

    except (pygame.error, UnicodeError):
        pass


def dibujar_interfaz():
    P.fill(FONDO)

    dibujar_boton(btn_ej, "EJECUTAR", VERDE)
    dibujar_boton(btn_nuevo, "NUEVO", AZUL)
    dibujar_boton(btn_lim, "LIMPIAR SALIDA", GRIS)
    dibujar_boton(btn_tokens, "VER TOKENS", (110, 75, 155))

    pygame.draw.rect(P, BLANCO, editor, border_radius=5)
    pygame.draw.rect(P, BORDE, editor, 1, border_radius=5)
    pygame.draw.rect(P, NEGRO, panel, border_radius=5)

    dibujar_texto("EDITOR SQL", B, AZUL, 25, 72)
    dibujar_texto("RESULTADO", B, BLANCO, 735, 75)

    visibles = 21
    alto_linea = 23
    inicio_y = 103

    for indice in range(
        desplazamiento_editor,
        min(len(lineas), desplazamiento_editor + visibles)
    ):
        y = inicio_y + (
            indice - desplazamiento_editor
        ) * alto_linea

        if indice == fila:
            pygame.draw.rect(
                P,
                SELECCION,
                (20, y - 2, 675, alto_linea)
            )

        dibujar_texto(
            str(indice + 1),
            S,
            GRIS,
            25,
            y
        )

        dibujar_texto(
            lineas[indice][:75],
            F,
            NEGRO,
            60,
            y
        )

        if indice == fila and activo:
            cursor_x = 60 + F.size(
                lineas[fila][:col]
            )[0]

            pygame.draw.line(
                P,
                AZUL,
                (cursor_x, y),
                (cursor_x, y + 20),
                2
            )

    y = 105
    limite_y = 615

    for texto in salida[desplazamiento_salida:]:
        if y >= limite_y:
            break

        if "ERROR" in texto or "CON ERRORES" in texto:
            color = (255, 130, 130)
        elif "CORRECTA" in texto or "valida" in texto.lower():
            color = (100, 220, 150)
        else:
            color = (230, 230, 230)

        partes = [
            texto[i:i + 39]
            for i in range(0, max(len(texto), 1), 39)
        ]

        for parte in partes:
            if y >= limite_y:
                break

            dibujar_texto(
                parte,
                S,
                color,
                735,
                y
            )

            y += 18

    pygame.display.flip()


reloj = pygame.time.Clock()

while True:
    ejecutar_pendiente = False
    modo_tokens = False

    for e in pygame.event.get():

        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if e.type == pygame.MOUSEBUTTONDOWN:

            if e.button == 1:

                if btn_ej.collidepoint(e.pos):
                    ejecutar_pendiente = True

                elif btn_nuevo.collidepoint(e.pos):
                    limpiar_editor()
                    salida = [
                        "Editor limpio.",
                        "Escriba una nueva consulta."
                    ]
                    desplazamiento_salida = 0

                elif btn_lim.collidepoint(e.pos):
                    salida = []
                    desplazamiento_salida = 0

                elif btn_tokens.collidepoint(e.pos):
                    modo_tokens = True
                    ejecutar_pendiente = True

                elif editor.collidepoint(e.pos):
                    activo = True

            elif e.button == 4:

                if panel.collidepoint(e.pos):
                    desplazamiento_salida = max(
                        0,
                        desplazamiento_salida - 3
                    )

                elif editor.collidepoint(e.pos):
                    desplazamiento_editor = max(
                        0,
                        desplazamiento_editor - 3
                    )

            elif e.button == 5:

                if panel.collidepoint(e.pos):
                    desplazamiento_salida = min(
                        max(0, len(salida) - 1),
                        desplazamiento_salida + 3
                    )

                elif editor.collidepoint(e.pos):
                    desplazamiento_editor = min(
                        max(0, len(lineas) - 1),
                        desplazamiento_editor + 3
                    )

        if e.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()

            if e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            elif e.key == pygame.K_F5:
                modo_tokens = False
                ejecutar_pendiente = True

            elif e.key == pygame.K_F6:
                modo_tokens = True
                ejecutar_pendiente = True

            elif mods & pygame.KMOD_CTRL and e.key == pygame.K_c:
                copiar_linea_actual()

            elif mods & pygame.KMOD_CTRL and e.key == pygame.K_v:
                pegar_portapapeles()

            elif e.key == pygame.K_UP:
                fila = max(0, fila - 1)
                col = min(col, len(lineas[fila]))
                ajustar_editor()

            elif e.key == pygame.K_DOWN:
                fila = min(len(lineas) - 1, fila + 1)
                col = min(col, len(lineas[fila]))
                ajustar_editor()

            elif e.key == pygame.K_LEFT:

                if col > 0:
                    col -= 1

                elif fila > 0:
                    fila -= 1
                    col = len(lineas[fila])

                ajustar_editor()

            elif e.key == pygame.K_RIGHT:

                if col < len(lineas[fila]):
                    col += 1

                elif fila < len(lineas) - 1:
                    fila += 1
                    col = 0

                ajustar_editor()

            elif e.key == pygame.K_HOME:
                col = 0

            elif e.key == pygame.K_END:
                col = len(lineas[fila])

            elif e.key == pygame.K_RETURN:
                nueva_linea()

            elif e.key == pygame.K_BACKSPACE:
                borrar_caracter()

            elif e.key == pygame.K_TAB:
                insertar_texto("    ")

            elif e.key == pygame.K_PAGEUP:
                desplazamiento_salida = max(
                    0,
                    desplazamiento_salida - 10
                )

            elif e.key == pygame.K_PAGEDOWN:
                desplazamiento_salida = min(
                    max(0, len(salida) - 1),
                    desplazamiento_salida + 10
                )

            elif e.unicode and e.unicode.isprintable():
                insertar_texto(e.unicode)

    if ejecutar_pendiente:
        salida = realizar_analisis(
            obtener_consulta(),
            modo_tokens
        )

        desplazamiento_salida = max(
            0,
            len(salida) - 24
        )

    dibujar_interfaz()
    reloj.tick(30)
