"""Lee un programa de IMP++ y coordina el lexer y el parser."""

import argparse
from dataclasses import fields
import json
from pathlib import Path
import sys
from lark.exceptions import GrammarError, UnexpectedCharacters, UnexpectedToken
if __package__:
    from . import lexer, parser
    from .asa import ASA
else:
    import lexer
    import parser
    from asa import ASA


def a_diccionario(nodo: ASA) -> dict:
    """Conserva el tipo de cada nodo al preparar el ASA para mostrarlo."""

    # 1. Guardar el nombre de la clase del nodo.
    resultado = {"tipo": type(nodo).__name__}

    # 2. Recorrer sus atributos y convertir los que también son nodos.
    for campo in fields(nodo):
        valor = getattr(nodo, campo.name)

        if isinstance(valor, ASA):
            valor = a_diccionario(valor)

        elif isinstance(valor, list):
            valor = [a_diccionario(elemento) for elemento in valor]

        resultado[campo.name] = valor

    # 3. Devolver el diccionario de este nodo.
    return resultado


def main() -> int:

    # 1. Crear el analizador de argumentos de línea de comandos.
    argumentos = argparse.ArgumentParser(
        description="Compilador didáctico de IMP++"
    )

    # 2. Indicar que el programa debe recibir la ruta
    #    de un archivo fuente .imp.
    argumentos.add_argument(
        "archivo",
        type=Path,
        help="programa fuente .imp"
    )

    # 3. Leer los argumentos proporcionados por la persona usuaria.
    opciones = argumentos.parse_args()

    try:

        # 4. Leer el contenido del programa fuente.
        fuente = opciones.archivo.read_text(
            encoding="utf-8"
        )

        # 5. Ejecutar el análisis léxico.
        #    Se obtiene la lista de tokens y la tabla de símbolos.
        tokens, tabla = lexer.analiza(fuente)

        # 6. Ejecutar el análisis sintáctico
        #    y obtener el árbol de sintaxis abstracta desendulzado.
        asa = parser.analiza(tokens)

    # 7. Detectar y reportar errores léxicos.
    except UnexpectedCharacters as error:
        print(
            f"Error léxico en línea {error.line}, "
            f"columna {error.column}: {error.char!r}",
            file=sys.stderr
        )

        return 1

    # 8. Detectar y reportar errores sintácticos.
    except UnexpectedToken as error:

        # 8.1. Verificar si el programa terminó
        #      cuando el parser esperaba más tokens.
        if error.token.type == "$END":
            print(
                "Error sintáctico al final del programa.",
                file=sys.stderr
            )

        # 8.2. Reportar el token inesperado.
        else:
            print(
                f"Error sintáctico en línea {error.line}, "
                f"columna {error.column}: "
                f"{str(error.token)!r}",
                file=sys.stderr
            )

        return 1

    # 9. Detectar errores relacionados con archivos
    #    o con la gramática de Lark.
    except (OSError, GrammarError) as error:
        print(
            f"Error al preparar el compilador: {error}",
            file=sys.stderr
        )

        return 2

    # 10. Informar si todavía falta completar una parte de la práctica.
    except NotImplementedError as error:
        print(f"Implementación pendiente: {error}", file=sys.stderr)
        return 2

    # 11. Convertir el ASA en un diccionario.
    diccionario_asa = a_diccionario(asa)

    # 12. Convertir el diccionario a JSON.
    texto_asa = json.dumps(
        diccionario_asa,
        ensure_ascii=False,
        indent=2
    )

    # 13. Mostrar el ASA desendulzado.
    print(texto_asa)

    # 14. Terminar correctamente el programa.
    return 0


# 15. Ejecutar main únicamente cuando este archivo
#     se ejecuta directamente.
if __name__ == "__main__":

    # 16. Usar el valor devuelto por main como
    #     código de salida del programa.
    codigo_salida = main()

    raise SystemExit(codigo_salida)
