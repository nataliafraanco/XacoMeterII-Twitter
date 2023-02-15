# XacoMeterII-Twitter

XacoMeterII es una aplicación web desarrollada como proyecto de fin de grado de ingeniería informática en la Universidad de Burgos. Consiste en realizar estadísticas gráficas a través de unos datos extraidos de la API de Twitter.

La aplicación se conecta a la API de Twitter, extrae los datos que se solicitan, realiza en el contenido de los tweets un análisis de sentimientos a través de la librería Sentiment-Analysis-Spanish y los inserta en una base de datos.

Para realizar las estadísticas se conecta a la base de datos, y a través de plotly muestra los datos graficamente. También se le ofrece al usuario descargar los datos del patrimonio elegido entre las fechas seleccionadas en bruto, a través de un fichero .csv. Se incluye también un gráfico analizando los sentimientos de los tweets de cada patrimonio.

## Instalación en local
Para poder utilizar la aplicación en local se necesita tener el archivo .env con las variables de entorno almacenadas, entre las que se encuentran las contraseñas de la API de Twitter y los datos de la base de datos.
Se necesita hacer uso de un entorno virtual e instalar en él todas las librerías del archivo requirements.txt.
Para crear un entorno virtual solo hace falta hacer uso del comando:

    $ python -m venv venv

Para activar el entorno:

    $ venv\Scripts\activate

Todas las librerías de Python pueden instalarse de la forma:

    $ pip install [librería]

Una vez esté preparado el entorno solo se necesita ejecutar el proyecto con:

    $ python main.py  

## Aplicación desplegada

La aplicación y la base de datos han sido desplegadas en Heroku.
Para visualizar la página web solo hay que acceder a https://tfg-nataliafranco-xacometer2.herokuapp.com/
