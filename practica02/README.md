# Programación de Sistemas

## Práctica 2: Extensión del analizador sintáctico para IMP++

### Fecha de entrega: 8 de octubre de 2026

La práctica es acumulativa: deben recuperar su especificación léxica de la práctica 1 y extender la gramática inicial de IMP a IMP++. Completar los atributos de los nodos del ASA, su construcción para los casos de IMP++ y la función que elimina el azúcar sintáctica. Trabajarán en el mismo equipo y repositorio de la práctica 1.

La lectura del archivo, la configuración de Lark, la entrega de tokens al parser y el recorrido para construir el ASA ya están integrados. Los casos de IMP están completos; deberán terminar los casos marcados de IMP++. El programa sigue este flujo:

```python
tokens, tabla = lexer.analiza(fuente)
asa = parser.analiza(tokens)
```

`parser.analiza` devuelve siempre el ASA desendulzado: `construye_asa` construye los nodos y llama a `desugar` antes de devolver el resultado.

Los únicos archivos que deben modificar son:

1. [`regex.lark`](src/regex.lark): copiar la especificación léxica que completaron en la práctica 1.
2. [`grammars.lark`](src/grammars.lark): extender la gramática inicial de IMP según la [EBNF requerida para IMP++](docs/gramatica_imp_mas_mas.ebnf).
3. [`asa.py`](src/asa.py): escribir los atributos de las clases de nodos proporcionadas.
4. [`parser.py`](src/parser.py): completar los casos de IMP++ marcados en `construye_nodo` y la función `desugar(arbol: ASA) -> ASA`.

*No deben modificar de ninguna manera ninguno de los otros archivos ni estructura de la práctica ni repositorio. Las pruebas las proporciona el docente y deben ejecutarse sin modificaciones.*

### Repositorio

Deberán seguir el **formato general de entrega** descrito en el repositorio.

Si ya realizaron la configuración inicial, **no deberán volver a clonar el repositorio**. Únicamente deberán entrar al directorio correspondiente y obtener la versión más reciente:

```bash
$ cd slt-pds-20262
$ git pull upstream main
```

Si es la primera vez que trabajan con el repositorio, deberán realizar primero los pasos indicados en la sección **Configuración inicial: sólo la primera vez** del formato general de entrega.

### Instalación y pruebas

Antes de comenzar, comprueben que todas las pruebas de la práctica 1 pasen. Después, copien el contenido de su archivo `practica01/src/lexico.lark` en `practica02/src/regex.lark`, que se entrega vacío.

Desde la raíz del repositorio, entren a la carpeta de la práctica y creen el entorno de Python:

```bash
$ cd practica02
$ python -m venv .venv
```

Actívenlo en Linux con:

```bash
$ source .venv/bin/activate
```

O en PowerShell con:

```powershell
.venv\Scripts\Activate.ps1
```

Instalen la dependencia y ejecuten las pruebas:

```bash
$ python -m pip install -r ../requirements.txt
$ python -m unittest -v
```

Las pruebas comprueban el resultado final de IMP++ y fallarán mientras las partes indicadas estén incompletas. Si alguna falla, corrijan los archivos permitidos y ejecuten nuevamente las pruebas. Antes de entregar, todas deberán pasar sin errores ni pruebas omitidas.

### Archivos de la práctica

```text
src/
├── regex.lark
├── grammars.lark
├── lexer.py
├── parser.py
├── asa.py
├── tabla_simbolos.py
└── compiler.py
```

#### 1. Recuperar las expresiones regulares

Completen `regex.lark` con su trabajo de la práctica 1. Debe reconocer los tokens de IMP++, incluidos `INT`, `BOOL`, `PRINT`, `FOR`, `LBRACE`, `RBRACE`, `INC` y `DEC`, los identificadores con guion bajo y los comentarios `//`. Conserven los nombres de los tokens. No es necesario modificar `lexer.py`.

#### 2. Extender la gramática

Completen las partes marcadas con `Aquí va tu código` en `grammars.lark`, siguiendo `docs/gramatica_imp_mas_mas.ebnf`. Inicialmente el archivo sólo contiene las producciones de IMP. Deben adaptarlas y añadir las de IMP++: declaraciones, tipos, impresión, bloques, incrementos, decrementos y `for`.

La gramática final usa `expresion` para expresiones aritméticas y booleanas; la comprobación de tipos se hará en otra práctica. Cada operación debe quedar entre paréntesis: `((2 + 3) * 4)`, `(2 + (3 * 4))`, `(-2)` y `(!false)`. Las llaves delimitan los cuerpos de control. Las instrucciones simples de IMP++ terminan en `;`; la gramática inicial de IMP lo utiliza como separador y deberán ajustar esa parte.

Conserven los nombres que utiliza `construye_nodo` para construir el ASA:

| Construcción | Nombre de regla o alias |
| --- | --- |
| Programa y bloque | `programa`, `bloque` |
| Datos y paréntesis | `numero`, `variable`, `verdadero`, `falso`, `parentesis` |
| Operaciones aritméticas | `suma`, `resta`, `multiplicacion`, `negativo` |
| Operaciones booleanas | `igualdad`, `menor_igual`, `negacion`, `conjuncion`, `disyuncion` |
| Comandos de IMP | `omitir`, `asignacion`, `condicional`, `mientras` |
| Extensiones | `declaracion`, `tipo_int`, `tipo_bool`, `impresion`, `incremento`, `decremento`, `ciclo_for` |
| Reglas que reúnen alternativas | `sentencia`, `actualizacion` |

