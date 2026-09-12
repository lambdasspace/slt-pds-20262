"""Pruebas proporcionadas del desendulzado del ASA. No modificar."""

import unittest
from lark import Token, Tree
from src import asa as a, parser


class PruebasDesugar(unittest.TestCase):
    def test_incremento_y_decremento(self):
        for nodo, operacion in ((a.INC, a.PLUS), (a.DEC, a.MINUS)):
            with self.subTest(nodo=nodo):
                self.assertEqual(parser.desugar(nodo(a.LOC("X"))),
                                 a.ASIG(a.LOC("X"), operacion(a.LOC("X"), a.NUM(1))))

    def test_construye_asa_devuelve_resultado_desendulzado(self):
        arbol = Tree("incremento", [Token("LOC", "X"), Token("INC", "++")])
        self.assertEqual(parser.construye_asa(arbol),
                         a.ASIG(a.LOC("X"), a.PLUS(a.LOC("X"), a.NUM(1))))

    def test_recorrido_de_bloques_condicionales_y_ciclos(self):
        original = a.PROGRAMA([a.BLOQUE([a.IF(
            a.BOOL(True), a.BLOQUE([a.INC(a.LOC("X"))]),
            a.BLOQUE([a.WHILE(a.BOOL(False), a.BLOQUE([a.DEC(a.LOC("Y"))]))])
        )])])
        esperado = a.PROGRAMA([a.BLOQUE([a.IF(
            a.BOOL(True), a.BLOQUE([a.ASIG(a.LOC("X"), a.PLUS(a.LOC("X"), a.NUM(1)))]),
            a.BLOQUE([a.WHILE(a.BOOL(False), a.BLOQUE([
                a.ASIG(a.LOC("Y"), a.MINUS(a.LOC("Y"), a.NUM(1)))
            ]))])
        )])])
        self.assertEqual(parser.desugar(original), esperado)

    def test_for_anidado_y_cuerpo_vacio(self):
        interior = a.FOR(a.ASIG(a.LOC("j"), a.NUM(0)), a.BOOL(False), a.DEC(a.LOC("j")), a.BLOQUE([]))
        exterior = a.FOR(a.ASIG(a.LOC("i"), a.NUM(0)), a.BOOL(True), a.INC(a.LOC("i")), a.BLOQUE([interior]))
        interior_esperado = a.SEQ(a.ASIG(a.LOC("j"), a.NUM(0)), a.WHILE(a.BOOL(False), a.SEQ(
            a.BLOQUE([]), a.ASIG(a.LOC("j"), a.MINUS(a.LOC("j"), a.NUM(1)))
        )))
        esperado = a.SEQ(a.ASIG(a.LOC("i"), a.NUM(0)), a.WHILE(a.BOOL(True), a.SEQ(
            a.BLOQUE([interior_esperado]), a.ASIG(a.LOC("i"), a.PLUS(a.LOC("i"), a.NUM(1)))
        )))
        self.assertEqual(parser.desugar(exterior), esperado)

    def test_conserva_arbol_sin_azucar(self):
        original = a.PROGRAMA([
            a.DECL(a.TIPO("bool"), a.LOC("activo"), a.NOT(a.BOOL(False))),
            a.PRINT(a.TIMES(a.NEG(a.NUM(2)), a.PLUS(a.NUM(1), a.NUM(3)))),
            a.SEQ(a.SKIP(), a.BLOQUE([]))
        ])
        self.assertEqual(parser.desugar(original), original)


if __name__ == "__main__":
    unittest.main(verbosity=2)
