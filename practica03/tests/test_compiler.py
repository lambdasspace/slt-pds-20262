"""Pruebas proporcionadas del compilador integrado. No modificar."""

import json
from pathlib import Path
import subprocess
import sys
import unittest


BASE = Path(__file__).resolve().parents[1]


class PruebasCompiler(unittest.TestCase):
    def ejecutar(self, entrada, ejemplo):
        return subprocess.run(
            [sys.executable, "-B", *entrada, f"ejemplos/{ejemplo}"],
            cwd=BASE,
            capture_output=True,
            text=True,
        )

    def test_archivo_y_modulo_verifican_programa_valido(self):
        salidas = []
        for entrada in (["src/compiler.py"], ["-m", "src.compiler"]):
            resultado = self.ejecutar(entrada, "imp_mas_mas.imp")
            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            salida = json.loads(resultado.stdout)
            self.assertEqual(salida["asa"]["tipo"], "PROGRAMA")
            self.assertEqual(
                [(e["nombre"], e["tipo"]) for e in salida["simbolos"]],
                [("contador_1", "int"), ("activo", "bool")],
            )
            salidas.append(salida)
        self.assertEqual(salidas[0], salidas[1])

    def test_reporta_errores_semanticos(self):
        resultado = self.ejecutar(["-m", "src.compiler"], "error_tipos.imp")
        self.assertEqual(resultado.returncode, 1)
        self.assertEqual(resultado.stdout, "")
        self.assertEqual(
            resultado.stderr.strip().splitlines(),
            [
                "Error semántico: la asignación a contador requiere int; recibió bool",
                "Error semántico: la condición de while debe ser bool; recibió int",
            ],
        )

    def test_conserva_errores_lexicos_y_sintacticos(self):
        for ejemplo, mensaje in (
            ("error_lexico.imp", "Error léxico en línea 2, columna 8: '@'"),
            ("error_sintactico.imp", "Error sintáctico en línea 2, columna 8: ';'"),
        ):
            with self.subTest(ejemplo=ejemplo):
                resultado = self.ejecutar(["src/compiler.py"], ejemplo)
                self.assertEqual(resultado.returncode, 1)
                self.assertEqual(resultado.stderr.strip(), mensaje)
                self.assertEqual(resultado.stdout, "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
