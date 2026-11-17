"""Generación de C para un ASA desazucarado y verificado de IMP++."""

from __future__ import annotations

from dataclasses import dataclass

if __package__:
    from .asa import (
        AND, ASIG, ASA, BLOQUE, BOOL, DECL, EQ, IF, LE, LOC, MINUS, NEG,
        NOT, NUM, OR, PLUS, PRINT, PROGRAMA, SEQ, SKIP, TIMES, WHILE,
    )
    from .tabla_simbolos import TablaTipos, Tipo
else:
    from asa import (
        AND, ASIG, ASA, BLOQUE, BOOL, DECL, EQ, IF, LE, LOC, MINUS, NEG,
        NOT, NUM, OR, PLUS, PRINT, PROGRAMA, SEQ, SKIP, TIMES, WHILE,
    )
    from tabla_simbolos import TablaTipos, Tipo


class ErrorGeneracion(Exception):
    """Indica que el generador recibió un nodo o un tipo inesperado."""


@dataclass(frozen=True)
class ResultadoGeneracion:
    """Código C producido y nombres incluidos en la unidad de traducción."""

    codigo: str
    variables: tuple[str, ...]


class GeneradorC:
    """Traduce el ASA mediante un recorrido explícito y legible."""

    OPERADORES = {
        PLUS: "+",
        MINUS: "-",
        TIMES: "*",
        EQ: "==",
        LE: "<=",
        AND: "&&",
        OR: "||",
    }

    def __init__(self, tabla: TablaTipos) -> None:
        self.tabla = tabla
        self.lineas: list[str] = []

    @staticmethod
    def nombre_c(nombre: str) -> str:
        """Evita choques entre nombres de IMP++ y nombres reservados de C."""

        return f"imp_{nombre}"

    @staticmethod
    def tipo_c(tipo: Tipo) -> str:
        """Devuelve la representación en C de un tipo ya verificado."""

        if tipo == Tipo.ENTERO:
            return "long long"
        if tipo == Tipo.BOOLEANO:
            return "bool"
        raise ErrorGeneracion(f"tipo no traducible: {tipo.value}")

    @staticmethod
    def valor_inicial(tipo: Tipo) -> str:
        if tipo == Tipo.ENTERO:
            return "0"
        if tipo == Tipo.BOOLEANO:
            return "false"
        raise ErrorGeneracion(f"tipo no inicializable: {tipo.value}")

    def emitir(self, linea: str = "", nivel: int = 0) -> None:
        self.lineas.append(f"{'    ' * nivel}{linea}")

    def tipo_expresion(self, nodo: ASA) -> Tipo:
        """Consulta el tipo de una expresión validada para elegir su impresión."""

        if isinstance(nodo, NUM):
            return Tipo.ENTERO
        if isinstance(nodo, BOOL):
            return Tipo.BOOLEANO
        if isinstance(nodo, LOC):
            entrada = self.tabla.buscar(nodo.nombre)
            if entrada is None:
                raise ErrorGeneracion(
                    f"la localidad {nodo.nombre} no aparece en la tabla de tipos"
                )
            return entrada.tipo
        if isinstance(nodo, (PLUS, MINUS, TIMES, NEG)):
            return Tipo.ENTERO
        if isinstance(nodo, (EQ, LE, NOT, AND, OR)):
            return Tipo.BOOLEANO
        raise ErrorGeneracion(
            f"no se puede obtener el tipo de {type(nodo).__name__}"
        )

    def expresion(self, nodo: ASA) -> str:
        """Traduce una expresión del ASA a una expresión de C."""

        if isinstance(nodo, NUM):
            return str(nodo.valor)

        if isinstance(nodo, BOOL):
            return "true" if nodo.valor else "false"

        if isinstance(nodo, LOC):
            return self.nombre_c(nodo.nombre)

        if isinstance(nodo, NOT):
            return f"(!{self.expresion(nodo.expresion)})"

        if isinstance(nodo, tuple(self.OPERADORES)):
            operador = self.OPERADORES[type(nodo)]
            izquierda = self.expresion(nodo.izquierda)
            derecha = self.expresion(nodo.derecha)
            return f"({izquierda} {operador} {derecha})"

        if isinstance(nodo, NEG):
            # Aquí va tu código: traduce el menos unario de IMP++.
            raise NotImplementedError("Completa el caso NEG en expresion")

        raise ErrorGeneracion(
            f"se esperaba una expresión; se recibió {type(nodo).__name__}"
        )

    def comando(self, nodo: ASA, nivel: int) -> None:
        """Emite las instrucciones correspondientes a un comando."""

        if isinstance(nodo, (PROGRAMA, BLOQUE)):
            for elemento in nodo.elementos:
                self.comando(elemento, nivel)
            return

        if isinstance(nodo, SKIP):
            self.emitir("; /* skip */", nivel)
            return

        if isinstance(nodo, ASIG):
            destino = self.nombre_c(nodo.variable.nombre)
            self.emitir(f"{destino} = {self.expresion(nodo.expresion)};", nivel)
            return

        if isinstance(nodo, SEQ):
            self.comando(nodo.primero, nivel)
            self.comando(nodo.segundo, nivel)
            return

        if isinstance(nodo, IF):
            self.emitir(f"if ({self.expresion(nodo.condicion)}) {{", nivel)
            self.comando(nodo.entonces, nivel + 1)
            self.emitir("} else {", nivel)
            self.comando(nodo.si_no, nivel + 1)
            self.emitir("}", nivel)
            return

        if isinstance(nodo, WHILE):
            self.emitir(f"while ({self.expresion(nodo.condicion)}) {{", nivel)
            self.comando(nodo.cuerpo, nivel + 1)
            self.emitir("}", nivel)
            return

        if isinstance(nodo, DECL):
            # Aquí va tu código: conserva el momento de la inicialización.
            raise NotImplementedError("Completa el caso DECL en comando")

        if isinstance(nodo, PRINT):
            # Aquí va tu código: usa el tipo para elegir el printf.
            raise NotImplementedError("Completa el caso PRINT en comando")

        raise ErrorGeneracion(f"comando desconocido: {type(nodo).__name__}")

    def generar(self, asa: ASA) -> ResultadoGeneracion:
        """Construye una unidad de traducción C completa."""

        self.emitir("#include <stdbool.h>")
        self.emitir("#include <stdio.h>")
        self.emitir()
        self.emitir("int main(void) {")

        entradas = self.tabla.entradas()
        for entrada in entradas:
            nombre = self.nombre_c(entrada.nombre)
            self.emitir(
                f"{self.tipo_c(entrada.tipo)} {nombre} = "
                f"{self.valor_inicial(entrada.tipo)};",
                1,
            )
        if entradas:
            self.emitir()

        self.comando(asa, 1)
        self.emitir("return 0;", 1)
        self.emitir("}")

        return ResultadoGeneracion(
            codigo="\n".join(self.lineas) + "\n",
            variables=tuple(entrada.nombre for entrada in entradas),
        )


def generar_c(asa: ASA, tabla: TablaTipos) -> ResultadoGeneracion:
    """Punto de entrada de la fase de generación."""

    return GeneradorC(tabla).generar(asa)
