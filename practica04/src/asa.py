from dataclasses import dataclass


class ASA:
    """Clase base para los nodos del árbol de sintaxis abstracta."""
    pass


@dataclass(frozen=True)
class NUM(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class LOC(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class BOOL(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class PLUS(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class MINUS(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class TIMES(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class EQ(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class LE(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class NOT(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class AND(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class OR(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class SKIP(ASA):
    # SKIP no necesita atributos.
    pass


@dataclass(frozen=True)
class ASIG(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class SEQ(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class IF(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class WHILE(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class PROGRAMA(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class BLOQUE(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class TIPO(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class DECL(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class PRINT(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class NEG(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class INC(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class DEC(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass


@dataclass(frozen=True)
class FOR(ASA):
    # Aquí va tu código: escribe los atributos de este nodo.
    pass
