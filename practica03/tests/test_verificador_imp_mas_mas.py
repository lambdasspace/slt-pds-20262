"""Pruebas proporcionadas de la extensión semántica a IMP++. No modificar."""

import unittest

from src import asa as a
from src.tabla_simbolos import Tipo
from src.verificador_tipos import VerificadorTipos, verifica


class PruebasVerificadorImpMasMas(unittest.TestCase):
    def test_declaraciones_impresion_y_menos_unario(self):
        programa = a.PROGRAMA([
            a.DECL(a.TIPO("int"), a.LOC("cantidad"), a.NEG(a.NUM(2))),
            a.DECL(a.TIPO("bool"), a.LOC("activo"), a.BOOL(True)),
            a.PRINT(a.LOC("cantidad")),
            a.PRINT(a.LOC("activo")),
        ])
        resultado = verifica(programa)
        self.assertTrue(resultado.es_valido)
        self.assertEqual(
            [(e.nombre, e.tipo) for e in resultado.tabla.entradas()],
            [("cantidad", Tipo.ENTERO), ("activo", Tipo.BOOLEANO)],
        )

    def test_igualdad_admite_operandos_del_mismo_tipo(self):
        verificador = VerificadorTipos()
        self.assertEqual(
            verificador.tipo_expresion(a.EQ(a.BOOL(True), a.BOOL(False))),
            Tipo.BOOLEANO,
        )
        self.assertEqual(
            verificador.tipo_expresion(a.EQ(a.NUM(1), a.BOOL(True))),
            Tipo.ERROR,
        )
        self.assertEqual(len(verificador.errores), 1)

    def test_inicializador_y_asignacion_deben_conservar_el_tipo(self):
        programa = a.PROGRAMA([
            a.DECL(a.TIPO("bool"), a.LOC("activo"), a.NUM(1)),
            a.DECL(a.TIPO("int"), a.LOC("contador"), a.NUM(0)),
            a.ASIG(a.LOC("contador"), a.BOOL(False)),
        ])
        resultado = verifica(programa)
        self.assertEqual(
            [e.mensaje for e in resultado.errores],
            [
                "la declaración de activo requiere bool; recibió int",
                "la asignación a contador requiere int; recibió bool",
            ],
        )

    def test_rechaza_declaracion_duplicada(self):
        resultado = verifica(a.PROGRAMA([
            a.DECL(a.TIPO("int"), a.LOC("dato"), a.NUM(1)),
            a.DECL(a.TIPO("bool"), a.LOC("dato"), a.BOOL(True)),
        ]))
        self.assertEqual(
            [e.mensaje for e in resultado.errores],
            ["el identificador dato ya fue declarado"],
        )

    def test_condiciones_deben_ser_booleanas(self):
        resultado = verifica(a.PROGRAMA([
            a.DECL(a.TIPO("int"), a.LOC("contador"), a.NUM(0)),
            a.IF(a.LOC("contador"), a.SKIP(), a.SKIP()),
        ]))
        self.assertEqual(
            [e.mensaje for e in resultado.errores],
            ["la condición de if debe ser bool; recibió int"],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
