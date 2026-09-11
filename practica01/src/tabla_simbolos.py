"""Tabla léxica de localidades de IMP."""

from __future__ import annotations

from dataclasses import dataclass, field

from lark import Token


@dataclass(frozen=True)
class Aparicion:
    """Posición inicial de una aparición en el programa fuente."""

    linea: int
    columna: int


@dataclass
class EntradaSimbolo:
    """Información disponible para una localidad durante el análisis léxico."""

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
        """Busca una localidad sin modificar la tabla."""
        return self._por_lexema.get(lexema)

    def entradas(self) -> list[EntradaSimbolo]:
        """Devuelve las entradas en orden de descubrimiento."""
        return list(self._por_lexema.values())
