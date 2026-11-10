# Programación de Sistemas

## Práctica 3: Verificador de tipos para IMP++

### Fecha de entrega: lunes 16 de noviembre de 2026

La práctica es acumulativa: deben recuperar los archivos que completaron en la
práctica 2 e implementar las reglas de tipos de IMP++ sobre el **ASA
desazucarado**. El verificador se conserva como un módulo independiente para
integrarlo con la generación de código en la práctica 4.

El compilador sigue este flujo:

```python
tokens, tabla_lexica = lexer.analiza(fuente)
asa = parser.analiza(tokens)          # ASA ya desazucarado
resultado = verificador_tipos.verifica(asa)
```

Los únicos archivos que deben modificar son:

1. [`regex.lark`](src/regex.lark), [`grammars.lark`](src/grammars.lark),
   [`asa.py`](src/asa.py) y [`parser.py`](src/parser.py): copiar sus versiones
   completas de la práctica 2.
2. [`verificador_tipos.py`](src/verificador_tipos.py): completar los casos de
   IMP++ indicados en el recorrido.

No deben modificar los otros archivos ni la estructura de la práctica.

Material de consulta: [reglas formales de tipos para
IMP++](docs/reglas_tipos_imp_mas_mas.pdf).

### Repositorio

Deberán seguir el **formato general de entrega** descrito en el repositorio.
Antes de comenzar, actualicen la copia local que utilizaron en las prácticas
anteriores:

```bash
$ cd slt-pds-20262
$ git pull upstream main
```

### Instalación y pruebas

Comprueben primero que las pruebas de la práctica 2 pasen. Después, copien a
`practica03/src/` sus versiones completas de `regex.lark`, `grammars.lark`,
`asa.py` y `parser.py`.

Desde la raíz del repositorio, entren a la carpeta y creen el entorno:

```bash
$ cd practica03
$ python -m venv .venv
```

Actívenlo en Linux:

```bash
$ source .venv/bin/activate
```

O en PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instalen la dependencia y ejecuten las pruebas:

```bash
$ python -m pip install -r ../requirements.txt
$ python -m unittest -v
```

Las pruebas de IMP deben pasar con el recorrido proporcionado. Las de IMP++
fallarán mientras los casos indicados estén incompletos.

### Archivos de la práctica

```text
docs/
├── gramatica_imp_mas_mas.ebnf
├── reglas_tipos_imp_mas_mas.tex
└── reglas_tipos_imp_mas_mas.pdf
src/
├── regex.lark
├── grammars.lark
├── lexer.py
├── parser.py
├── asa.py
├── tabla_simbolos.py
├── verificador_tipos.py
└── compiler.py
```

#### 1. Recuperar el ASA desazucarado de la práctica 2

Copien los cuatro archivos indicados desde su práctica 2. Su función
`parser.analiza` debe continuar construyendo el ASA y aplicando `desugar` antes
de devolverlo. Las pruebas de desazucarado comprueban esta precondición de la
práctica.

No trasladen el azúcar sintáctico al verificador: por ejemplo, `X++` llega como
una asignación con una suma y un `for` llega como una secuencia seguida de un
`while`. El verificador sólo aplica reglas a ese resultado.

#### 2. Contexto de tipos proporcionado

`TablaTipos` representa el contexto finito \(\Gamma\) que asocia identificadores
con `int` o `bool`. Antes de comprobar los nodos, el código proporcionado
registra las declaraciones explícitas en ese único contexto. Los identificadores
de IMP que no tienen declaración explícita conservan el tipo implícito `int`.

Los nodos `BLOQUE` únicamente agrupan comandos y se recorren en orden. En esta
práctica no se implementan pilas de contextos, niveles, ocultamiento ni búsqueda
entre regiones anidadas.

#### 3. Completar el verificador de tipos

En [`verificador_tipos.py`](src/verificador_tipos.py), completen solamente los
casos marcados:

- `EQ` acepta dos operandos del mismo tipo, ya sea `int` o `bool`, y produce
  `bool`.
- `NEG` requiere una expresión `int` y produce `int`.
- `DECL` comprueba que el inicializador tenga el tipo declarado. La asociación
  del identificador con su tipo ya fue incorporada a \(\Gamma\) por el código
  proporcionado.
- `PRINT` acepta una expresión `int` o `bool`.

El recorrido proporcionado ya implementa las reglas de IMP para literales,
identificadores, operaciones, asignaciones, secuencias, condicionales y ciclos.
Sigan esa estructura y las reglas del PDF. Los errores de una expresión deben
propagarse con `Tipo.ERROR` sin producir diagnósticos repetidos; `Tipo.ERROR` es
una marca de la implementación, no un tipo del lenguaje formal.

No modifiquen `_registrar_declaraciones`: esa pasada únicamente prepara
\(\Gamma\) y detecta identificadores declarados más de una vez. No forma parte
del ejercicio evaluado.

### Ejecutar el compilador

```bash
$ python src/compiler.py ejemplos/imp_mas_mas.imp
$ python -m src.compiler ejemplos/error_tipos.imp
```

El primer comando debe mostrar el ASA desazucarado y su contexto de tipos. El
segundo debe informar los errores semánticos y terminar con código 1.

### Entrega

Antes de entregar, ejecuten nuevamente:

```bash
$ python -m unittest -v
```

Después realicen el commit y súbanlo a su repositorio privado:

```bash
$ git add .
$ git commit -m "Entrega de la práctica 3"
$ git push
```

Finalmente, entreguen en Classroom la liga al **commit correspondiente a la
entrega**, siguiendo el formato general. El repositorio debe ser privado y el
usuario **`manu-msr`** debe estar agregado como colaborador.
