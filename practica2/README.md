# Práctica 2

##### David Gil Bautista
##### [Mail](mailto:davidbautista@correo.ugr.es)

#### Inicio del contenedor y prueba

En este directorio abre una terminal y ejecuta `docker-compose up flask` para ejecutar el contenedor.

Una vez esté corriento entra a tu navegador de confianza e introduce la siguiente dirección: [127.0.0.1:8080](127.0.0.1:8080)

Aparece un mensaje de Hola mundo.

Distintos ejercicios

#### Manejo de URLS + Contenidos estáticos

Entra a la siguiente dirección: [127.0.0.1:8080/user/tu_nombre](127.0.0.1:8080/user/tu_nombre) y deberías ver un mensaje personalizado con el nombre escogido y una imagen.

#### Para Nota 1

Entra a la siguiente dirección: [127.0.0.1:8080/mandelbrot](127.0.0.1:8080/mandelbrot) y se te pedirán una serie de datos que se usarán para generar una imagen fractal.

#### Para Nota 2

Entra a la siguiente dirección: [127.0.0.1:8080/svg](127.0.0.1:8080/svg) y se generarán automáticamente 3 figuras vectoriales con datos aleatorios. En cada petición las figuras cambian y no se almacenan estáticamente en ningún directorio.


#### Información adicional

Para el desarrollo de esta práctica se han usado templates con el fin de agilizar el proceso de obtención de datos del usuario y no saturar el programa principal añadiendo código HTML.