Por ejemplo, una producción que reconoce una suma termina con `-> suma`. Para los tipos, usen las alternativas `INT -> tipo_int` y `BOOL -> tipo_bool`. La configuración de Lark ya usa `programa` como símbolo inicial.

#### 3. Completar los nodos del ASA

En `asa.py` ya están los nombres de las clases. Sustituyan cada comentario `Aquí va tu código` y su `pass` por los atributos correspondientes, con sus anotaciones de tipo. Conserven estos nombres y este orden, que utilizan el constructor y las pruebas:

| Clases | Atributos, en orden |
| --- | --- |
| `NUM`, `BOOL` | `valor` (entero o booleano, respectivamente) |
| `LOC`, `TIPO` | `nombre` (cadena) |
| `PLUS`, `MINUS`, `TIMES`, `EQ`, `LE`, `AND`, `OR` | `izquierda`, `derecha` (nodos ASA) |
| `NOT`, `NEG`, `PRINT` | `expresion` (nodo ASA) |
| `ASIG` | `variable` (LOC), `expresion` (ASA) |
| `SEQ` | `primero`, `segundo` (nodos ASA) |
| `IF` | `condicion`, `entonces`, `si_no` (nodos ASA) |
| `WHILE` | `condicion`, `cuerpo` (nodos ASA) |
| `PROGRAMA`, `BLOQUE` | `elementos` (lista de nodos ASA) |
| `DECL` | `tipo_declarado` (TIPO), `variable` (LOC), `expresion` (ASA) |
| `INC`, `DEC` | `variable` (LOC) |
| `FOR` | `inicio`, `condicion`, `actualizacion`, `cuerpo` (nodos ASA) |

`ASA` es la clase base y `SKIP` no necesita atributos. Conserven ambas como están. Los nodos `PROGRAMA` y `BLOQUE` conservan los elementos en su orden de aparición. `SEQ` representa dos comandos consecutivos y no introduce un bloque nuevo.

#### 4. Construir los nodos de IMP++ y eliminar el azúcar sintáctica

En `construye_nodo`, completen los casos marcados con `Aquí va tu código`: `tipo_int`, `tipo_bool`, `declaracion`, `impresion`, `negativo`, `incremento`, `decremento` y `ciclo_for`. Conserven las condiciones de cada caso y sustituyan su comentario y `raise NotImplementedError` por la construcción del nodo correspondiente. Pueden seguir los casos de IMP que ya están completos; `hijos_asa` contiene los hijos construidos en el orden de la producción.

En esta función, un incremento debe producir `INC`, un decremento `DEC` y un ciclo `for` el nodo `FOR`. La transformación se realiza después, mediante `desugar`.

Completen también `desugar` en `parser.py`. Esta función recibe un ASA y devuelve otro equivalente que ya no contiene nodos `INC`, `DEC` ni `FOR`.

- `X++` se transforma en la asignación `X := (X + 1)`.
- `X--` se transforma en la asignación `X := (X - 1)`.
- Un `for` se transforma en su inicialización seguida de un `while`. En cada vuelta se ejecutan primero el cuerpo original y después la actualización.

Recorran también los nodos interiores: puede haber incrementos y ciclos dentro de bloques, condicionales y otros ciclos. Conserven las demás operaciones, declaraciones y su orden. El cuerpo original del `for` debe mantenerse como un `BLOQUE`; la actualización va después de ese bloque en una `SEQ`, para que las variables declaradas dentro del cuerpo no cambien el alcance de la actualización. Si el árbol no tiene azúcar sintáctica, devuelvan un árbol equivalente.

La llamada ya está preparada dentro de `construye_asa`. No deben cambiar `analiza`, `construye_asa`, las partes proporcionadas de `construye_nodo` ni `compiler.py`.

### Ejecutar el compilador

Una vez completados los pendientes:

```bash
$ python src/compiler.py ejemplos/imp_mas_mas.imp
$ python -m src.compiler ejemplos/error_sintactico.imp
```

El primer comando muestra el ASA desendulzado en JSON: cada nodo incluye su `tipo` y sus atributos. No debe contener nodos `INC`, `DEC` ni `FOR`. El segundo debe informar `Error sintáctico en línea 2, columna 8: ';'` y terminar con código 1.

### Entrega

Antes de entregar deberán ejecutar nuevamente:

```bash
$ python -m unittest -v
```

y comprobar que todas pasen correctamente.

Posteriormente deberán realizar el commit correspondiente a la entrega y subirlo a su repositorio privado de GitHub:

```bash
$ git add .
$ git commit -m "Entrega de la práctica 2"
$ git push
```

Finalmente, deberán entregar en Classroom la liga al **commit correspondiente a la entrega**, siguiendo el formato general de entrega.

Recuerden que el repositorio deberá ser **privado** y que el usuario **`manu-msr`** deberá estar agregado como colaborador para que la práctica pueda ser revisada.
