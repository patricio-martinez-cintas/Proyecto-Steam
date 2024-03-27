# <p align="center">**Proyecto Steam**</p>

<p align="center">
  <img src="/Recursos/Steam.png" alt="Steam logo">
</p>

## OBJETIVO DEL PROYECTO: 

El objetivo principal de este proyecto fue desarrollar funciones específicas para trabajar con la base de datos de Steam. Estas funciones se enfocaron en proporcionar recomendaciones y datos clave sobre los juegos de la plataforma Steam. Todo esto fue diseñado para ser integrado en FastAPI y luego desplegado en Render.

## PARTES DEL PROYECTO

**EDA:** 
Se realizó un análisis exploratorio de los datos de los 3 conjuntos de datos, en el cual dos de ellos, "review" y "item", requirieron un tratamiento especial y la creación de una función para poder ser leídos, ya que ambos archivos estaban corruptos. Estas bases de datos fueron guardadas en nuevos archivos en formato Parquet y comprimidos en formato gzip para mejorar su lectura para el ETL. Además, se exploró información importante de los 3 conjuntos de datos, como el número de duplicados, outliers, la cantidad de columnas y filas, los tipos de variables, valores nulos, entre otros aspectos relevantes.

+ [EDA link](/EDA/EDA.ipynb)


**ETL:** Se realizaron las transformaciones necesarias en las tres bases de datos, manteniendo únicamente los valores relevantes para la realización del proyecto. Posteriormente, se guardaron estas bases de datos finales para su uso en las funciones del proyecto.

+ [EDA link](/ETL/ETL.ipynb)


**CREACIÓN DE LAS FUNCIONES:** Se construyeron 5 funciones que permiten realizar consultas a la base de datos y que posteriormente se subieron a fast api para deployar en Render. 

+ [Funciones link](/Funciones%20fastapi/Function_api.ipynb)

Estas funciones son:

+ **`developer:`** Esta función recibe como parámetro el desarrollador en formato str y devuelve un diccionario con la cantidad de items por año y el porcentaje de juegos free que hay en cada año.

+ **`UserForGenre:`** Esta función recibe como parámetro el género en str de un juego y devuelve el usuario que ha jugado más horas en ese género, junto con las horas jugadas por ese usuario en ese género a lo largo de los años.

+ **`sentiment_analysis:`** Esta función recibe como parámetro la empresa desarrolladora de tipo str y devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento positivo o negativo como valor.

+ **`game_recommendation:`** Esta función recibe como parámetro la ID de un juego en formato int y devuelve 5 juegos aleatorios recomendables si encuentra la ID en el sistema, y 5 juegos aleatorios si no la encuentra.

+ **`best_developer_year:`** Esta función recibe como parametro el str año y devuelve el top 3 de desarrolladoras con juegos mas recomendados por usuarios para el año dado.


**FAST API Y RENDER:** Se creo el entorno vitual para fastapi y se construyo el main.py necesario para usar las funciones.

+ [Fastapi main link](/main.py)

Finalmente se uso Render para deployar fastapi en una página web.
