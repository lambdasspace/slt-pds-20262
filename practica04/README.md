# Programación de Sistemas

## Práctica 4: Generación de código C para IMP++ e integración del compilador

### Fecha de entrega: viernes 11 de diciembre de 2026

La práctica es acumulativa: deben recuperar los archivos completos de la
práctica 3, terminar el generador de C e integrar el compilador.

El flujo final es:

```text
IMP++ → lexer → parser y desazucarado → verificación de tipos → C → GCC → .out
```

Los únicos archivos que deben modificar son:

1. [`regex.lark`](src/regex.lark), [`grammars.lark`](src/grammars.lark),
   [`asa.py`](src/asa.py), [`parser.py`](src/parser.py) y
   [`verificador_tipos.py`](src/verificador_tipos.py): copiar sus versiones
   completas de la práctica 3.
2. [`generador.py`](src/generador.py): completar `NEG`, `DECL` y `PRINT`.
3. [`compiler.py`](src/compiler.py): integrar la generación de C y la llamada a
   GCC.

No modifiquen los otros archivos ni las pruebas.

Material de consulta: [correspondencias de IMP++ a
C](docs/traduccion_imp_mas_mas_a_c.md).

### Requisito: GCC

En esta práctica asumimos que tienen GCC instalado y disponible desde la
terminal. Compruébenlo antes de comenzar:

```bash
$ gcc --version
```

### Repositorio

Sigan el **formato general de entrega** descrito en el repositorio. Antes de
comenzar, actualicen la copia local:

```bash
$ cd slt-pds-20262
$ git pull upstream main
```

### Instalación y pruebas

Comprueben primero que las pruebas de la práctica 3 pasen. Después, copien a
`practica04/src/` los cinco archivos indicados arriba.

Desde la raíz del repositorio:

```bash
$ cd practicas/github/practica04
$ python -m venv .venv
$ source .venv/bin/activate
$ python -m pip install -r ../requirements.txt
$ python -m unittest -v
```

En PowerShell, activen el entorno con:

```powershell
.venv\Scripts\Activate.ps1
```

Las pruebas de las fases anteriores deben pasar después de recuperar la
práctica 3. Las nuevas fallarán mientras el generador y la integración estén
incompletos.

### Archivos de la práctica

```text
docs/
├── gramatica_imp_mas_mas.ebnf
├── reglas_tipos_imp_mas_mas.pdf
└── traduccion_imp_mas_mas_a_c.md
ejemplos/
src/
├── generador.py
├── compiler.py
└── archivos de las fases anteriores
tests/
```

#### 1. Recuperar el compilador de la práctica 3

Copien los cinco archivos indicados. `parser.analiza` debe seguir devolviendo
el ASA desazucarado y `verificador_tipos.verifica` debe comprobarlo antes de la
generación.

El generador no recibe nodos `INC`, `DEC` ni `FOR`: `++`, `--` y `for` ya deben
haber sido traducidos a formas básicas.

#### 2. Completar el generador

En [`generador.py`](src/generador.py), completen los casos marcados:

- `NEG`: traducir el menos unario.
- `DECL`: emitir la asignación que inicializa la variable.
- `PRINT`: elegir la impresión según el tipo de la expresión.

La traducción usa estas convenciones:

- `int` se representa con `long long` y `bool` con `bool` de `stdbool.h`;
- los identificadores reciben el prefijo `imp_`;
- las variables se declaran al inicio de `main`;
- los enteros se imprimen con `%lld` y una conversión a `long long`;
- los booleanos se imprimen como `true` o `false`.

#### 3. Integrar el compilador

En [`compiler.py`](src/compiler.py), completen los dos pasos marcados:

1. En `compilar`, llamar al generador solamente si la verificación de tipos es
   válida.
2. En `compilar_archivo`, escribir el archivo `.c` y llamar a
   `invocar_gcc` para producir el ejecutable `.out`.

La función `invocar_gcc` ya está proporcionada y ejecuta el equivalente de:

```bash
$ gcc -std=c11 -Wall -Wextra -pedantic programa.c -o programa.out
```

Si una fase anterior falla, no se debe llamar a GCC. Si GCC rechaza el código,
se conserva el archivo `.c` para revisar el diagnóstico.

### Ejecutar el compilador

```bash
$ python -m src.compiler ejemplos/imp_mas_mas.imp -o programa.out
$ ./programa.out
```

Si omiten `-o`, se utiliza el nombre del archivo fuente con extensión `.out`.
La compilación correcta conserva tanto `programa.c` como `programa.out`.

La salida esperada del ejemplo es:

```text
0
1
2
3
-2
true
```

### Entrega

Antes de entregar, ejecuten nuevamente:

```bash
$ python -m unittest -v
```

Después realicen el commit y súbanlo a su repositorio privado:

```bash
$ git add .
$ git commit -m "Entrega de la práctica 4"
$ git push
```

Entreguen en Classroom la liga al **commit correspondiente a la entrega**. El
repositorio debe ser privado y el usuario **`manu-msr`** debe estar agregado
como colaborador.
