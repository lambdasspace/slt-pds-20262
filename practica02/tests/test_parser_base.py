"""Pruebas proporcionadas de los comandos y expresiones básicos. No modificar."""

import unittest
from lark import Token
from lark.exceptions import UnexpectedCharacters, UnexpectedToken
from src import asa as a, lexer, parser


def analiza_fuente(fuente):
    tokens, tabla = lexer.analiza(fuente)
    return parser.analiza(tokens)


class PruebasParserBase(unittest.TestCase):
    def test_asignacion_y_valores(self):
        self.assertEqual(analiza_fuente("X := 12;"), a.PROGRAMA([a.ASIG(a.LOC("X"), a.NUM(12))]))

    def test_agrupacion_aritmetica_explicita(self):
        resultado = analiza_fuente("X := ((10 - 3) - (2 * 4));")
        self.assertEqual(resultado.elementos[0].expresion,
                         a.MINUS(a.MINUS(a.NUM(10), a.NUM(3)), a.TIMES(a.NUM(2), a.NUM(4))))
        resultado = analiza_fuente("X := (((2 + 3)) * 4);")
        self.assertEqual(resultado.elementos[0].expresion, a.TIMES(a.PLUS(a.NUM(2), a.NUM(3)), a.NUM(4)))

    def test_condicional_y_expresion_booleana(self):
        resultado = analiza_fuente("if ((!false) || (true && (X <= 3))) then { skip; } else { X := 0; }")
        self.assertEqual(resultado, a.PROGRAMA([
            a.IF(a.OR(a.NOT(a.BOOL(False)), a.AND(a.BOOL(True), a.LE(a.LOC("X"), a.NUM(3)))),
                 a.BLOQUE([a.SKIP()]), a.BLOQUE([a.ASIG(a.LOC("X"), a.NUM(0))]))
        ]))

    def test_igualdad_y_menos_unario(self):
        resultado = analiza_fuente("print(((-2) = (0 - 2)));")
        self.assertEqual(resultado.elementos[0],
                         a.PRINT(a.EQ(a.NEG(a.NUM(2)), a.MINUS(a.NUM(0), a.NUM(2)))))

    def test_llaves_delimitan_el_cuerpo(self):
        dentro = analiza_fuente("while true do { X := 1; Y := 2; }")
        fuera = analiza_fuente("while true do { X := 1; } Y := 2;")
        self.assertEqual(dentro, a.PROGRAMA([
            a.WHILE(a.BOOL(True), a.BLOQUE([a.ASIG(a.LOC("X"), a.NUM(1)), a.ASIG(a.LOC("Y"), a.NUM(2))]))
        ]))
        self.assertEqual(fuera, a.PROGRAMA([
            a.WHILE(a.BOOL(True), a.BLOQUE([a.ASIG(a.LOC("X"), a.NUM(1))])), a.ASIG(a.LOC("Y"), a.NUM(2))
        ]))

    def test_condicionales_anidados(self):
        resultado = analiza_fuente("if true then { if false then { skip; } else { X := 1; } } else { X := 2; }")
        self.assertEqual(resultado.elementos[0].entonces.elementos[0],
                         a.IF(a.BOOL(False), a.BLOQUE([a.SKIP()]), a.BLOQUE([a.ASIG(a.LOC("X"), a.NUM(1))])))
        self.assertEqual(resultado.elementos[0].si_no, a.BLOQUE([a.ASIG(a.LOC("X"), a.NUM(2))]))

    def test_comandos_conservan_orden(self):
        resultado = analiza_fuente("X := 1; Y := 2; Z := 3;")
        self.assertEqual(resultado, a.PROGRAMA([
            a.ASIG(a.LOC("X"), a.NUM(1)), a.ASIG(a.LOC("Y"), a.NUM(2)), a.ASIG(a.LOC("Z"), a.NUM(3))
        ]))

    def test_error_lexico_conserva_posicion(self):
        with self.assertRaises(UnexpectedCharacters) as contexto:
            analiza_fuente("X := 1;\nY := @")
        error = contexto.exception
        self.assertEqual((error.char, error.line, error.column), ("@", 2, 6))

    def test_error_sintactico_con_token(self):
        with self.assertRaises(UnexpectedToken) as contexto:
            analiza_fuente("X := ;")
        error = contexto.exception
        self.assertEqual((str(error.token), error.line, error.column), (";", 1, 6))

    def test_error_al_final_del_archivo(self):
        with self.assertRaises(UnexpectedToken) as contexto:
            analiza_fuente("X :=\n")
        self.assertEqual(contexto.exception.token.type, "$END")

    def test_recibe_tokens_sin_programa_fuente(self):
        tokens = [Token("SKIP", "skip", line=4, column=2), Token("SEMI", ";", line=4, column=6)]
        self.assertEqual(parser.analiza(tokens), a.PROGRAMA([a.SKIP()]))

    def test_rechaza_programa_vacio(self):
        with self.assertRaises(UnexpectedToken):
            analiza_fuente("")


if __name__ == "__main__":
    unittest.main(verbosity=2)
