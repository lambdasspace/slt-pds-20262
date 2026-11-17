"""Pruebas proporcionadas de la tabla de tipos. No modificar."""

import unittest

from src.tabla_simbolos import TablaTipos, Tipo


class PruebasTablaTipos(unittest.TestCase):
    def test_declarar_y_buscar(self):
        tabla = TablaTipos()
        entrada = tabla.declarar("contador", Tipo.ENTERO)
        self.assertIs(tabla.buscar("contador"), entrada)
        self.assertEqual((entrada.nombre, entrada.tipo),
                         ("contador", Tipo.ENTERO))

    def test_rechaza_identificador_duplicado(self):
        tabla = TablaTipos()
        self.assertIsNotNone(tabla.declarar("activo", Tipo.BOOLEANO))
        self.assertIsNone(tabla.declarar("activo", Tipo.ENTERO))

    def test_identificador_implicito_se_registra_como_entero(self):
        tabla = TablaTipos()
        entrada = tabla.asegurar_entera("X")
        self.assertEqual(entrada.tipo, Tipo.ENTERO)
        self.assertIs(tabla.buscar("X"), entrada)

    def test_conserva_el_orden_de_registro(self):
        tabla = TablaTipos()
        tabla.declarar("primero", Tipo.ENTERO)
        tabla.declarar("segundo", Tipo.BOOLEANO)
        self.assertEqual(
            [entrada.nombre for entrada in tabla.entradas()],
            ["primero", "segundo"],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
