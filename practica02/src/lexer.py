"""Reconoce los tokens del programa y construye la tabla de símbolos."""

from pathlib import Path
from lark import Lark, Token
if __package__:
    from .tabla_simbolos import TablaSimbolos
else:
    from tabla_simbolos import TablaSimbolos


def analiza(fuente: str) -> tuple[list[Token], TablaSimbolos]:
    """Recibe el programa como texto y devuelve (tokens, tabla de símbolos)."""
    
    # 1. Obtener la ruta del módulo del lexer
    archivo_lexer = Path(__file__)

    # 2. Obtener la ruta del archivo con las expresiones regulares
    archivo_regex = archivo_lexer.with_name("regex.lark")
    
    # 3. Leer las expresiones regulares
    reglas = archivo_regex.read_text(encoding="utf-8")

    if not reglas.strip():
        raise NotImplementedError("Completa src/regex.lark con tu especificación de la práctica 1")
    
    # 4. Construir el analizador léxico
    analizador = Lark(
        reglas,
        parser=None,
        lexer="basic", # toma el texto y va escogiendo los tokens de acuerdo con las 
                       # expresiones regulares definidas en reglas
        propagate_positions=True # hace que Lark conserve información sobre dónde 
                                 # apareció cada elemento en el texto, como línea, 
                                 # columna y posiciones inicial/final.
    )
    
    # 5. Obtener tokens y convertirlos en lista
    tokens = list(analizador.lex(fuente))
    
    # 6. Construir la tabla de símbolos
    tabla = TablaSimbolos()
    
    # 8. Registrar los identificadores correspondientes
    for token in tokens:
        tipo = token.type

        if tipo == "LOC":
            tabla.registrar(token)

    # 9. Devolver el resultado del análisis léxico
    return tokens, tabla
