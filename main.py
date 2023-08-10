

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
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno.
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma. En formato lista'''
    # Convertir el valor a minúsculas
    nombre_director = nombre_director.lower()

    if df_f6_get_director[df_f6_get_director['directors_names'] == nombre_director].empty:
        return {'mensaje': 'No encontramos el director en el set de datos...'}
    else:
        director_row = df_f6_get_director[df_f6_get_director['directors_names'] == nombre_director].iloc[0]
        retorno_total_director = int(round(director_row['director_return']))

        movie_titles = director_row['title']
        release_dates = director_row['release_date']
        budgets = director_row['budget']
        revenues = director_row['revenue']
        returns = director_row['return']

        peliculas_info = []

        for i in range(len(movie_titles)):
            movie_info = {
                'title': movie_titles[i],
                'release_date': release_dates[i],
                'budget': int(round(budgets[i])),
                'revenue': int(round(revenues[i])),
                'return': int(round(returns[i]))
            }
            peliculas_info.append(movie_info)

        response_dict = {
            'retorno_total_director': retorno_total_director,
            'peliculas_info': peliculas_info
        }
        print(response_dict)
        return response_dict



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