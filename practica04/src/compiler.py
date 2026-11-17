"""Pipeline de IMP++: del archivo fuente a un ejecutable producido por GCC."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
import sys

from lark.exceptions import GrammarError, UnexpectedCharacters, UnexpectedToken

if __package__:
    from . import generador, lexer, parser, verificador_tipos
    from .asa import ASA
    from .generador import ErrorGeneracion, ResultadoGeneracion
    from .verificador_tipos import ResultadoVerificacion
else:
    import generador
    import lexer
    import parser
    import verificador_tipos
    from asa import ASA
    from generador import ErrorGeneracion, ResultadoGeneracion
    from verificador_tipos import ResultadoVerificacion


class ErrorCompiladorC(Exception):
    """Indica que GCC no está disponible o rechazó el C generado."""


@dataclass
class ResultadoCompilacion:
    """Resultados de las fases y, cuando procede, archivos producidos."""

    asa: ASA
    semantica: ResultadoVerificacion
    generacion: ResultadoGeneracion | None
    archivo_c: Path | None = None
    ejecutable: Path | None = None


def compilar(fuente: str) -> ResultadoCompilacion:
    """Ejecuta las fases propias del compilador de IMP++."""

    tokens, _tabla_lexica = lexer.analiza(fuente)
    asa = parser.analiza(tokens)
    semantica = verificador_tipos.verifica(asa)

    if not semantica.es_valido:
        return ResultadoCompilacion(asa, semantica, None)

    # Aquí va tu código:
    # llama al generador con el ASA validado y la tabla de tipos.
    raise NotImplementedError("Completa la generación dentro de compilar")


def invocar_gcc(archivo_c: Path, salida: Path) -> None:
    """Compila una unidad C con GCC y exige que produzca la salida."""

    if shutil.which("gcc") is None:
        raise ErrorCompiladorC(
            "No se encontró GCC. Instálenlo y comprueben el comando "
            "'gcc --version'."
        )

    if salida.suffix != ".out":
        raise ErrorCompiladorC("el ejecutable debe tener extensión .out")

    if salida.exists():
        salida.unlink()

    proceso = subprocess.run(
        [
            "gcc",
            "-std=c11",
            "-Wall",
            "-Wextra",
            "-pedantic",
            str(archivo_c),
            "-o",
            str(salida),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    if proceso.returncode != 0:
        diagnostico = proceso.stderr.strip() or "GCC rechazó el archivo C"
        raise ErrorCompiladorC(diagnostico)

    if not salida.is_file():
        raise ErrorCompiladorC("GCC terminó sin producir el ejecutable .out")


def compilar_archivo(entrada: Path, salida: Path) -> ResultadoCompilacion:
    """Compila un archivo IMP++ y conserva su C intermedio."""

    fuente = entrada.read_text(encoding="utf-8")
    resultado = compilar(fuente)

    if not resultado.semantica.es_valido:
        return resultado

    assert resultado.generacion is not None

    # Aquí va tu código:
    # 1. usa salida.with_suffix(".c") para obtener la ruta del C;
    # 2. escribe resultado.generacion.codigo;
    # 3. llama a invocar_gcc;
    # 4. registra las dos rutas en resultado y devuélvelo.
    raise NotImplementedError("Completa la escritura del C y la llamada a GCC")


def main() -> int:
    argumentos = argparse.ArgumentParser(
        description="Compilador de IMP++ con generación de C y llamada a GCC"
    )
    argumentos.add_argument("archivo", type=Path, help="programa fuente .imp")
    argumentos.add_argument(
        "-o",
        "--salida",
        type=Path,
        help="ejecutable .out; por omisión usa el nombre del archivo fuente",
    )
    opciones = argumentos.parse_args()
    salida = opciones.salida or opciones.archivo.with_suffix(".out")

    if salida.suffix != ".out":
        print("Error de salida: el ejecutable debe tener extensión .out", file=sys.stderr)
        return 2

    try:
        resultado = compilar_archivo(opciones.archivo, salida)

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

    except ErrorCompiladorC as error:
        print(f"Error de GCC: {error}", file=sys.stderr)
        return 3

    except (OSError, GrammarError, ErrorGeneracion) as error:
        print(f"Error al preparar el compilador: {error}", file=sys.stderr)
        return 2

    except NotImplementedError as error:
        print(f"Implementación pendiente: {error}", file=sys.stderr)
        return 2

    if not resultado.semantica.es_valido:
        for diagnostico in resultado.semantica.errores:
            print(f"Error semántico: {diagnostico.mensaje}", file=sys.stderr)
        return 1

    assert resultado.archivo_c is not None
    assert resultado.ejecutable is not None
    print(f"C generado: {resultado.archivo_c}")
    print(f"Ejecutable generado por GCC: {resultado.ejecutable}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
