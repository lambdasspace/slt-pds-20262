"""Pruebas proporcionadas del verificador funcional de IMP. No modificar."""

import unittest

from src import asa as a
from src.tabla_simbolos import Tipo
from src.verificador_tipos import VerificadorTipos, verifica


class PruebasVerificadorImp(unittest.TestCase):
    def test_programa_imp_bien_tipificado(self):
        programa = a.PROGRAMA([
            a.ASIG(a.LOC("X"), a.NUM(0)),
            a.WHILE(
                a.LE(a.LOC("X"), a.NUM(3)),
                a.ASIG(a.LOC("X"), a.PLUS(a.LOC("X"), a.NUM(1))),
            ),
        ])
        resultado = verifica(programa)
        self.assertTrue(resultado.es_valido)
        self.assertEqual(
            [(e.nombre, e.tipo) for e in resultado.tabla.entradas()],
            [("X", Tipo.ENTERO)],
        )

    def test_tipos_de_expresiones_de_imp(self):
        verificador = VerificadorTipos()
        expresiones = (
            (a.NUM(1), Tipo.ENTERO),
            (a.BOOL(True), Tipo.BOOLEANO),
            (a.TIMES(a.NUM(2), a.NUM(3)), Tipo.ENTERO),
            (a.EQ(a.NUM(2), a.NUM(2)), Tipo.BOOLEANO),
            (a.NOT(a.BOOL(False)), Tipo.BOOLEANO),
            (a.OR(a.BOOL(False), a.BOOL(True)), Tipo.BOOLEANO),
        )
        for expresion, esperado in expresiones:
            with self.subTest(expresion=expresion):
                self.assertEqual(verificador.tipo_expresion(expresion), esperado)
        self.assertEqual(verificador.errores, [])

    def test_detecta_errores_independientes(self):
        programa = a.PROGRAMA([
            a.ASIG(a.LOC("X"), a.PLUS(a.BOOL(True), a.NUM(1))),
            a.WHILE(a.NUM(1), a.SKIP()),
        ])
        resultado = verifica(programa)
        self.assertEqual(
            [e.mensaje for e in resultado.errores],
            [
                "el operador PLUS requiere operandos int; recibió bool y int",
                "la condición de while debe ser bool; recibió int",
            ],
        )

    def test_no_repite_un_error_en_expresiones_exteriores(self):
        expresion = a.TIMES(
            a.AND(a.NUM(1), a.BOOL(True)),
            a.NUM(2),
        )
        resultado = verifica(a.PROGRAMA([a.ASIG(a.LOC("X"), expresion)]))
        self.assertEqual(len(resultado.errores), 1)
        self.assertIn("operador AND", resultado.errores[0].mensaje)


if __name__ == "__main__":
    unittest.main(verbosity=2)
