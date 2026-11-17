# Correspondencias de IMP++ a C

Este documento fija la salida que deben producir los casos incompletos del
generador. Describe el resultado; no prescribe una solución en Python.

## Contrato de entrada

El generador recibe:

- un ASA desazucarado;
- una verificación semántica correcta;
- la tabla plana de tipos construida por la práctica 3.

Si la verificación contiene errores, el generador no debe ejecutarse.

## Unidad de traducción

El resultado es un programa C11 con esta forma general:

~~~c
#include <stdbool.h>
#include <stdio.h>

int main(void) {
    /* declaraciones obtenidas de la tabla de tipos */
    /* traducción del programa */
    return 0;
}
~~~

Los identificadores del programa fuente reciben el prefijo **imp_**. Así se
evita que un nombre como **main** choque con el punto de entrada de C.

| Tipo de IMP++ | Representación en C | Valor inicial |
| --- | --- | --- |
| int | long long | 0 |
| bool | bool | false |

## Expresiones

| Nodo del ASA | Forma de C |
| --- | --- |
| NUM(n) | n |
| BOOL(true) | true |
| BOOL(false) | false |
| LOC(X) | imp_X |
| PLUS(E1,E2) | (E1 + E2) |
| MINUS(E1,E2) | (E1 - E2) |
| TIMES(E1,E2) | (E1 * E2) |
| EQ(E1,E2) | (E1 == E2) |
| LE(E1,E2) | (E1 <= E2) |
| NOT(E) | (!E) |
| AND(E1,E2) | (E1 && E2) |
| OR(E1,E2) | (E1 \|\| E2) |
| NEG(E) | (-E) |

Cada aparición de E, E1 o E2 representa la traducción recursiva de la
subexpresión correspondiente.

## Comandos

Las asignaciones, secuencias, condicionales y ciclos siguen las
correspondencias del IMP básico desarrollado en clase.

### Declaración

Todas las variables se declaran al inicio de **main** con la información de la
tabla de tipos. Cuando el recorrido encuentra:

~~~text
DECL(TIPO("int"), LOC("cantidad"), E)
~~~

debe emitir en ese punto la inicialización:

~~~c
imp_cantidad = E;
~~~

La misma regla se aplica a una declaración booleana. No se vuelve a escribir el
tipo porque la declaración de C ya fue preparada al inicio de **main**.

### Impresión

Para una expresión entera E:

~~~c
printf("%lld\n", (long long)(E));
~~~

Para una expresión booleana E:

~~~c
printf("%s\n", E ? "true" : "false");
~~~

El formato `%lld` corresponde a `long long`. La conversión explícita evita que
`printf` reciba por accidente un `int`, por ejemplo cuando la expresión es un
literal o una negación. En C, el formato y el tipo del argumento deben
coincidir. Cada impresión termina con un salto de línea.

### Programa y bloque

**PROGRAMA** y **BLOQUE** recorren sus elementos de izquierda a derecha. Esta
práctica conserva el contexto plano de tipos de la práctica 3; un bloque no
introduce una tabla nueva durante la generación.

## Formas que no recibe el generador

No se definen correspondencias para **INC**, **DEC** ni **FOR**. El parser debe
haberlas transformado antes:

- incremento y decremento se vuelven asignaciones;
- for se vuelve una secuencia con un while.

Recibir cualquiera de esos nodos indica que no se respetó el contrato entre las
fases.

## Producto final

El texto C es una representación intermedia visible. **compiler.py** debe
guardarlo y llamar después a GCC:

~~~bash
gcc -std=c11 -Wall -Wextra -pedantic programa.c -o programa.out
~~~

La compilación completa tiene éxito únicamente cuando GCC termina con código
cero y existe el archivo **programa.out**.
