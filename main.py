

# Define your routes and other FastAPI configurations here

from typing import Union
from fastapi import FastAPI
import pickle
app = FastAPI()
import pandas as pd
import itertools
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches
import requests
from difflib import get_close_matches

#
# URLs de los archivos Pickle en GitHub
urls = [
    'https://github.com/Lucaramallo/PI1_MLOps_Sistema_de_Recomendacion_Movies_ML/raw/main/Datasets_Cleaned_light/df_f1_lang_movie_count.pkl',
    'https://github.com/Lucaramallo/PI1_MLOps_Sistema_de_Recomendacion_Movies_ML/raw/main/Datasets_Cleaned_light/df_f2_movies_runtime.pkl',
    'https://github.com/Lucaramallo/PI1_MLOps_Sistema_de_Recomendacion_Movies_ML/raw/main/Datasets_Cleaned_light/df_f3_collection_name_returns.pkl',
    'https://github.com/Lucaramallo/PI1_MLOps_Sistema_de_Recomendacion_Movies_ML/raw/main/Datasets_Cleaned_light/df_f4_production_countrys.pkl',
    'https://github.com/Lucaramallo/PI1_MLOps_Sistema_de_Recomendacion_Movies_ML/raw/main/Datasets_Cleaned_light/df_f5_production_companies_return.pkl',
    'https://github.com/Lucaramallo/PI1_MLOps_Sistema_de_Recomendacion_Movies_ML/raw/main/Datasets_Cleaned_light/df_f6_df_expanded.pkl',
    'https://github.com/Lucaramallo/PI1_MLOps_Sistema_de_Recomendacion_Movies_ML/raw/main/Datasets_Cleaned_light/df_f6_get_director.pkl',
    'https://github.com/Lucaramallo/PI1_MLOps_Sistema_de_Recomendacion_Movies_ML/raw/main/Datasets_Cleaned_light/df_f7_one_hot_genres.pkl'
]

# Descargar y cargar los archivos Pickle
dataframes = []
for url in urls:
    response = requests.get(url)
    with open(url.split('/')[-1], 'wb') as f:
        f.write(response.content)
    dataframe = pd.read_pickle(url.split('/')[-1])
    dataframes.append(dataframe)

# Asignar los DataFrames a las variables correspondientes
df_f1_lang_movie_count, df_f2_movies_runtime, df_f3_collection_name_returns, df_f4_production_countrys, df_f5_production_companies_return, df_f6_df_expanded, df_f6_get_director, df_f7_one_hot_genres = dataframes

# Ahora @app.get('/peliculas_idioma/{idioma}')
@app.get('/peliculas_idioma/{idioma}')
def peliculas_idioma(idioma: str):
    '''Ingresas el idioma, retornando la cantidad de peliculas producidas en el mismo'''
    filtered_df = df_f1_lang_movie_count[df_f1_lang_movie_count['language_name'] == idioma]
    count = 0  # Inicializar la variable count como 0
    
    if not filtered_df.empty:
        count = filtered_df['count'].values[0].item()  # Convertir a tipo nativo de Python
    
    if count > 0:
        return {'idioma': idioma, 'cantidad': count}
    else:
        return {'idioma': idioma, 'cantidad': 0}  # Asegurarse de devolver un valor válido





@app.get('/peliculas_duracion/{movie_name}')
def peliculas_duracion(movie_name: str):
    '''Ingresas la pelicula, retornando la duracion y el año'''

    # Filtrar el DataFrame para obtener la fila que corresponde al nombre de la película proporcionado
    filtered_df = df_f2_movies_runtime[df_f2_movies_runtime['title'] == movie_name]

    if not filtered_df.empty:
        # Obtener el valor del runtime
        runtime = filtered_df['runtime'].values[0]
        year = filtered_df['release_year'].values[0]

        # Crear el diccionario de respuesta
        response_dict = {
            'pelicula': movie_name,
            'duracion': runtime,
            'anio': year
        }
    else:
        # Si no se encuentra la película, retornar un diccionario vacío
        response_dict = {}

    return response_dict

