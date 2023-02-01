# Proyecto AION: Backend

![Cabecera AION backend](/src/recursos/CabeceraBackend.svg)

## *El laboratorio de proyectos de ACMUD presenta*

<img align="right" width="80" height="80" src="/src/recursos/favicon.ico" alt="Icono del proyecto AION">

> **AION (backend) provee una API consumible para la recopilacion de horarios universitarios en formato JSON, con funcionalidades CRUD y posibilidad de organizar los horarios a peticion del usuario o de manera automatica a través de algoritmos de ciencias de datos.**

AION (backend) es un proyecto web que genera respuestas de objetos JSON en base a peticiones del usuario.

El usuario puede:
- Elegir una universidad a la cual acceder
- Modificar los horarios existentes almacenados para esa universidad (solo administradores y colaboradores)
- Elegir una serie de horarios basado en filtros
- Organizar los horarios basado en filtros
- Solicitar que se organicen automaticamente unos horarios basado en filtros

## Canales de comunicación

### Para ser un colaborador

(sin actualizar)

### Para reportar problemas

(sin actualizar)

### Para proponer ideas

(sin actualizar)

### Para conocer proximas actualizaciones

(sin actualizar)

## Instalación

### Requerimientos previos
- [Python (>=3.10)](https://www.python.org/downloads/): Instale Python de manera tal que sea usable en la Consola de Comandos de su sistema operativo, para esto al momento de la instalacion (o después de manera manual) deberá poner [Python en las Variables de Entorno del Sistema Operativo](https://realpython.com/add-python-to-path/)
- [Pipenv](https://pypi.org/project/pipenv/)
- [Git](https://git-scm.com/downloads): Instale Git de manera tal que sea usable en la Consola de Comandos de su sistema operativo.

### Clonando el repositorio
Antes que nada cree la carpeta en la que almacenará el repositorio, se recomienda un ruta nombrada `AION/backend`.
Para descargar el repositorio dispone de varios metodos (clonacion, descarga o solicitud de cambios). Para el tutorial se recomendara la solicitud de cambios. [Abra la Consola de Comandos en el directorio](https://www.groovypost.com/howto/open-command-window-terminal-window-specific-folder-windows-mac-linux/) y ejecute `git init`, esto inicializará el directorio como alojamiento para un repositorio local. Ejecute `git pull https://github.com/ACMUD/AION_backend main` y esto descargará el repositorio a su directorio. A continuación un gif mostrando lo escrito.

![GIF Tutorial clonacion repositorio](/guides/AION_tutorial-InstalacionClonar.gif)

### Instalando el entorno de trabajo y las dependencias
Cree un entorno de trabajo con Pipenv ejecutando `py -m pipenv --three` y luego instale las dependencias del repositorio en el entorno ejecutando `py -m pipenv install`. A continuación un gif mostrando lo escrito.

![GIF Tutorial instalacion dependencias](/guides/AION_tutorial-InstalacaionInstalar.gif)

### Configurando el aplicativo
Para poder ejecutar el aplicativo debe suministrar una URI de base de datos valida (puede ser una URI alojada en la red, en su computador con un motor de bases de datos o [en un archivo plano](https://stackoverflow.com/posts/56417062/revisions)). Para suministrar la URI debera disponer de la base de datos creada y crean un archivo JSON en [src/config](/src/config) con la forma {"host": string, "puerto": integer, "nombre_bd": string, "usuario": string, "clave": string, "motor": string}.
Para evitar errores, puede generar el archivo ejecutando los comandos ´cd src/config´, luego ´py´, lo cual abrira la consola de comandos de Python, luego ´form db import constructor_uri´ y finalmente ´constructor_uri()´, lo que creara el archivo ´db.json´ automaticamente para que introduzca allí sus credenciales de la base de datos. Entonces, ejecute en la consola `exit()` para salir de la consola de Python y `cd ../..` para volver al directorio principal. A continuación un gif mostrando lo escrito.

![GIF Tutorial configuracion base de datos](/guides/AION_tutorial-InstalacionConfigurar.gif)

### Resumen
La instalación rapida consiste en crear un directorio, abrir la Consola de Comandos en el directorio y ejecutar:

```
git init
git pull https://github.com/ACMUD/AION_backend main
py -m pipenv --three
py -m pipenv install
cd src/config
py
from db import constructor_uri
constructor_uri()
exit()
cd ../..

```

## Ejecucion
Asumiendo que se han seguido los pasos de la instalación.

### Utilizando un archivo de [arranque](/bootstrap)
Si se desea usar un archivo de arranque se debe ejecutar la Consola de Comandos en el directorio `bootstrap` del repositorio y ejecutar `cmd<bootstrap_win.txt`. A continuación un gif mostrando lo escrito.

![GIF Tutorial ejecucion arranque](/guides/AION_tutorial-EjecucionArranque.gif)

### Ejecutando por comandos
Si no se desea usar un archivo de arranque se debe ejecutar la Consola de Comandos en el directorio del repositorio. Ejecutar `py -m pipenv shell`, para activar la consola del entorno virtual, y luego `py -m src.index` para empezar la ejecucion. A continuación un gif mostrando lo escrito.

![GIF Tutorial ejecucion comandos](/guides/AION_tutorial-EjecucionDisparar.gif)

Para finalizar la ejecucion oprima `Ctrl+C` para cancelar la ejecución y ejecute `exit` para salir del entorno virtual.

### Probando el correcto funcionamiento (opcional)
Para realizar una prueba del aplicativo puede dirigirse en el navegador a la direccion `localhost:5000` o realizar una prueba con un [probador de consola](https://curl.se/download.html), como se ve en el siguiente gif.

![GIF Tutorial prueba consola](/guides/AION_tutorial-EjecucionProbar.gif)

### Tecnologias
- [Python (>=3.10)](https://www.python.org/downloads/)
  - [Pipenv](https://pypi.org/project/pipenv/)
  - [Flask](https://pypi.org/project/Flask/)
  - Otras dependencias son descritas en el archivo de [requerimientos](/requirements.txt)

## Politica sobre las ramas

(sin actualizar)

## Licencia

Este proyecto se halla licenciado bajo la **[GNU General Public License v3](/LICENSE)** [^c]

## Acerca de

### [ACMUD](https://www.acmud.cf/)

<img align="right" width="80" height="80" src="https://www.acmud.cf/static/media/logo_dark@2x.a77414011244bb13251c.png" alt="Icono del capitulo estudiantil ACMUD">

El Capitulo Estudiantil de la *Association for Computing Machine ([ACM](https://www.acm.org/))*, de la Universidad Distrital Francisco José de Caldas es una agrupación estudiantil con reconocimiento nacional e internacional que se dedica a la promoción de conocimientos de ingeniería. El grupo cuenta con ejes de interes y un laboratorio de proyectos en los cuales participan diferentes estudiantes. El Proyecto AION empezó su desarrollo dentro del laboratorio de proyectos de ACMUD y recibe colaboración de multiples personas.

### [Proyecto original (Kairos)](https://www.facebook.com/KairosUN)

<img align="right" width="80" height="80" src="/src/recursos/IconKairos1213x1280.jpg" alt="Icono del proyecto Kairos">

El Proyecto Kairos de la Universidad Nacional de Colombia (actualmente desamparado) era utilizado por estudiantes de la Universidad Nacional de Colombia y la Universidad Distrital Francisco José de Caldas para organizar sus horarios. El proyecto paró sus actualizaciones en febrero de 2020. El Proyecto AION se desarrolló con la premisa de ser el Proyecto Kairos alojado en la red y con una estructura abierta para incluir más universidades.

### Alta Lengua

<img align="right" width="80" height="80" src="https://i.pinimg.com/originals/7c/45/ed/7c45edada41d213994f17f5f26b05b67.jpg" alt="Representacion IGNOTA">

El Grupo Alta Lengua funge como colaborador del Proyecto AION.

[^c]: AION (backend) 2022 (c)
