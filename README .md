# PI 1 -STEAM

## OBJETIVO DEL PROYECTO: 

El objetivo de este proyecto se centró en la lectura, transformación y análisis de tres bases de datos de la página de juegos 'Steam' con el objetivo de construir funciones de consultas en fast api y deployar en render.

## PARTES DEL PROYECTO
## ETL
- **EXTRACT:** Se realizó la lectura de los 3 dataset en el cual dos de ellos “review” y “item” necesitaron un tratamiento especial y una función creada para poder ser leídas ya que ambos archivos estaban corruptos.

-**EDA:** El análisis exploratorio en mi caso se realizó en primer lugar después de la extracción de los datos donde se pudo observar las columnas necesarias y datos necesarios para el proyecto, también así se observó los tipos de datos nulos y duplicados que habían.

-**TRANSFORMATION:** Después de la transformación de los datos necesarios de cada columna, descartamos columnas innecesarias, borramos duplicados y nulos que no necesitaramos y se desnido aquellas columnas que tenían una doble anidación de lista con diccionarios en su interior para extraer y colocar en columnas aparte los valores necesarias de allí para el proyecto. 

-**LOAD:** Finalmente los datasets listos se re guardaron en una carpeta aparte llamada ‘DATASETS_FIXED’ con el formato de parquet y comprimida con gz con el objetivo de reducir su tamaño y futuras lecturas, asi como tambien permitirme de esta forma guardarla en github ya que tiene un límite del tamaño de los archivos.

## FAST API Y RENDER:
-**FUNCTION FAST API:** Se construyeron 5 funciones que permiten realizar consultas a la base de datos y que posteriormente se subieron  a fast api para deployar en render.

La primera llamada **developer** en la cual se recibe un parámetro de tipo string con la desarrolladora y developer, donde devuelve la cantidad de ítems de esa desarrolladora por año y su contenido free por año también.

La segunda función llamada **UserForGenre** recibe como parámetro el dato string genero y te devuelve el usuario que acumula más horas jugadas para el género dado y una lista acumulada de horas jugadas por año de lanzamiento.

La tercera función llamada **best_developer_year** recibe como parámetro un tipo de dato entero con el año y devuelve el top desarrolladores con juegos más recomendados por usuarios para el año dado.

La cuarta función llamada **developer_reviews_analysis** recibe como dato un tipo string de una desarrolladora en la cual nos devuelve la cantidad de reseñas positivas y negativas hechas por los usuarios

Finalmente se construyo como quinta funcion relacionada al machine learning la llamada **recomendacion_juego** donde ingresamos como parametro el id de algun juego y nos devuelve 5 juegos recomendados de forma aleatoria.
