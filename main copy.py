
# Para arrancar un fastapi:

""""
Dentro de la carpeta, localizada para Fast API crear un entorno virtual dentro de la misma (debe abrirce desde consloa de comandoos cmp * clic derecho abrir en terminal

alli ejecutar 
$ python3 -m venv fastapi-env 

creo el entorno luego lo arranco con:
$ fastapi-env\Scripts\activate.bat

me meto dentro del entorno #p windows
$ cd .\fastapi-env\


intalo libs:
$ pip install fastapi
$ pip install uvicorn

por si las dudas tmb:
$ pip install uvicorn[standard]

ahora creo dentro del entorno virtual el archivo main.py desde visual que contenga lo siguiente segun la instalacion de fastapi:


***
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

***
y por ultimo ejecuto: 
$ python -m uvicorn main:app --reload


salida:

INFO:     Waiting for application startup.
INFO:     Application startup complete.

render: https://www.youtube.com/watch?v=920XxI2-MJ0
web service 
Start Command: uvicorn main:app --host 0.0.0.0 --port 10000
"""

import pickle
from typing import Union
from fastapi import FastAPI
from typing import Dict
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from pydantic import BaseModel

 # Cargar el archivo pickle en un DataFrame
# df_merged = pd.read_pickle('../../Datasets/Datasets_cleaned_ETL/Combinado_merged_movies_ratings/df_merged.pkl')
# df_merged = pd.read_pickle('./Datasets/Datasets_cleaned_ETL/Combinado_merged_movies_ratings/df_merged.pkl')

# with open('../PI-1---REINTENTO/df_merged.pkl') as file:
#     df_merged = pickle.load(file)

df_merged = pd.read_csv('./df_merged.csv')

app = FastAPI()

#_________________________________________________________________________________________

# Docs: http://127.0.0.1:8000/docs#/

# Ruta: http://127.0.0.1:8000/
@app.get("/") # decorador cuando alguien cosulta la ruta"/" eecuta la funcion
def read_root():
    return {"Hello": "World"}

# Ruta: http://127.0.0.1:8000/Libros/5?q=somequery
@app.get("/Libros/{item_id}") # para consultas con variables ej librio n°1 ,2,3,4...
def read_item(item_id: int):
    return {"libro n°:": item_id}

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
#____________________________________________________________________________________________________

# Funcion 1:
# Ruta: http://127.0.0.1:8000/get_max_duration/2021/{plataform}/min?platform=aws

@app.get("/get_max_duration/{year}/{plataform}/{duration_type}")
def get_max_duration(year: int, platform: str, duration_type: str):
    """get_max_duration of...### Funcion 1:

    #### Película (sólo película, no serie, etc)
    con mayor duración según año, plataforma y tipo de duración.
    La función debe llamarse get_max_duration(year, platform, duration_type) y 
    debe devolver sólo el string del nombre de la película.

    Args:
        year (int): 
        platform (str): 
        duration_type (str): 

    Returns:
        output_dict = {
        'plataforma': platform,
        'tipo_duracion': duration_type,
        'año': year,
        'titulo': max_duration_movie
    """
    # Filtrar el DataFrame para incluir solo las películas
    movies_df = df_merged[df_merged['type'] == 'movie']

    # Filtrar por año, plataforma y tipo de duración
    filtered_df = movies_df[(movies_df['release_year'] == year) & 
                            (movies_df['plataforma'] == platform) &
                            (movies_df['duration_type'] == duration_type)]
    
    # Verificar si el DataFrame filtrado está vacío
    if filtered_df.empty:
        return "No se encontraron películas que cumplan con los criterios especificados."
    
    # Obtener el título de la película con la duración máxima
    max_duration_movie = filtered_df.loc[filtered_df['duration_int'].idxmax(), 'title']
    
    return {'plataforma': platform,
        'tipo_duracion': duration_type,
        'año': year,
        'titulo': max_duration_movie}


#____________________________________________________________________________________________________



# Funcion 2:
# Ruta: http://127.0.0.1:8000/get_score_count/netflix/3.5/2021

