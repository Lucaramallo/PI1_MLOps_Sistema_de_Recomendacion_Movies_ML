Proyecto MLOps - Operaciones de Aprendizaje Automático
¡Bienvenidos al emocionante proyecto MLOps! En este proyecto, he trabajado arduamente para abordar desafíos en el despliegue y operación de modelos de Aprendizaje Automático. He adoptado el papel de un Ingeniero de MLOps para llevar a cabo este proyecto.

video exxplicativo: https://drive.google.com/file/d/1ZfWhqqd8viU0lBHb1BoeIbYNUF6CGhuF/view?usp=sharing
enlace render (solo por 90 dias) = https://render-pi-mlops-movies-api.onrender.com/docs

Introducción
Este proyecto se centra en la creación y despliegue de un sistema de recomendación de películas utilizando un enfoque end-to-end. Desde la transformación de los datos hasta la creación de una API accesible, pasando por el análisis exploratorio y la implementación de un modelo de recomendación, cada paso ha sido cuidadosamente ejecutado para lograr los objetivos del proyecto.

Pasos del Proyecto
Transformaciones de Datos
El primer desafío fue abordar los datos en bruto. He realizado una serie de transformaciones para preparar los datos para su posterior análisis y modelado:

Desanidé los campos como "belongs_to_collection" y "production_companies", permitiendo un acceso más eficiente a los datos.
Traté los valores nulos en los campos "revenue" y "budget" al llenarlos con 0, garantizando la integridad de los datos.
Eliminé los valores nulos en el campo "release date", asegurando que solo se utilicen datos válidos.
Establecí un formato uniforme (AAAA-MM-DD) para las fechas de lanzamiento y creé una columna "release_year" para simplificar el análisis.
Calculé la columna "return" al evaluar el retorno de inversión (ROI) basado en los campos "revenue" y "budget". Cuando los datos no estaban disponibles, se estableció un valor de 0.
Finalmente, eliminé las columnas no utilizadas para mantener una estructura más limpia.
Creación de la API
He desarrollado una API utilizando el framework FastAPI para permitir el acceso a los datos y la funcionalidad del sistema de recomendación. La API incluye varias consultas que ofrecen información valiosa:

peliculas_idioma(Idioma: str): Devuelve la cantidad de películas producidas en un idioma específico.
peliculas_duracion(Pelicula: str): Proporciona la duración y el año de lanzamiento de una película dada.
franquicia(Franquicia: str): Informa sobre el recuento de películas, la ganancia total y el promedio de ganancias de una franquicia.
peliculas_pais(Pais: str): Muestra el número de películas producidas en un país determinado.
productoras_exitosas(Productora: str): Ofrece información sobre el ingreso total y la cantidad de películas producidas por una productora específica.
get_director(nombre_director): Presenta el nivel de éxito de un director junto con una lista de películas dirigidas por él, incluyendo fechas de lanzamiento, retorno individual, costo y ganancia.
Análisis Exploratorio de Datos (EDA)
Antes de construir el modelo de recomendación, realicé un análisis exploratorio de datos a mano. Exploré las relaciones entre variables, identifiqué posibles outliers y examiné patrones interesantes. Mediante gráficos y visualizaciones personalizadas, pude descubrir información relevante que impulsó la creación del modelo de recomendación.

Sistema de Recomendación
El corazón de este proyecto es el sistema de recomendación de películas. Implementé un modelo que calcula la similitud entre películas y genera recomendaciones basadas en películas similares. Esta funcionalidad se ha integrado en la API, lo que permite a los usuarios obtener recomendaciones de películas al proporcionar el título de una película.

Conclusiones
Este proyecto ha sido una inmersión completa en el mundo de las Operaciones de Aprendizaje Automático. Desde el procesamiento de datos hasta el despliegue de la API y la creación de un sistema de recomendación, cada etapa ha sido un reto gratificante. A través de este proyecto, he adquirido experiencia valiosa en la creación y operación de sistemas de ML y estoy emocionado por las oportunidades que el futuro en MLOps tiene para ofrecer.
