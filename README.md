# CSErver
Server para soportar el juego serio CSE : Investigations.

# Instalación
Hace falta tener instalado node.js, npm, y mysql.

Para instalar las dependencias basta con ejecutar en consola: npm update

el proyecto usa un fichero .env para obtener variables que deberían ser privadas. Para usarlo en el proyecto descargado, añade en el mismo nivel que el resto del código un fichero ".env" con las variables necesarias.
Las variables que se usan se encuentran en los archivos authentication.js y mysql.js.

# Ejecución
El archivo principal del proyecto se llama app.js
Para ejecutarlo basta con poner en consola: node app

El programa loguea problemas que ocurren durante su funcionamiento ocupando el uso de la consola. Se recomienda crear un daemon que pase el log del programa a un fichero, así cuando deje de ejecutarse se podrá ver que ha ocurrido (en qué fecha y en qué parte del código, etc)