@app.get("/get_score_count/{plataforma}/{scored}/{anio}")
def get_score_count(plataforma: str, scored: float, anio: int) -> str:
    """get_score_count: ### Funcion 2:
    #### Cantidad de películas (sólo películas, no series, etc) según plataforma, 
    con un puntaje mayor a XX en determinado año. La función debe llamarse get_score_count(platform, scored, year) 
    y debe devolver un int, con el total de películas que cumplen lo solicitado.

    Args:
        plataforma (str): netflix, hulu, disney plus, aws
        scored (float): puntaje por encima de...
        anio (int): year/n

    Returns:
        output_dict = {
        'plataforma': plataforma,
        'cantidad': count,
        'anio': anio,
        'score': scored
    }
    """
    
    # Filtrar sólo las películas del año y plataforma solicitados
    movies2 = df_merged[(df_merged['plataforma'] == plataforma) & 
                       (df_merged['type'] == 'movie') &
                       (df_merged['release_year'] == anio)]

    # Contar las películas que cumplen con el puntaje mínimo
    count = (movies2['prom_rating'] >= scored).sum()
    
    
    return {'Cantidad de peliculas': {count}, 'puntajes mayores a' : {scored}, 'para el anio': {anio}}
#____________________________________________________________________________________________________

# Funcion 3:
# Ruta: http://127.0.0.1:8000/get_count_platform/netflix

@app.get("/get_count_platform/{plataforma}")
def get_count_platform(plataforma: str):
    """get_count_platform:
    ### Funcion 3:
    #### Cantidad de películas (sólo películas, no series, etc) según plataforma. 
    La función debe llamarse get_count_platform(platform) y debe devolver un int, con el número total de películas de esa plataforma.
     Las plataformas deben llamarse amazon, netflix, hulu, disney.

    Args:
        plataforma (str): netflix, hulu, disney plus, aws

    Returns:
        int: Cantidad de peliculas 
    """
    platform_df = df_merged[df_merged['type'] == 'movie']
    respuesta = len(platform_df[platform_df['plataforma'] == plataforma])
    
    return {respuesta, plataforma}

#____________________________________________________________________________________________________


# Funcion 4:
# Ruta: http://127.0.0.1:8000/get_actor/netflix/2016
@app.get("/get_actor/{plataforma}/{anio}")
def get_actor(plataforma: str, anio: int):
    """get_actor:
    ### Funcion 4:
    #### Actor que más se repite según plataforma y año. 
    La función debe llamarse get_actor(platform, year) y debe devolver sólo el string con el nombre 
    del actor que más se repite según la plataforma y el año dado.

    Args:
        plataforma (str): netflix, aws, hulu, disney plus
        anio (int): "2016", por ej,

    Returns:
        return: most_frequent_actor, plataforma, anio
    """
    # obtener los datos para la plataforma y el año dado
    platform_data = df_merged[df_merged['plataforma'] == plataforma]
    year_data = platform_data[platform_data['release_year'] == anio]

    # dividir los actores en una lista
    year_data['actors_list'] = year_data['cast'].str.split(',')

    # crear una columna con la cantidad de actores en cada fila
    year_data['num_actors'] = year_data['actors_list'].apply(len)

    # obtener todos los actores en un solo conjunto
    all_actors = set()
    for actors in year_data['actors_list']:
        all_actors.update(actors)

    # crear un diccionario para contar la frecuencia de aparición de cada actor
    actor_counts = {actor: 0 for actor in all_actors}
    for actors in year_data['actors_list']:
        for actor in actors:
            actor_counts[actor] += 1

    # obtener el actor que aparece con mayor frecuencia
    most_frequent_actor = max(actor_counts, key=actor_counts.get)
    max_count = actor_counts[most_frequent_actor]

    # si el actor más frecuente es 'unknown', buscar el siguiente actor con mayor apariciones
    if most_frequent_actor == 'unknown':
        del actor_counts['unknown']
        most_frequent_actor = max(actor_counts, key=actor_counts.get)
        max_count = actor_counts[most_frequent_actor]

    return {'most_frequent_actor': most_frequent_actor,'plataforma': plataforma, 'anio': anio, 'cantidad de apariciones': max_count}

#____________________________________________________________________________________________________


# Funcion 5:
# Ruta: http://127.0.0.1:8000/prod_per_county/movie/united%20states/2000

