# ipm-practica-1
Práctica 1 de la asignatura de IPM.Aplicación básica cliente/servidor con interfaz cliente en python3

Se implementa una aplicación básica cliente/servidor desarrollada con el lenguaje de programación Python3.

El servidor se desarrolla en Flask y expondrá una API para el cliente. La API devolverá una lista de canciones (título, url y fav) organizada por sus intervalos.

El servidor ofrece una API de tipo RESTFULL con las respuestas en formato JSON. La API tiene dos endpoints:

    /intervals: Devuelve una lista de intervalos y los tonos entre los intervalos
    /songs//<asc_des>: Devuelve una lista de canciones para un intervalo dado en un orden especificado

El Cliente recupera la información de la API y muestra la información recuperada, además de permitir abrir la URL seleccionada en el navegador. La interfaz de cliente utiliza Gtk+ y el protocolo At-spi. La aplicación cambia la notación para los siguientes locales:

    es_ES.utf8
    en_US.utf8

Se incluye documentación y ficheros de test.
