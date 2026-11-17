"""Pruebas proporcionadas del pipeline hasta el ejecutable .out. No modificar."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from src.compiler import ErrorCompiladorC, compilar, invocar_gcc


BASE = Path(__file__).resolve().parents[1]


class PruebasCompiler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if shutil.which("gcc") is None:
            raise AssertionError(
                "La práctica 4 requiere GCC. Comprueba el comando 'gcc --version'."
            )

    def ejecutar_compilador(self, fuente, salida):
        return subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "src.compiler",
                str(fuente),
                "-o",
                str(salida),
            ],
            cwd=BASE,
            capture_output=True,
            text=True,
        )

    def test_genera_c_out_y_salida_observable(self):
        fuente = BASE / "ejemplos" / "imp_mas_mas.imp"
        with tempfile.TemporaryDirectory() as temporal:
            ruta = Path(temporal)
            salida = ruta / "programa.out"
            resultado = self.ejecutar_compilador(fuente, salida)

            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            self.assertTrue((ruta / "programa.c").is_file())
            self.assertTrue(salida.is_file())
            self.assertIn("Ejecutable generado por GCC", resultado.stdout)

            ejecucion = subprocess.run(
                [str(salida)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(ejecucion.returncode, 0, ejecucion.stderr)
            self.assertEqual(ejecucion.stdout, "0\n1\n2\n3\n-2\ntrue\n")

    def test_conserva_compatibilidad_con_imp(self):
        fuente = BASE / "ejemplos" / "imp_base.imp"
        with tempfile.TemporaryDirectory() as temporal:
            salida = Path(temporal) / "imp.out"
            resultado = self.ejecutar_compilador(fuente, salida)
            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            self.assertTrue(salida.is_file())

    def test_error_semantico_detiene_generacion_y_gcc(self):
        with patch("src.compiler.generador.generar_c") as generar:
            resultado = compilar("int X := 0; X := false;")
        self.assertFalse(resultado.semantica.es_valido)
        self.assertIsNone(resultado.generacion)
        generar.assert_not_called()

    def test_cli_no_crea_productos_para_errores_previos(self):
        casos = (
            ("error_lexico.imp", "Error léxico"),
            ("error_sintactico.imp", "Error sintáctico"),
            ("error_tipos.imp", "Error semántico"),
        )
        with tempfile.TemporaryDirectory() as temporal:
            ruta = Path(temporal)
            for indice, (ejemplo, mensaje) in enumerate(casos):
                with self.subTest(ejemplo=ejemplo):
                    salida = ruta / f"error{indice}.out"
                    resultado = self.ejecutar_compilador(
                        BASE / "ejemplos" / ejemplo,
                        salida,
                    )
                    self.assertEqual(resultado.returncode, 1)
                    self.assertIn(mensaje, resultado.stderr)
                    self.assertFalse(salida.exists())
                    self.assertFalse(salida.with_suffix(".c").exists())

    def test_informa_si_gcc_no_esta_disponible(self):
        with patch("src.compiler.shutil.which", return_value=None):
            with self.assertRaisesRegex(ErrorCompiladorC, "No se encontró GCC"):
                invocar_gcc(Path("programa.c"), Path("programa.out"))

    def test_conserva_c_si_gcc_lo_rechaza(self):
        with tempfile.TemporaryDirectory() as temporal:
            ruta = Path(temporal)
            archivo_c = ruta / "incorrecto.c"
            salida = ruta / "incorrecto.out"
            archivo_c.write_text("esto no es C\n", encoding="utf-8")

            with self.assertRaises(ErrorCompiladorC):
                invocar_gcc(archivo_c, salida)

            self.assertTrue(archivo_c.is_file())
            self.assertFalse(salida.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
