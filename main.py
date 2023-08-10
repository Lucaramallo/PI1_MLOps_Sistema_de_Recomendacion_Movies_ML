

# Define your routes and other FastAPI configurations here

from typing import Union
from fastapi import FastAPI
app = FastAPI()
import pandas as pd
import itertools
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches
import requests
from difflib import get_close_matches
import ast

# URLs de los archivos Pickle en GitHub
urls = [
    'https://github.com/Lucaramallo/PI1_MLOps_Sistema_de_Recomendacion_Movies_ML/raw/main/Datasets_Cleaned_light/df_f1_lang_movie_count.csv',
    'https://github.com/Lucaramallo/PI1_MLOps_Sistema_de_Recomendacion_Movies_ML/raw/main/Datasets_Cleaned_light/df_f2_movies_runtime.csv',
    'https://github.com/Lucaramallo/PI1_MLOps_Sistema_de_Recomendacion_Movies_ML/raw/main/Datasets_Cleaned_light/df_f3_collection_name_returns.csv',
    'https://github.com/Lucaramallo/PI1_MLOps_Sistema_de_Recomendacion_Movies_ML/raw/main/Datasets_Cleaned_light/df_f4_production_countrys.csv',
    'https://github.com/Lucaramallo/PI1_MLOps_Sistema_de_Recomendacion_Movies_ML/raw/main/Datasets_Cleaned_light/df_f5_production_companies_return.csv',
    'https://github.com/Lucaramallo/PI1_MLOps_Sistema_de_Recomendacion_Movies_ML/raw/main/Datasets_Cleaned_light/df_f6_df_expanded.csv',
    'https://github.com/Lucaramallo/PI1_MLOps_Sistema_de_Recomendacion_Movies_ML/raw/main/Datasets_Cleaned_light/df_f6_get_director.csv',
    'https://github.com/Lucaramallo/PI1_MLOps_Sistema_de_Recomendacion_Movies_ML/raw/main/Datasets_Cleaned_light/df_f7_one_hot_genres.csv'
]

# Descargar y cargar los archivos CSVS
dataframes = []
for url in urls:
    response = requests.get(url)
    with open(url.split('/')[-1], 'wb') as f:
        f.write(response.content)
    dataframe = pd.read_csv(url.split('/')[-1])
    dataframes.append(dataframe)

# Asignar los DataFrames a las variables correspondientes
df_f1_lang_movie_count, df_f2_movies_runtime, df_f3_collection_name_returns, df_f4_production_countrys, df_f5_production_companies_return, df_f6_df_expanded, df_f6_get_director, df_f7_one_hot_genres = dataframes



# Ahora @app.get('/peliculas_idioma/{idioma}') 
@app.get('/peliculas_idioma/{idioma}') # ok
def peliculas_idioma(idioma: str):
    '''Ingresas el idioma, retornando la cantidad de peliculas producidas en el mismo, ej english'''
    idioma = idioma.lower()
    filtered_df = df_f1_lang_movie_count[df_f1_lang_movie_count['language_name'] == idioma]
    count = 0  # Inicializar la variable count como 0
    
    if not filtered_df.empty:
        count = filtered_df['count'].values[0].item()  # Convertir a tipo nativo de Python
    
    if count > 0:
        return {'idioma': idioma, 'cantidad': count}
    else:
        return {'idioma': idioma, 'cantidad': 0}  # Asegurarse de devolver un valor válido

#peliculas_idioma('english')

@app.get('/peliculas_duracion/{movie_name}') # ok
def peliculas_duracion(movie_name: str):
    '''Ingresas la pelicula, retornando la duracion y el año. ej, pulp fiction'''
    movie_name = movie_name.lower()
    # Filtrar el DataFrame para obtener la fila que corresponde al nombre de la película proporcionado
    filtered_df = df_f2_movies_runtime[df_f2_movies_runtime['title'] == movie_name]

    if not filtered_df.empty:
        # Obtener el valor del runtime
        runtime = filtered_df['runtime'].values[0].item()  # Convertir a tipo nativo de Python
        year = filtered_df['release_year'].values[0].item()  # Convertir a tipo nativo de Python

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

#peliculas_duracion('toy story')

