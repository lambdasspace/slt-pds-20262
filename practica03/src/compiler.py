"""Coordina las fases del compilador de IMP++ hasta la semántica."""

import argparse
from dataclasses import fields
import json
from pathlib import Path
import sys

from lark.exceptions import GrammarError, UnexpectedCharacters, UnexpectedToken

if __package__:
    from . import lexer, parser, verificador_tipos
    from .asa import ASA
else:
    import lexer
    import parser
    import verificador_tipos
    from asa import ASA


def a_diccionario(nodo: ASA) -> dict:
    """Convierte recursivamente un nodo del ASA en un diccionario."""

    resultado = {"tipo": type(nodo).__name__}
    for campo in fields(nodo):
        valor = getattr(nodo, campo.name)
        if isinstance(valor, ASA):
            valor = a_diccionario(valor)
        elif isinstance(valor, list):
            valor = [a_diccionario(elemento) for elemento in valor]
        resultado[campo.name] = valor
    return resultado


def salida_compilacion(asa: ASA, resultado) -> dict:
    """Prepara el ASA y su contexto de tipos para mostrarlos."""

    simbolos = [
        {
            "nombre": entrada.nombre,
            "tipo": entrada.tipo.value,
        }
        for entrada in resultado.tabla.entradas()
    ]
    return {"asa": a_diccionario(asa), "simbolos": simbolos}


def main() -> int:
    argumentos = argparse.ArgumentParser(
        description="Compilador didáctico de IMP++ hasta la semántica"
    )
    argumentos.add_argument("archivo", type=Path, help="programa fuente .imp")
    opciones = argumentos.parse_args()

    try:
        fuente = opciones.archivo.read_text(encoding="utf-8")
        tokens, _tabla_lexica = lexer.analiza(fuente)
        asa = parser.analiza(tokens)
        resultado = verificador_tipos.verifica(asa)

    except UnexpectedCharacters as error:
        print(
            f"Error léxico en línea {error.line}, "
            f"columna {error.column}: {error.char!r}",
            file=sys.stderr,
        )
        return 1

    except UnexpectedToken as error:
        if error.token.type == "$END":
            print("Error sintáctico al final del programa.", file=sys.stderr)
        else:
            print(
                f"Error sintáctico en línea {error.line}, "
                f"columna {error.column}: {str(error.token)!r}",
                file=sys.stderr,
            )
        return 1

    except (OSError, GrammarError) as error:
        print(f"Error al preparar el compilador: {error}", file=sys.stderr)
        return 2

    except NotImplementedError as error:
        print(f"Implementación pendiente: {error}", file=sys.stderr)
        return 2

    if not resultado.es_valido:
        for diagnostico in resultado.errores:
            print(f"Error semántico: {diagnostico.mensaje}", file=sys.stderr)
        return 1

    print(json.dumps(
        salida_compilacion(asa, resultado),
        ensure_ascii=False,
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
