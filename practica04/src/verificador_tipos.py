"""Verificación de tipos mediante un recorrido explícito del ASA."""

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


@dataclass(frozen=True)
class DiagnosticoSemantico:
    """Describe un error encontrado durante la verificación."""

    mensaje: str


@dataclass
class ResultadoVerificacion:
    """Resultado de verificar un ASA completo."""

    asa: ASA
    tabla: TablaTipos
    errores: list[DiagnosticoSemantico]

    @property
    def es_valido(self) -> bool:
        return not self.errores


class VerificadorTipos:
    """Implementa los juicios de tipo de IMP y su extensión a IMP++."""

    def __init__(self) -> None:
        self.tabla = TablaTipos()
        self.errores: list[DiagnosticoSemantico] = []

    def error(self, mensaje: str) -> None:
        self.errores.append(DiagnosticoSemantico(mensaje))

    def tipo_expresion(self, nodo: ASA) -> Tipo:
        """Calcula el tipo de una expresión y registra sus errores."""

        if isinstance(nodo, NUM):
            return Tipo.ENTERO

        if isinstance(nodo, BOOL):
            return Tipo.BOOLEANO

        if isinstance(nodo, LOC):
            return self.tabla.asegurar_entera(nodo.nombre).tipo

        if isinstance(nodo, (PLUS, MINUS, TIMES)):
            return self._binaria(
                nodo, Tipo.ENTERO, Tipo.ENTERO,
                type(nodo).__name__,
            )

        if isinstance(nodo, LE):
            return self._binaria(nodo, Tipo.ENTERO, Tipo.BOOLEANO, "LE")

        if isinstance(nodo, EQ):
            # Este caso funciona para el IMP básico. Adáptalo para que
            # IMP++ permita comparar dos enteros o dos booleanos.
            return self._binaria(nodo, Tipo.ENTERO, Tipo.BOOLEANO, "EQ")

        if isinstance(nodo, NOT):
            return self._unaria(nodo.expresion, Tipo.BOOLEANO, "NOT")

        if isinstance(nodo, (AND, OR)):
            return self._binaria(
                nodo, Tipo.BOOLEANO, Tipo.BOOLEANO,
                type(nodo).__name__,
            )

        if isinstance(nodo, NEG):
            # Aquí va tu código: verifica el menos unario de IMP++.
            raise NotImplementedError("Completa el caso NEG en tipo_expresion")

        self.error(f"se esperaba una expresión; se recibió {type(nodo).__name__}")
        return Tipo.ERROR

    def _unaria(self, expresion: ASA, esperado: Tipo, operador: str) -> Tipo:
        recibido = self.tipo_expresion(expresion)
        if recibido == Tipo.ERROR:
            return Tipo.ERROR
        if recibido != esperado:
            self.error(
                f"el operador {operador} requiere {esperado.value}; "
                f"recibió {recibido.value}"
            )
            return Tipo.ERROR
        return esperado

    def _binaria(
        self,
        nodo: ASA,
        esperado: Tipo,
        resultado: Tipo,
        operador: str,
    ) -> Tipo:
        izquierdo = self.tipo_expresion(nodo.izquierda)
        derecho = self.tipo_expresion(nodo.derecha)

        if Tipo.ERROR in {izquierdo, derecho}:
            return Tipo.ERROR
        if izquierdo != esperado or derecho != esperado:
            self.error(
                f"el operador {operador} requiere operandos {esperado.value}; "
                f"recibió {izquierdo.value} y {derecho.value}"
            )
            return Tipo.ERROR
        return resultado

    def exigir_booleano(self, nodo: ASA, construccion: str) -> None:
        recibido = self.tipo_expresion(nodo)
        if recibido not in {Tipo.BOOLEANO, Tipo.ERROR}:
            self.error(
                f"la condición de {construccion} debe ser bool; "
                f"recibió {recibido.value}"
            )

    def verificar_comando(self, nodo: ASA) -> None:
        """Comprueba que un comando esté bien tipificado."""

        if isinstance(nodo, PROGRAMA):
            for elemento in nodo.elementos:
                self.verificar_comando(elemento)
            return

        if isinstance(nodo, BLOQUE):
            for elemento in nodo.elementos:
                self.verificar_comando(elemento)
            return

        if isinstance(nodo, SKIP):
            return

        if isinstance(nodo, ASIG):
            destino = self.tabla.asegurar_entera(nodo.variable.nombre)
            origen = self.tipo_expresion(nodo.expresion)
            if origen not in {destino.tipo, Tipo.ERROR}:
                self.error(
                    f"la asignación a {nodo.variable.nombre} requiere "
                    f"{destino.tipo.value}; recibió {origen.value}"
                )
            return

        if isinstance(nodo, SEQ):
            self.verificar_comando(nodo.primero)
            self.verificar_comando(nodo.segundo)
            return

        if isinstance(nodo, IF):
            self.exigir_booleano(nodo.condicion, "if")
            self.verificar_comando(nodo.entonces)
            self.verificar_comando(nodo.si_no)
            return

        if isinstance(nodo, WHILE):
            self.exigir_booleano(nodo.condicion, "while")
            self.verificar_comando(nodo.cuerpo)
            return

        if isinstance(nodo, DECL):
            # La declaración ya está registrada en Gamma. Aquí va tu código:
            # aplica la regla Decl y comprueba el tipo del inicializador.
            raise NotImplementedError("Completa el caso DECL en verificar_comando")

        if isinstance(nodo, PRINT):
            # Aquí va tu código: acepta expresiones int o bool.
            raise NotImplementedError("Completa el caso PRINT en verificar_comando")

        self.error(f"comando desconocido: {type(nodo).__name__}")

    def _tipo_declarado(self, nombre: str) -> Tipo:
        """Traduce los nombres de tipos admitidos por la gramática."""

        return {"int": Tipo.ENTERO, "bool": Tipo.BOOLEANO}[nombre]

    def _registrar_declaraciones(self, nodo: ASA) -> None:
        """Construye el único contexto Gamma antes de aplicar las reglas."""

        if isinstance(nodo, (PROGRAMA, BLOQUE)):
            for elemento in nodo.elementos:
                self._registrar_declaraciones(elemento)
            return

        if isinstance(nodo, SEQ):
            self._registrar_declaraciones(nodo.primero)
            self._registrar_declaraciones(nodo.segundo)
            return

        if isinstance(nodo, IF):
            self._registrar_declaraciones(nodo.entonces)
            self._registrar_declaraciones(nodo.si_no)
            return

        if isinstance(nodo, WHILE):
            self._registrar_declaraciones(nodo.cuerpo)
            return

        if isinstance(nodo, DECL):
            nombre = nodo.variable.nombre
            tipo = self._tipo_declarado(nodo.tipo_declarado.nombre)
            if self.tabla.declarar(nombre, tipo) is None:
                self.error(f"el identificador {nombre} ya fue declarado")

    def verificar(self, asa: ASA) -> ResultadoVerificacion:
        """Verifica un ASA desazucarado y devuelve sus diagnósticos."""

        self._registrar_declaraciones(asa)
        self.verificar_comando(asa)
        return ResultadoVerificacion(asa, self.tabla, self.errores)


def verifica(asa: ASA) -> ResultadoVerificacion:
    """Punto de entrada; el argumento debe ser un ASA desazucarado."""

    return VerificadorTipos().verificar(asa)
