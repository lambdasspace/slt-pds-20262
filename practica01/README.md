# Programación de Sistemas

## Práctica 1: Extensión del analizador léxico para IMP++

### Fecha de entrega: viernes 11 de septiembre de 2026

Deben completar las reglas léxicas faltantes de [lexico.lark](src/lexico.lark) para extender el analizador de IMP a IMP++, conservando el reconocimiento de IMP básico. Deberán ampliar los identificadores y agregar comentarios, palabras reservadas, llaves y operadores de incremento y decremento, según los pendientes indicados en el archivo.

Para consultar las construcciones del lenguaje base, pueden revisar [la descripción de IMP](docs/descripcion_imp.pdf).

El analizador proporcionado conserva los mismos módulos e interfaz de IMP01: produce los tokens y la tabla de localidades. La extensión a IMP++ se realiza en la especificación léxica.

El único archivo que deben modificar es:

- [`lexico.lark`](src/lexico.lark) con la especificación léxica de IMP++.

*No deben modificar de ninguna manera ninguno de los otros archivos ni estructura de la práctica ni repositorio.*

### Repositorio

Deberán seguir el **formato general de entrega** descrito en el repositorio.

Si ya realizaron la configuración inicial, **no deberán volver a clonar el repositorio**. Únicamente deberán entrar al directorio correspondiente y obtener la versión más reciente:

```bash
$ cd slt-pds-20262
$ git pull upstream main
```

Si es la primera vez que trabajan con el repositorio, deberán realizar primero los pasos indicados en la sección **Configuración inicial: sólo la primera vez** del formato general de entrega.

### Instalación y pruebas

Desde la raíz del repositorio, entren a la carpeta de la práctica y creen el entorno de Python:

```bash
$ cd practica01
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

Instalen la dependencia:

```bash
$ python -m pip install -r requirements.txt
```

Para ejecutar el analizador y mostrar los tokens y la tabla de localidades:

```bash
$ python -m src.lexer ejemplos/imp_base.imp
```

Una vez terminado el trabajo correspondiente a la práctica, deberán comprobar que todas las pruebas unitarias pasan correctamente al ejecutar:

```bash
$ python -m unittest -v
```

Este comando ejecuta el conjunto de pruebas definido para la práctica. Las pruebas de IMP básico pasan desde el inicio; las de IMP++ fallarán hasta que completen la extensión.

Todas las pruebas deberán pasar sin errores ni pruebas omitidas. Si alguna falla, corrijan `src/lexico.lark` y ejecuten nuevamente las pruebas.

### Archivos de la práctica

Deberán modificar **únicamente el archivo indicado explícitamente para esta práctica**. No deberán modificar de ninguna manera `src/lexer.py`, los archivos de pruebas ni otros archivos proporcionados como parte de la infraestructura de la práctica, salvo que las instrucciones indiquen lo contrario.

### Entrega

Antes de entregar deberán ejecutar nuevamente:

```bash
$ python -m unittest -v
```

y comprobar que todas las pruebas pasen correctamente.

Posteriormente deberán realizar el commit correspondiente a la entrega y subirlo a su repositorio privado de GitHub:

```bash
$ git add .
$ git commit -m "Entrega de la práctica 1"
$ git push
```

Finalmente, deberán entregar en Classroom la liga al **commit correspondiente a la entrega**, siguiendo el formato general de entrega.

Recuerden que el repositorio deberá ser **privado** y que el usuario **`manu-msr`** deberá estar agregado como colaborador para que la práctica pueda ser revisada.
