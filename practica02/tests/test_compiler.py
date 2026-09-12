"""Pruebas proporcionadas del compilador integrado. No modificar."""

import json
from pathlib import Path
import subprocess
import sys
import unittest
from src import asa as a
from src.compiler import a_diccionario


BASE = Path(__file__).resolve().parents[1]


class PruebasCompiler(unittest.TestCase):
    def test_json_conserva_operaciones_y_listas(self):
        arbol = a.PROGRAMA([a.PRINT(a.MINUS(a.NUM(4), a.NUM(2)))])
        self.assertEqual(a_diccionario(arbol), {
            "tipo": "PROGRAMA", "elementos": [{"tipo": "PRINT", "expresion": {
                "tipo": "MINUS", "izquierda": {"tipo": "NUM", "valor": 4},
                "derecha": {"tipo": "NUM", "valor": 2}
            }}]
        })

    def test_archivo_y_modulo_entregan_asa_desendulzado(self):
        salidas = []
        for entrada in (["src/compiler.py"], ["-m", "src.compiler"]):
            resultado = subprocess.run(
                [sys.executable, "-B", *entrada, "ejemplos/imp_mas_mas.imp"],
                cwd=BASE, capture_output=True, text=True
            )
            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            arbol = json.loads(resultado.stdout)
            self.assertEqual(arbol["tipo"], "PROGRAMA")
            self.assertEqual([n["tipo"] for n in arbol["elementos"]], ["DECL", "DECL", "SEQ", "IF"])
            for tipo in ("INC", "DEC", "FOR"):
                self.assertNotIn(f'"tipo": "{tipo}"', resultado.stdout)
            salidas.append(arbol)
        self.assertEqual(salidas[0], salidas[1])

    def test_mensajes_de_error(self):
        for ejemplo, mensaje in (
            ("error_lexico.imp", "Error léxico en línea 2, columna 8: '@'"),
            ("error_sintactico.imp", "Error sintáctico en línea 2, columna 8: ';'"),
        ):
            with self.subTest(ejemplo=ejemplo):
                resultado = subprocess.run(
                    [sys.executable, "-B", "src/compiler.py", f"ejemplos/{ejemplo}"],
                    cwd=BASE, capture_output=True, text=True
                )
                self.assertEqual(resultado.returncode, 1)
                self.assertEqual(resultado.stderr.strip(), mensaje)
                self.assertEqual(resultado.stdout, "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
