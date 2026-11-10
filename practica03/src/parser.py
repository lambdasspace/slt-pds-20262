"""Completar los casos de IMP++ en construye_nodo y la función desugar."""

from pathlib import Path
from lark import Lark, Token, Tree
if __package__:
    from .asa import (
        ASA, NUM, LOC, BOOL, PLUS, MINUS, TIMES, EQ, LE, NOT, AND, OR,
        SKIP, ASIG, SEQ, IF, WHILE, PROGRAMA, BLOQUE, TIPO, DECL,
        PRINT, NEG, INC, DEC, FOR
    )
else:
    from asa import (
        ASA, NUM, LOC, BOOL, PLUS, MINUS, TIMES, EQ, LE, NOT, AND, OR,
        SKIP, ASIG, SEQ, IF, WHILE, PROGRAMA, BLOQUE, TIPO, DECL,
        PRINT, NEG, INC, DEC, FOR
    )


def analiza(tokens: list[Token]) -> ASA:
    """Recibe una lista de tokens y devuelve el ASA desendulzado."""

    # 1. Obtener la ruta del módulo del analizador sintáctico
    archivo_actual = Path(__file__)

    # 2. Obtener la ruta del archivo con la gramática
    archivo_gramatica = archivo_actual.with_name("grammars.lark")

    # 3. Leer la gramática
    gramatica = archivo_gramatica.read_text(encoding="utf-8")

    # 4. Construir el analizador sintáctico
    analizador = Lark(
        gramatica,
        parser="lalr", # Análisis ascendente usando LALR(1)
        lexer="basic",
        start="programa", # Indicamos el símbolo inicial
        propagate_positions=True
    )

    # 5. Crear una sesión de análisis sintáctico interactivo
    sesion = analizador.parse_interactive()

    # 6. Entregar los tokens al parser uno por uno
    # La sesión recibe los tokens que ya produjo el analizador léxico.
    for token in tokens:
        sesion.feed_token(token)

    # 7. Indicar que ya no hay más tokens
    arbol_sintactico = sesion.feed_eof()

    # 8. Convertir el árbol de análisis sintáctico de Lark en un ASA
    asa = construye_asa(arbol_sintactico)

    # 9. Devolver el ASA
    return asa


# Estos tokens contienen los datos que se guardan en las hojas del ASA.
DATOS = {"NUM", "LOC", "TRUE", "FALSE"}


def construye_asa(arbol: Tree | Token) -> ASA:
    """Construye los nodos y devuelve el ASA desendulzado."""

    # 1. Construir los nodos del ASA a partir del árbol de Lark.
    asa = construye_nodo(arbol)

    # 2. Eliminar el azúcar sintáctica antes de devolver el ASA.
    return desugar(asa)


def construye_nodo(arbol: Tree | Token) -> ASA:
    """Convierte recursivamente un Tree de Lark en un ASA."""

    # 1. Caso base de la recursión:
    #    convertir los tokens que contienen datos en hojas del ASA.
    if isinstance(arbol, Token):

        if arbol.type == "NUM":
            return NUM(int(arbol.value))

        if arbol.type == "LOC":
            return LOC(str(arbol.value))

        if arbol.type == "TRUE":
            return BOOL(True)

        if arbol.type == "FALSE":
            return BOOL(False)

        raise ValueError(f"Token inesperado: {arbol.type}")

    # 2. Obtener el nombre de la regla de producción
    #    utilizada por Lark para construir este nodo.
    regla = str(arbol.data)

    # 3. Eliminar los tokens que pertenecen únicamente
    #    a la sintaxis concreta. El nombre de la regla
    #    ya indica qué operación o comando se debe construir.
    hijos = [
        hijo
        for hijo in arbol.children
        if not isinstance(hijo, Token) or hijo.type in DATOS
    ]

    # 4. Los paréntesis no forman parte del ASA.
    if regla == "parentesis":
        return construye_nodo(hijos[0])

    # 5. Si una producción sólo envuelve un dato o comando,
    #    continuar recursivamente con ese contenido.
    if regla in {"numero", "variable", "verdadero", "falso", "sentencia", "actualizacion"}:
        return construye_nodo(hijos[0])

    # 6. Construir recursivamente los hijos.
    hijos_asa = [
        construye_nodo(hijo)
        for hijo in hijos
    ]

    # 7. Construir el nodo del ASA correspondiente.
    if regla == "programa":
        return PROGRAMA(hijos_asa)

    if regla == "bloque":
        return BLOQUE(hijos_asa)

    if regla == "suma":
        return PLUS(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "resta":
        return MINUS(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "multiplicacion":
        return TIMES(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "igualdad":
        return EQ(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "menor_igual":
        return LE(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "negacion":
        return NOT(
            hijos_asa[0]
        )

    if regla == "conjuncion":
        return AND(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "disyuncion":
        return OR(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "omitir":
        return SKIP()

    if regla == "asignacion":
        return ASIG(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "secuencia":
        return SEQ(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "condicional":
        return IF(
            hijos_asa[0],
            hijos_asa[1],
            hijos_asa[2]
        )

    if regla == "mientras":
        return WHILE(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "tipo_int":
        # Aquí va tu código.
        raise NotImplementedError("Completa tipo_int en construye_nodo")

    if regla == "tipo_bool":
        # Aquí va tu código.
        raise NotImplementedError("Completa tipo_bool en construye_nodo")

    if regla == "declaracion":
        # Aquí va tu código.
        raise NotImplementedError("Completa declaracion en construye_nodo")

    if regla == "impresion":
        # Aquí va tu código.
        raise NotImplementedError("Completa impresion en construye_nodo")

    if regla == "negativo":
        # Aquí va tu código.
        raise NotImplementedError("Completa negativo en construye_nodo")

    if regla == "incremento":
        # Aquí va tu código.
        raise NotImplementedError("Completa incremento en construye_nodo")

    if regla == "decremento":
        # Aquí va tu código.
        raise NotImplementedError("Completa decremento en construye_nodo")

    if regla == "ciclo_for":
        # Aquí va tu código.
        raise NotImplementedError("Completa ciclo_for en construye_nodo")

    # 8. Detectar producciones que todavía no tienen
    #    una representación definida en el ASA.
    raise ValueError(f"Producción no reconocida: {regla}")


def desugar(arbol: ASA) -> ASA:
    """Devuelve un ASA equivalente sin incrementos, decrementos ni for."""

    # Aquí va tu código.
    raise NotImplementedError("Completa desugar en src/parser.py")
