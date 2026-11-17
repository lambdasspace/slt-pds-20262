"""Pruebas proporcionadas del generador funcional para IMP. No modificar."""

import unittest

from src import asa as a
from src.generador import ErrorGeneracion, generar_c
from src.verificador_tipos import verifica


class PruebasGeneradorImp(unittest.TestCase):
    def generar(self, programa):
        semantica = verifica(programa)
        self.assertTrue(semantica.es_valido, semantica.errores)
        return generar_c(programa, semantica.tabla).codigo

    def test_traduce_asignacion_ciclo_y_operadores(self):
        programa = a.PROGRAMA([
            a.ASIG(a.LOC("X"), a.NUM(0)),
            a.WHILE(
                a.LE(a.LOC("X"), a.NUM(3)),
                a.ASIG(a.LOC("X"), a.PLUS(a.LOC("X"), a.NUM(1))),
            ),
        ])
        codigo = self.generar(programa)
        self.assertIn("long long imp_X = 0;", codigo)
        self.assertIn("while ((imp_X <= 3)) {", codigo)
        self.assertIn("imp_X = (imp_X + 1);", codigo)

    def test_traduce_booleanos_y_condicional(self):
        programa = a.PROGRAMA([
            a.IF(
                a.AND(a.BOOL(True), a.NOT(a.BOOL(False))),
                a.ASIG(a.LOC("X"), a.NUM(1)),
                a.SKIP(),
            )
        ])
        codigo = self.generar(programa)
        self.assertIn("if ((true && (!false))) {", codigo)
        self.assertIn("imp_X = 1;", codigo)
        self.assertIn("; /* skip */", codigo)

    def test_prefija_un_nombre_reservado_de_c(self):
        programa = a.PROGRAMA([a.ASIG(a.LOC("main"), a.NUM(1))])
        codigo = self.generar(programa)
        self.assertIn("long long imp_main = 0;", codigo)
        self.assertIn("imp_main = 1;", codigo)

    def test_rechaza_azucar_sintactica(self):
        programa = a.PROGRAMA([a.INC(a.LOC("X"))])
        semantica = verifica(a.PROGRAMA([a.ASIG(a.LOC("X"), a.NUM(0))]))
        with self.assertRaises(ErrorGeneracion):
            generar_c(programa, semantica.tabla)


if __name__ == "__main__":
    unittest.main(verbosity=2)
