# CSErver
Server para soportar el juego serio [CSE : Investigations](https://github.com/HexStar27/cse-investigaciones).

Versión desarrollada para usarla con docker compose.
Sirve para abstraer la configuración de mysql y nginx. Esto facilita infinítamente el despliegue.

# Instalación
Dependencias: docker (y su extensión docker compose).
Véase la documentación oficial de [Docker](https://docs.docker.com/compose/install/) para saber más sobre cómo instalarlo.

El proyecto usa un fichero .env en el directorio raiz para obtener variables que deberían ser privadas en producción. 
El repositorio contiene dicho fichero pero sin contener los datos relevantes, por lo que deberán rellenarse antes de ejecutarlo.


Tras tenerlo configurado ya solo bastaría con ejecutar el siguiente comando en el directorio raiz:
```
docker compose build
```

# Ejecución

Para ejecutarlo en la terminal:
```
docker compose up
```
Y para terminar el proceso simplemente presiona Ctrl+C y espera a que terminen de pararse los procesos.

Opcionalmente, se puede usar la opción -d (detach) para que se ejecute en segundo plano:
```
docker compose up -d
```
Para terminar el proceso, ejecuta en el mismo directorio el siguiente comando:
```
docker compose down
```

Nota: Parar la ejecución de la base de datos no hará que desaparezcan los datos gracias a los docker volumes.
(El mismo volume se puede eliminar incluyendo el parametro -v en el comando anterior)