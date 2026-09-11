"""Pruebas del analizador léxico funcional de IMP."""

from __future__ import annotations

import unittest

from lark.exceptions import UnexpectedCharacters

from src.lexer import analizar, tokenizar


def tipos_y_lexemas(codigo_fuente: str) -> list[tuple[str, str]]:
    """Reduce los tokens a los campos relevantes para varias pruebas."""
    return [
        (token.type, str(token)) for token in analizar(codigo_fuente).tokens
    ]


class PruebasLexerBase(unittest.TestCase):
    def test_programa_con_ciclo(self) -> None:
        codigo = "X := 0;\nwhile X <= 3 do X := X + 1"
        self.assertEqual(tokenizar(codigo), analizar(codigo).tokens)
        self.assertEqual(
            tipos_y_lexemas(codigo),
            [
                ("LOC", "X"),
                ("ASSIGN", ":="),
                ("NUM", "0"),
                ("SEMI", ";"),
                ("WHILE", "while"),
                ("LOC", "X"),
                ("LE", "<="),
                ("NUM", "3"),
                ("DO", "do"),
                ("LOC", "X"),
                ("ASSIGN", ":="),
                ("LOC", "X"),
                ("PLUS", "+"),
                ("NUM", "1"),
            ],
        )

    def test_asignacion_aritmetica(self) -> None:
        self.assertEqual(
            tipos_y_lexemas("X := X + 2;"),
            [
                ("LOC", "X"),
                ("ASSIGN", ":="),
                ("LOC", "X"),
                ("PLUS", "+"),
                ("NUM", "2"),
                ("SEMI", ";"),
            ],
        )

    def test_palabra_reservada_y_localidad(self) -> None:
        self.assertEqual(
            tipos_y_lexemas("if if2 then skip"),
            [
                ("IF", "if"),
                ("LOC", "if2"),
                ("THEN", "then"),
                ("SKIP", "skip"),
            ],
        )

    def test_operadores_booleanos(self) -> None:
        self.assertEqual(
            tipos_y_lexemas("!(X <= 10) || false && true"),
            [
                ("NOT", "!"),
                ("LPAR", "("),
                ("LOC", "X"),
                ("LE", "<="),
                ("NUM", "10"),
                ("RPAR", ")"),
                ("OR", "||"),
                ("FALSE", "false"),
                ("AND", "&&"),
                ("TRUE", "true"),
            ],
        )

    def test_posicion_en_segunda_linea(self) -> None:
        tokens = analizar("X := 1;\nY := 2").tokens
        token_y = tokens[4]
        self.assertEqual(
            (token_y.type, token_y.line, token_y.column),
            ("LOC", 2, 1),
        )

    def test_tabla_reutiliza_la_entrada(self) -> None:
        resultado = analizar("X := 0;\nX := X + 1")
        entradas = resultado.tabla.entradas()
        self.assertEqual(len(entradas), 1)
        self.assertEqual(entradas[0].lexema, "X")
        self.assertEqual(
            [(p.linea, p.columna) for p in entradas[0].apariciones],
            [(1, 1), (2, 1), (2, 6)],
        )

    def test_tabla_distingue_localidades(self) -> None:
        resultado = analizar("X := Y + X")
        self.assertEqual(
            [(e.indice, e.lexema) for e in resultado.tabla.entradas()],
            [(0, "X"), (1, "Y")],
        )
        self.assertIs(resultado.tabla.buscar("X"), resultado.tabla.entradas()[0])

    def test_caracter_no_reconocido(self) -> None:
        with self.assertRaises(UnexpectedCharacters) as contexto:
            analizar("X := 2 @ Y")
        self.assertEqual(
            (contexto.exception.char, contexto.exception.line, contexto.exception.column),
            ("@", 1, 8),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
