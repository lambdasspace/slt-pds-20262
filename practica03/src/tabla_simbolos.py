"""Tablas de símbolos para las fases léxica y semántica de IMP++."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from lark import Token


@dataclass(frozen=True)
class Aparicion:
    """Posición inicial de una aparición en el programa fuente."""

    linea: int
    columna: int


@dataclass
class EntradaSimbolo:
    """Información léxica disponible para un identificador."""

    indice: int
    lexema: str
    apariciones: list[Aparicion] = field(default_factory=list)


class TablaSimbolos:
    """Conserva una entrada por lexema LOC, en orden de descubrimiento."""

    def __init__(self) -> None:
        self._por_lexema: dict[str, EntradaSimbolo] = {}

    def registrar(self, token: Token) -> EntradaSimbolo:
        """Registra la aparición de un LOC y devuelve su entrada compartida."""

        if token.type != "LOC":
            raise ValueError("Solo se registran tokens LOC")

        lexema = str(token)
        if lexema not in self._por_lexema:
            self._por_lexema[lexema] = EntradaSimbolo(
                indice=len(self._por_lexema),
                lexema=lexema,
            )

        entrada = self._por_lexema[lexema]
        entrada.apariciones.append(Aparicion(token.line, token.column))
        return entrada

    def buscar(self, lexema: str) -> EntradaSimbolo | None:
        """Busca un identificador sin modificar la tabla."""

        return self._por_lexema.get(lexema)

    def entradas(self) -> list[EntradaSimbolo]:
        """Devuelve las entradas en orden de descubrimiento."""

        return list(self._por_lexema.values())


class Tipo(Enum):
    """Tipos de IMP++ y marca interna para contener errores."""

    ENTERO = "int"
    BOOLEANO = "bool"
    ERROR = "error"


@dataclass(frozen=True)
class EntradaTipo:
    """Asociación entre un identificador y su tipo."""

    nombre: str
    tipo: Tipo


class TablaTipos:
    """Contexto de tipos plano para los juicios de la práctica."""

    def __init__(self) -> None:
        self._por_nombre: dict[str, EntradaTipo] = {}

    def declarar(self, nombre: str, tipo: Tipo) -> EntradaTipo | None:
        """Agrega una asociación o devuelve None si el nombre ya existe."""

        if nombre in self._por_nombre:
            return None
        entrada = EntradaTipo(nombre, tipo)
        self._por_nombre[nombre] = entrada
        return entrada

    def buscar(self, nombre: str) -> EntradaTipo | None:
        """Busca un identificador sin modificar el contexto."""

        return self._por_nombre.get(nombre)

    def asegurar_entera(self, nombre: str) -> EntradaTipo:
        """Conserva la regla de variables implícitas enteras de IMP."""

        entrada = self.buscar(nombre)
        if entrada is not None:
            return entrada

        entrada = EntradaTipo(nombre, Tipo.ENTERO)
        self._por_nombre[nombre] = entrada
        return entrada

    def entradas(self) -> list[EntradaTipo]:
        """Devuelve las asociaciones en orden de registro."""

        return list(self._por_nombre.values())