@app.get("/prod_per_county/{tipo}/{pais}/{anio}")
def prod_per_county(tipo: str, pais: str, anio: int):
    """prod_per_county:
    ### Funcion 5:
    #### La cantidad de contenidos/productos (todo lo disponible en streaming) que se publicó por país y año. 
    La función debe llamarse prod_per_county(tipo,pais,anio) deberia devolver el tipo de contenido (pelicula,serie) por pais y 
    año en un diccionario con las variables llamadas 'pais' (nombre del pais), 'anio' (año), 'pelicula' (tipo de contenido).

    Args:
        tipo (str): movie, tv-show, serie, documental...etc
        pais (str): country
        anio (int): 2020 por ej,

    Returns:
        return: {'pais': pais, 'anio': anio, 'peliculas': respuesta}
    """
    # filtrar los datos según el tipo de contenido, país y año
    df_filt = df_merged[(df_merged['type'] == tipo) & (df_merged['country'] == pais) & (df_merged['release_year'] == anio)]
    # contar el número de filas
    respuesta = len(df_filt)
    # crear un diccionario con los resultados y devolverlo    
    return {'pais': pais, 'anio': anio, 'cantidad de peliculas publicadas': respuesta}


#____________________________________________________________________________________________________


# Funcion 6:
# Ruta: http://127.0.0.1:8000/get_contents/tv-14

@app.get("/get_contents/{rating}")
def get_contents(rating: str):
    # Filtrar el DataFrame por el rating de audiencia dado
    contents = df_merged[df_merged['rating_x'] == rating]
    # Obtener el número total de contenidos
    num_contents = contents.shape[0]
    # Devolver una respuesta en formato JSON
    respuesta = {'rating_x': rating, 'num_contents': num_contents}
    return {'rating_x': rating, 'cantidad de contenido': num_contents}
#____________________________________________________________________________________________________

# Funcion 7:
# Ruta: http://127.0.0.1:8000/get_recomendation/school%20of%20rock/50
@app.get("/get_recomendation/{title}/{cantidad_recomendaciones}")
def get_recommendation(title: str, cantidad_recomendaciones: int):
    """get_recommendation
        Éste consiste en recomendar películas a los usuarios basándose en películas similares,
         por lo que se debe encontrar la similitud de puntuación entre esa película y el resto de películas, 
         se ordenarán según el score y devolverá una lista de Python con 5 valores, cada uno siendo el string del nombre de las películas 
         con mayor puntaje, en orden descendente. Debe ser deployado como una función adicional de la API anterior 
         y debe llamarse get_recommendation(titulo: str)
    Args:
        title (str): titulo de pelicula a tomar como referencia, ejemplo: toy story
        cantidad_recomendaciones (int): cantidad de peliculas similares que quiero recibir como recomendaciones

    Returns:
        return : listado de peliculas recomendadas segun peticion, con su porcentaje de similitud coseno, indicando que tan similar en los topicos según
        la pelicula referencia.
    """
    try:
        # Seleccionar las columnas relevantes para el cálculo del coseno
        columns_for_similarity = df_merged.columns[17:]

        # Calcular la matriz de similitud del coseno
        cosine_sim_matrix = cosine_similarity(df_merged[columns_for_similarity])

        # Obtener el índice de la película de referencia
        input_title = title
        
        input_index = df_merged[df_merged['title'] == input_title].index[0]

        # Obtener las puntuaciones de similitud de la película de referencia
        similarity_scores = list(enumerate(cosine_sim_matrix[input_index]))

        # Ordenar las películas según su puntuación de similitud en orden descendente
        sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Obtener los índices de las películas más similares (excluyendo la película de referencia)
        similar_movies_indices = [i for i, _ in sorted_scores[:cantidad_recomendaciones]]

        # Obtener los títulos de las películas más similares
        similar_movies_titles = df_merged.iloc[similar_movies_indices]['title']

        # Imprimir las puntuaciones de similitud de la película de referencia y las películas recomendadas
        result = []
        for i, score in sorted_scores[:cantidad_recomendaciones]:
            result.append({"Movie": df_merged.iloc[i]['title'], "Percentage of similarity founded": round(score * 100, 1)})

        return {'Recomended movies': similar_movies_titles.tolist(), 'Similarity scores': result}

    except IndexError:
        error_message = 'Try with another movie title. Could be this MVP do not know that movie. Here we have a limited database, more than 22,000 movies... other way, you must be sure that the movie name is correct, search it in Google, maybe it helps you... For example, use: "toy story" a kids movie we all know..'
        
        # Buscar la palabra "Hola" en la columna "Campo"
        filtro = df_merged['title'].str.contains(title)

        # Aplicar el máscara al DataFrame original
        resultados = df_merged.loc[filtro, 'title'].head(5)

        # Mostrar los resultados
        return {'Error': error_message, 'Related movies': resultados.tolist()}




#____________________________________________________________________________________________________



