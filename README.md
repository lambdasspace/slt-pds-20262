# Programación de Sistemas

## Semestre 2026-2

### Prácticas

* [Práctica 1: Extensión del analizador léxico para IMP++](practica01)   
  Entrega: 11 de septiembre de 2026

### Formato de entrega

Las prácticas estarán disponibles en este repositorio. Para trabajar y entregar las prácticas deberán seguir el procedimiento que corresponda.

## Configuración inicial: sólo la primera vez

**Los siguientes pasos deberán realizarse una sola vez durante el semestre. Si ya realizaron esta configuración para una práctica anterior, no deberán repetirlos.**

* Clonar el repositorio del curso:

  ```bash
  $ git clone https://github.com/lambdasspace/slt-pds-20262
  Cloning into 'slt-pds-20262'...
  ```

  y entrar al directorio correspondiente:

  ```bash
  $ cd slt-pds-20262
  ```

* Renombrar el repositorio remoto del curso como `upstream`:

  ```bash
  $ git remote rename origin upstream
  ```

* Crear un repositorio **privado** en la cuenta de una persona del equipo. Las prácticas se realizarán en equipos de una a tres personas y deberán dar acceso a todos sus integrantes.

  **Es obligatorio que el repositorio sea privado. No deberán crear repositorios públicos para las prácticas del curso.**

  Al crear el repositorio, deberán además agregar al usuario **`manu-msr`** como colaborador para que el profesor pueda acceder al código y revisar las entregas.

  En GitHub pueden hacerlo desde:

  **Settings → Collaborators → Add people → `manu-msr`**

  **Un repositorio privado al que no se haya agregado a `manu-msr` como colaborador no podrá ser revisado y, por lo tanto, se considerará como una entrega incompleta.**

* Una vez creado el repositorio privado, agregarlo como repositorio remoto `origin`:

  ```bash
  $ git remote add origin <URL_DE_SU_REPOSITORIO>
  ```

* Comprobar que ambos repositorios remotos quedaron configurados correctamente:

  ```bash
  $ git remote -v
  ```

  El repositorio del curso deberá aparecer como `upstream` y el repositorio del equipo como `origin`.

* Subir inicialmente el contenido del repositorio a su cuenta de GitHub:

  ```bash
  $ git push -u origin main
  ```

**Una vez completados estos pasos, no deberán volver a clonar el repositorio, renombrar los repositorios remotos, crear otro repositorio ni volver a agregar `origin` para las prácticas siguientes.**

## Para cada nueva práctica

**A partir de la segunda práctica deberán comenzar desde este punto. No vuelvan a realizar los pasos de configuración inicial.**

* Entrar al directorio del repositorio que ya tienen en su computadora:

  ```bash
  $ cd slt-pds-20262
  ```

* Antes de comenzar la práctica, actualizar su copia local con los cambios más recientes del repositorio del curso:

  ```bash
  $ git pull upstream main
  ```

* Completar los archivos correspondientes a la práctica. Todas las prácticas se desarrollarán utilizando **Python y Lark**.

  Pueden, y de hecho recomiendo, realizar (**commit**) cambios periódicamente para ir preservando su avance durante la escritura de la práctica:

  ```bash
  $ git add .
  $ git commit -m "Avance de la práctica"
  ```

* Completar la práctica hasta que todas las **pruebas unitarias** pasen. Para ejecutar las pruebas, desde la carpeta de la práctica utilizarán:

  ```bash
  $ python -m unittest -v
  ```

  Este comando ejecuta el conjunto de pruebas unitarias definido para la práctica.

  Todas las pruebas deberán pasar sin errores ni pruebas omitidas. Si alguna falla, deberán corregir el código y ejecutarlas nuevamente.

* Antes de realizar la entrega, ejecutar nuevamente las pruebas:

  ```bash
  $ python -m unittest -v
  ```

  y comprobar que todas pasen correctamente.

* Una vez terminada la práctica, agregar los cambios pendientes y realizar el commit correspondiente a la entrega:

  ```bash
  $ git add .
  $ git commit -m "Entrega de la práctica"
  ```

* Subir los cambios a su repositorio de GitHub:

  ```bash
  $ git push
  ```

* Comprobar directamente en GitHub que:

  * el repositorio sea **privado**;
  * el usuario **`manu-msr`** se encuentre agregado como colaborador;
  * los archivos de la práctica se encuentren correctamente actualizados;
  * el programa entregado corresponda con la versión final;
  * el commit correspondiente a la entrega se encuentre correctamente en el repositorio.

* Obtener la liga del **commit correspondiente a la entrega**. La liga tendrá una forma similar a:

  ```text
  https://github.com/usuario/repositorio/commit/abc123...
  ```

* Entregar dicha liga a través de Classroom en la actividad correspondiente.

La liga enviada deberá corresponder al commit que se considerará como la versión final de la práctica. Los cambios realizados posteriormente en el repositorio no modificarán la versión considerada para esa entrega.

**Importante:** todas las entregas deberán realizarse mediante un repositorio **privado** de GitHub al que se haya agregado al usuario **`manu-msr`** como colaborador. Es responsabilidad del estudiante verificar que el profesor tenga acceso al repositorio antes de entregar la liga en Classroom.
