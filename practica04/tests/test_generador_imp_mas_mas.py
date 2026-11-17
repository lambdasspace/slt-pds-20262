"""Pruebas proporcionadas de la generación para IMP++. No modificar."""

import unittest

from src import asa as a
from src.generador import GeneradorC, generar_c
from src.tabla_simbolos import TablaTipos, Tipo
from src.verificador_tipos import verifica


class PruebasGeneradorImpMasMas(unittest.TestCase):
    def test_menos_unario(self):
        generador = GeneradorC(TablaTipos())
        self.assertEqual(generador.expresion(a.NEG(a.NUM(2))), "(-2)")

    def test_declaraciones_e_impresion_por_tipo(self):
        programa = a.PROGRAMA([
            a.DECL(a.TIPO("int"), a.LOC("cantidad"), a.NEG(a.NUM(2))),
            a.DECL(a.TIPO("bool"), a.LOC("activo"), a.BOOL(True)),
            a.PRINT(a.LOC("cantidad")),
            a.PRINT(a.LOC("activo")),
        ])
        semantica = verifica(programa)
        self.assertTrue(semantica.es_valido, semantica.errores)
        codigo = generar_c(programa, semantica.tabla).codigo

        self.assertIn("long long imp_cantidad = 0;", codigo)
        self.assertIn("bool imp_activo = false;", codigo)
        self.assertIn("imp_cantidad = (-2);", codigo)
        self.assertIn("imp_activo = true;", codigo)
        self.assertIn(
            'printf("%lld\\n", (long long)(imp_cantidad));',
            codigo,
        )
        self.assertIn(
            'printf("%s\\n", imp_activo ? "true" : "false");',
            codigo,
        )

    def test_impresion_de_expresiones_no_solo_localidades(self):
        tabla = TablaTipos()
        tabla.declarar("activo", Tipo.BOOLEANO)
        programa = a.PROGRAMA([
            a.PRINT(a.PLUS(a.NUM(2), a.NUM(3))),
            a.PRINT(a.NOT(a.LOC("activo"))),
        ])
        codigo = generar_c(programa, tabla).codigo
        self.assertIn(
            'printf("%lld\\n", (long long)((2 + 3)));',
            codigo,
        )
        self.assertIn(
            'printf("%s\\n", (!imp_activo) ? "true" : "false");',
            codigo,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
