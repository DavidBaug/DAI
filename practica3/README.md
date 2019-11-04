# Práctica 3

##### David Gil Bautista
##### [Mail](mailto:davidbautista@correo.ugr.es)

#### Inicio del contenedor y prueba

En este directorio abre una terminal y ejecuta `docker-compose up flask` para ejecutar el contenedor.

Una vez esté corriento entra a tu navegador de confianza e introduce la siguiente dirección: [127.0.0.1:8080](127.0.0.1:8080)

Podemos ver la página principal del sitio web con un submenú para navegar por las distintas secciones y una cabecera con el logo y un formulario de login.

#### Plantillas

Uso una plantilla genérica para mostrar el contenido genérico del sitio web y una serie de páginas adicionales para almacenar la información del cuerpo. He optado por almacenar toda la información "dinámica" en la plantilla, lo que nos permite guardar un contenido estático en el cuerpo de la página.

#### PickleShareDB

Nos permite crear nuevos usuarios y modificar la información de los mismos.

#### Historial

Para el historial tenemos que tener en cuenta que el usuario haya iniciado sesión, una vez hecho esto guardamos las páginas visitadas en un array de 3 posiciones en el que vamos añadiendo al comienzo la última página visitada y desplazando las anteriores.
