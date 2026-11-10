"""Pruebas proporcionadas de la extensión a IMP++. No modificar."""

import unittest
from pathlib import Path
from lark.exceptions import UnexpectedToken
from src import asa as a, lexer, parser


def analiza_fuente(fuente):
    tokens, tabla = lexer.analiza(fuente)
    return parser.analiza(tokens)


class PruebasParserImpMasMas(unittest.TestCase):
    def test_declaraciones_y_tokens_de_la_practica_1(self):
        fuente = "int contador_1 := 0; // avance\nbool activo := true; print(contador_1);"
        tokens, tabla = lexer.analiza(fuente)
        self.assertEqual(parser.analiza(tokens), a.PROGRAMA([
            a.DECL(a.TIPO("int"), a.LOC("contador_1"), a.NUM(0)),
            a.DECL(a.TIPO("bool"), a.LOC("activo"), a.BOOL(True)), a.PRINT(a.LOC("contador_1"))
        ]))
        self.assertEqual([e.lexema for e in tabla.entradas()], ["contador_1", "activo"])
        self.assertNotIn("COMMENT", [t.type for t in tokens])

    def test_bloques_anidados_y_vacios(self):
        resultado = analiza_fuente("{ int X := 1; { int X := 2; print(X); } {} }")
        self.assertEqual(resultado, a.PROGRAMA([a.BLOQUE([
            a.DECL(a.TIPO("int"), a.LOC("X"), a.NUM(1)),
            a.BLOQUE([a.DECL(a.TIPO("int"), a.LOC("X"), a.NUM(2)), a.PRINT(a.LOC("X"))]), a.BLOQUE([])
        ])]))

    def test_incremento_y_decremento_desendulzados(self):
        for fuente, operacion in (("X++;", a.PLUS), ("X--;", a.MINUS)):
            with self.subTest(fuente=fuente):
                self.assertEqual(analiza_fuente(fuente),
                                 a.PROGRAMA([a.ASIG(a.LOC("X"), operacion(a.LOC("X"), a.NUM(1)))]))

    def test_for_y_sus_tres_actualizaciones(self):
        for actualizacion, operacion, paso in (("i++", a.PLUS, 1), ("i--", a.MINUS, 1), ("i := (i + 2)", a.PLUS, 2)):
            with self.subTest(actualizacion=actualizacion):
                resultado = analiza_fuente(f"for (i := 0; (i <= 2); {actualizacion}) {{ print(i); }}")
                self.assertEqual(resultado, a.PROGRAMA([a.SEQ(
                    a.ASIG(a.LOC("i"), a.NUM(0)),
                    a.WHILE(a.LE(a.LOC("i"), a.NUM(2)), a.SEQ(
                        a.BLOQUE([a.PRINT(a.LOC("i"))]),
                        a.ASIG(a.LOC("i"), operacion(a.LOC("i"), a.NUM(paso)))
                    ))
                )]))

    def test_for_conserva_el_bloque_antes_de_actualizar(self):
        resultado = analiza_fuente("for (i := 0; (i <= 2); i++) { int i := 9; print(i); }")
        vuelta = resultado.elementos[0].segundo.cuerpo
        self.assertEqual(vuelta.primero, a.BLOQUE([
            a.DECL(a.TIPO("int"), a.LOC("i"), a.NUM(9)), a.PRINT(a.LOC("i"))
        ]))
        self.assertEqual(vuelta.segundo, a.ASIG(a.LOC("i"), a.PLUS(a.LOC("i"), a.NUM(1))))

    def test_condicional_y_while_desendulzados(self):
        resultado = analiza_fuente("if true then { skip; } else { while (X <= 2) do { X++; } }")
        self.assertEqual(resultado.elementos[0].si_no.elementos[0].cuerpo,
                         a.BLOQUE([a.ASIG(a.LOC("X"), a.PLUS(a.LOC("X"), a.NUM(1)))]))

    def test_programa_completo(self):
        ruta = Path(__file__).resolve().parents[1] / "ejemplos/imp_mas_mas.imp"
        resultado = analiza_fuente(ruta.read_text(encoding="utf-8"))
        self.assertEqual([type(n) for n in resultado.elementos], [a.DECL, a.DECL, a.SEQ, a.IF])

    def test_rechaza_construcciones_incompletas(self):
        for fuente in (
            "print(1)", "X++", "{ X := 1 }", "int X := 1;",
            "print(1); int X := 1;", "{ print(1); int X := 1; }",
            "if true then { skip; }", "for (i := 0; (i <= 2); i++) print(i);",
            "for (int i := 0; (i <= 2); i++) {}", "print(1 <= 2 <= 3);",
            "print(true = false = true);", "while true do {", "print(1 + 2);",
            "print((1 + 2 * 3));", "print(!false);", "if true && false then {} else {}",
            "while true do skip;", "X := -1;"
        ):
            with self.subTest(fuente=fuente):
                with self.assertRaises(UnexpectedToken):
                    analiza_fuente(fuente)

    def test_posiciones_despues_de_comentarios(self):
        tokens, tabla = lexer.analiza("// @ ignorada\r\n\tprint((-2)); // fin")
        self.assertEqual((tokens[0].type, tokens[0].line, tokens[0].column), ("PRINT", 2, 2))
        self.assertEqual(parser.analiza(tokens), a.PROGRAMA([a.PRINT(a.NEG(a.NUM(2)))]))

    def test_expresiones_booleanas_en_asignacion(self):
        self.assertEqual(analiza_fuente("activo := (X = 1);"),
                         a.PROGRAMA([a.ASIG(a.LOC("activo"), a.EQ(a.LOC("X"), a.NUM(1)))]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