@app.get('/franquicia/{franquicia}')
def franquicia(collection_name:str):
    '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio'''
    # Filtrar los datos en función del valor de la columna 'collection_name'
    df_return = df_f3_collection_name_returns[df_f3_collection_name_returns['collection_name'] == collection_name]

    # Verificar si la colección fue encontrada
    if df_return.empty:
        print(f"No se encontró la colección '{collection_name}' en el dataframe.")
        return None

    # Calcular la cantidad de películas
    cantidad_peliculas = df_return['id_list'].apply(len).sum()

    # Calcular la ganancia total
    ganancia_total = df_return['return_sum'].sum()

    # Calcular la ganancia promedio
    ganancia_promedio = df_return['return_mean'].mean()

    # Crear el diccionario de respuesta
    response_dict = {
        'franquicia': collection_name,
        'cantidad': cantidad_peliculas,
        'ganancia_total': ganancia_total,
        'ganancia_promedio': ganancia_promedio
    }

    return response_dict


@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais:str):
    '''Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo'''
    # Contar las películas producidas en el país proporcionado (teniendo en cuenta las listas de valores)
    cantidad_peliculas = df_f4_production_countrys.apply(lambda x: pais.lower() in x).sum()

    # Crear el diccionario de respuesta
    response_dict = {
        'pais': pais,
        'cantidad': cantidad_peliculas
    }

    return response_dict


@app.get('/productoras_exitosas/{productora}')
def productoras_exitosas(productora:str):
    '''Ingresas la productora, entregandote el revunue total y la cantidad de peliculas que realizo '''
    # Filtrar el dataframe para obtener los datos de la productora deseada
    productora_data = df_f5_production_companies_return[df_f5_production_companies_return['production_companies_nombres'].str.contains(productora, case=False, na=False)]

    # Verificar si la productora existe en el dataframe
    if productora_data.empty:
        return {'mensaje': f"La productora '{productora}' no fue encontrada en el dataframe."}

    # Calcular el revenue total de la productora
    revenue_total = productora_data['return_per_company'].sum()
    cant_movies = productora_data['count_movies'].sum()

    # Crear el diccionario de respuesta
    response_dict = {
        'productora': productora,
        'revenue_total': revenue_total,
        'cantidad': cant_movies
    }

    return response_dict


@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno.
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma. En formato lista'''
    # Convertir el valor a minúsculas
    nombre_director = nombre_director.lower()
    if df_f6_get_director[df_f6_get_director['directors_names'] == nombre_director].empty:
        return {'mensaje': 'No encontramos el director en el set de datos...'}
    else:
        director_df_resume = df_f6_get_director[df_f6_get_director['directors_names'] == nombre_director]
        retorno_total_director = round(director_df_resume['director_return'].iloc[0])

        movies_titles = director_df_resume['title']
        flattened_titles = list(itertools.chain(*movies_titles))

        movies_release_date = director_df_resume['release_date']

        retorno_total_movies = round(director_df_resume['return'].iloc[0])
        budget_pelicula = round(director_df_resume['budget'].iloc[0])
        revenue_pelicula = round(director_df_resume['revenue'].iloc[0])

        peliculas_info = []

        for movie in flattened_titles:
            movie_search_df = df_f6_df_expanded[df_f6_df_expanded['title'] == movie]
            movie_info = {
                'title': movie,
                'release_date': movie_search_df['release_date'].iloc[0],
                'budget': movie_search_df['budget'].iloc[0],
                'revenue': movie_search_df['revenue'].iloc[0],
                'return': movie_search_df['return'].iloc[0]
            }
            peliculas_info.append(movie_info)

        return {
            'director': nombre_director,
            'retorno_total_director': retorno_total_director,
            'peliculas': peliculas_info
        }





@app.get('/recomendacion/{reference_movie}')
def recomendacion(reference_movie: str, n: int = 16, cutoff: float = 0.5):
    '''Ingresas un nombre de película y te recomienda las similares en una lista'''
    results = {'movie_reference': reference_movie}
    reference_movie = reference_movie.lower()
    
    if reference_movie in df_f7_one_hot_genres['title'].values:
        reference_row = df_f7_one_hot_genres[df_f7_one_hot_genres['title'] == reference_movie].iloc[:, 1:]
        similarities = cosine_similarity(df_f7_one_hot_genres.iloc[:, 1:], reference_row)
        df_f7_one_hot_genres['similarity'] = similarities
        similar_movies = df_f7_one_hot_genres.sort_values(by='similarity', ascending=False).head(n)
        similar_movies = similar_movies.iloc[1:]

        results['similar_movies'] = similar_movies[['title', 'similarity']].to_dict(orient='records')
    else:
        similar_titles = get_close_matches(reference_movie, df_f7_one_hot_genres['title'], n=n, cutoff=cutoff)
        results['suggested_titles'] = similar_titles

    return results
