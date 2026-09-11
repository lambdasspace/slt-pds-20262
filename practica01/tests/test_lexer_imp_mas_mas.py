"""Pruebas unitarias para la extensión del lexer a IMP++."""

from __future__ import annotations

import unittest

from src.lexer import analizar, tokenizar


def tipos_y_lexemas(codigo_fuente: str) -> list[tuple[str, str]]:
    return [(token.type, str(token)) for token in tokenizar(codigo_fuente)]


class PruebasLexerImpMasMas(unittest.TestCase):
    def test_identificador_con_guion_bajo(self) -> None:
        self.assertEqual(
            tipos_y_lexemas("contador_1 := 0;"),
            [("LOC", "contador_1"), ("ASSIGN", ":="), ("NUM", "0"), ("SEMI", ";")],
        )

    def test_comentario_se_ignora(self) -> None:
        tokens = tokenizar("X := 1; // avance\nY := 2;")
        self.assertEqual([str(token) for token in tokens], ["X", ":=", "1", ";", "Y", ":=", "2", ";"])
        self.assertEqual((tokens[4].type, tokens[4].line, tokens[4].column), ("LOC", 2, 1))

    def test_palabras_reservadas_y_llaves(self) -> None:
        self.assertEqual(
            tipos_y_lexemas("int bool print for { } printable"),
            [
                ("INT", "int"),
                ("BOOL", "bool"),
                ("PRINT", "print"),
                ("FOR", "for"),
                ("LBRACE", "{"),
                ("RBRACE", "}"),
                ("LOC", "printable"),
            ],
        )

    def test_incremento_y_decremento_son_tokens_completos(self) -> None:
        self.assertEqual(
            tipos_y_lexemas("X++ + Y-- - 1"),
            [
                ("LOC", "X"),
                ("INC", "++"),
                ("PLUS", "+"),
                ("LOC", "Y"),
                ("DEC", "--"),
                ("MINUS", "-"),
                ("NUM", "1"),
            ],
        )

    def test_programa_imp_mas_mas(self) -> None:
        codigo = """int contador_1 := 0;
bool activo := true;
for (contador_1 := 0; contador_1 <= 2; contador_1++) {
    print(contador_1); // salida
}
"""
        resultado = analizar(codigo)
        tipos = [token.type for token in resultado.tokens]
        self.assertEqual(
            tipos,
            [
                "INT", "LOC", "ASSIGN", "NUM", "SEMI",
                "BOOL", "LOC", "ASSIGN", "TRUE", "SEMI",
                "FOR", "LPAR", "LOC", "ASSIGN", "NUM", "SEMI",
                "LOC", "LE", "NUM", "SEMI", "LOC", "INC", "RPAR",
                "LBRACE", "PRINT", "LPAR", "LOC", "RPAR", "SEMI", "RBRACE",
            ],
        )
        self.assertEqual(
            [(entrada.lexema, len(entrada.apariciones)) for entrada in resultado.tabla.entradas()],
            [("contador_1", 5), ("activo", 1)],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