@app.get("/get_recommendation2/{title}/{cantidad_recomendaciones}")
def get_recommendation2(title: str, cantidad_recomendaciones: int):
    """Get movie recommendations based on similarity scores.
    
    Args:
        title (str): Title of the movie to use as a reference.
        cantidad_recomendaciones (int): Number of similar movies to recommend.
    
    Returns:
        dict: Recommended movies and their similarity scores.
    """
    try:
        # Select relevant columns for cosine similarity calculation
        columns_for_similarity = df_merged.columns[17:]
        
        # Calculate the cosine similarity matrix
        cosine_sim_matrix = cosine_similarity(df_merged[columns_for_similarity])

        # Get the index of the reference movie
        reference_title = title
        reference_index = df_merged[df_merged['title'] == reference_title].index[0]

        # Get the similarity scores of the reference movie
        similarity_scores = list(enumerate(cosine_sim_matrix[reference_index]))

        # Sort movies based on similarity scores in descending order
        sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Get the indices of the most similar movies (excluding the reference movie)
        similar_movies_indices = [i for i, _ in sorted_scores[:cantidad_recomendaciones]]

        # Get the titles of the most similar movies
        similar_movies_titles = df_merged.iloc[similar_movies_indices]['title']

        # Generate the list of recommended movies with their similarity scores
        result = []
        for i, score in sorted_scores[:cantidad_recomendaciones]:
            result.append({
                "Movie": df_merged.iloc[i]['title'],
                "Percentage of similarity": round(score * 100, 1)
            })

        return {
            'Recomended movies': similar_movies_titles.tolist(),
            'Similarity scores': result
        }

    except IndexError:
        error_message = 'Try with another movie title. Could be that this MVP does not know that movie. Here we have a limited database of more than 22,000 movies... Otherwise, make sure the movie name is correct. You can search it on Google. For example, use: "Toy Story" - a well-known kids movie.'

        # Search for related movies using a filter on the "title" column
        filtro = df_merged['title'].str.contains(title)

        # Apply the mask to the original DataFrame
        resultados = df_merged.loc[filtro, 'title'].head(5)

        return {
            'Error': error_message,
            'Related movies': resultados.tolist()
        }


#____________________________________________________________________________________________________


@app.get("/get_recommendation3/{title}/{cantidad_recomendaciones}")
def get_recommendation3(title: str, cantidad_recomendaciones: int):
    """Get movie recommendations based on similarity scores.
    
    Args:
        title (str): Title of the movie to use as a reference.
        cantidad_recomendaciones (int): Number of similar movies to recommend.
    
    Returns:
        dict: Recommended movies and their similarity scores.
    """
    try:
        # Select relevant columns for cosine similarity calculation
        columns_for_similarity = df_merged.columns[17:]
        
        # Calculate the cosine similarity matrix
        cosine_sim_matrix = cosine_similarity(df_merged[columns_for_similarity])

        # Get the index of the reference movie
        reference_title = title
        reference_index = df_merged[df_merged['title'] == reference_title].index[0]

        # Get the similarity scores of the reference movie
        similarity_scores = list(enumerate(cosine_sim_matrix[reference_index]))

        # Sort movies based on similarity scores in descending order
        sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Get the indices of the most similar movies (excluding the reference movie)
        similar_movies_indices = [i for i, _ in sorted_scores[:cantidad_recomendaciones]]

        # Get the titles of the most similar movies
        similar_movies_titles = df_merged.iloc[similar_movies_indices]['title']

        # Generate the list of recommended movies with their similarity scores
        result = []
        for i, score in sorted_scores[:cantidad_recomendaciones]:
            result.append({
                "Movie": df_merged.iloc[i]['title'],
                "Percentage of similarity": round(score * 100, 1)
            })

        return {
            'Recomended movies': similar_movies_titles.to_dict(),
            'Similarity scores': result
        }

    except IndexError:
        error_message = 'Try with another movie title. Could be that this MVP does not know that movie. Here we have a limited database of more than 22,000 movies... Otherwise, make sure the movie name is correct. You can search it on Google. For example, use: "Toy Story" - a well-known kids movie.'

        # Search for related movies using a filter on the "title" column
        filtro = df_merged['title'].str.contains(title)

        # Apply the mask to the original DataFrame
        resultados = df_merged.loc[filtro, 'title'].head(5)

        return {
            'Error': error_message,
            'Related movies': resultados.to_dict()
        }