@app.get('/franquicia/{collection_name}') # ok
def franquicia(collection_name: str):
    '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio. ej, toy story collection'''
    collection_name = collection_name.lower()

    # Filtrar los datos en función del valor de la columna 'collection_name'
    df_return = df_f3_collection_name_returns[df_f3_collection_name_returns['collection_name'].str.contains(collection_name)]

    # Verificar si la colección fue encontrada
    if df_return.empty:
        return f"No se encontró la colección '{collection_name}' en el dataframe."

    # Calcular la cantidad de películas
    cantidad_peliculas = df_return['id_list'].apply(len).sum().item()

    # Calcular la ganancia total
    ganancia_total = round(df_return['return_sum'].sum(), 2)

    # Calcular la ganancia promedio
    ganancia_promedio = round(df_return['return_mean'].mean(), 2)

    # Crear el diccionario de respuesta
    response_dict = {
        'franquicia': collection_name,
        'cantidad': cantidad_peliculas,
        'ganancia_total': ganancia_total,
        'ganancia_promedio': ganancia_promedio
    }

    return response_dict

# franquicia('toy story collection')

@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais: str):
    '''Ingresas el país, retornando la cantidad de películas producidas en el mismo. ej argentina'''
    # Convert the country name to lowercase for case-insensitive matching
    pais = pais.lower()
    
    # Filter out rows with missing values in the 'country_names' column, then use .str.contains()
    filtered_df = df_f4_production_countrys.dropna(subset=['country_names'])
    count = filtered_df[filtered_df['country_names'].str.contains(pais, case=False)].shape[0]

    # Create the response dictionary
    response_dict = {
        'pais': pais,
        'cantidad': count
    }
    return response_dict



# peliculas_pais('argentina')


@app.get('/productoras_exitosas/{production_company}')
def productoras_exitosas(production_company: str):
    '''Se ingresa la productora, retornando el promedio de ganancias y la ganancia total, ej pixar'''
    production_company = production_company.lower()

    # Filter the DataFrame to get data for the desired production company
    productora_data = df_f5_production_companies_return[df_f5_production_companies_return['production_companies_nombres'].str.contains(production_company, case=False)]

    # Verificar si la productora existe en el dataframe
    if productora_data.empty:
        return {"error": f"La productora '{production_company}' no fue encontrada en el dataframe."}

    # Convert numpy int64 values to regular Python integers
    revenue_total = int(productora_data['return_per_company'].sum())
    cant_movies = int(productora_data['count_movies'].sum())

    # Crear el diccionario de respuesta
    response_dict = {
        'productora': production_company,
        'revenue_total': revenue_total,
        'cant_movies': cant_movies
    }
    
    return response_dict

# productoras_exitosas('pixar')


@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
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

        for movie in flattened_titles:
            movie_search_df = df_f6_df_expanded[df_f6_df_expanded['title'] == movie]
            lista_movie_b_r_r = movie_search_df[['title', 'release_date', 'budget', 'revenue', 'return']].to_records(index=False)
            # print(f'Listado de informacion peliculas para el director {nombre_director}')
            # print(f'retorno_total_director: {retorno_total_director}')
            # print(f'Listado de peliculas: {flattened_titles}')
            # print(f'Listado de fechas para las peliculas retornadas: {movies_release_date}')
            # print(f'Listado de Returns para las peliculas retornadas: {retorno_total_movies}')
            # print(f'Listado de Revenues para las peliculas retornadas: {revenue_pelicula}')
            # print(f'Listado de Budgets para las peliculas retornadas: {budget_pelicula}')
            # print(f'listado de info movies: {lista_movie_b_r_r}')
        
        dict_rta =  {'director': nombre_director, 'retorno_total_director': retorno_total_director, 
                'peliculas': movies_titles, 'fechas de lanzamiento': movies_release_date, 'retorno_peliculas': retorno_total_movies, 
                'budget_peliculas': budget_pelicula, 'revenue_peliculas': revenue_pelicula, 'listado_de_info_movies': lista_movie_b_r_r}
        print(dict_rta)
        return(dict_rta)


get_director('quentin tarantino')

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
# recomendacion('toy story')