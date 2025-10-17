# Primer-entrega-DJANGO
Proyecto de tecnologias de desarrollo en el servidor


Para la levantar el contenedor de docker de este proyecto primero sera necesario tener instalado docker desktop. Si no es asi acceder al siguiente enlace: https://docs.docker.com/desktop/

Una vez descargado los archivos de este repositorio vamos a dirigirnos a la carpeta donde tenemos guardado nuestro proyecto, donde esta nuestro archivo docker-compose.yml

Ejecutamos en terminal el comando: docker compose build

Una vez terminada la creacion de nuetro contenedor ejecutamos el comando: docker compose up

Con eso ya tenemos nuestro contenedor creado, en caso de querer realizar instalaciones o modificaciones a los modelos es necesario ingresar por otra terminar a nuestro contenedor usando el comando: docker compose run web bash
