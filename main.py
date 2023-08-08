from fastapi import FastAPI
app = FastAPI()

# Define your routes and other FastAPI configurations here

from typing import Union
import pandas as pd
from fastapi import FastAPI
import itertools
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches

df_f1_lang_movie_count = pd.read_pickle('CURSADO HENRY DTS09\PI PT02 - Def\PI1_MLOps_Sistema_de_Recomendacion_Movies_ML\Datasets Cleaned & light\df_f1_lang_movie_count.pkl')
df_f2_movies_runtime = pd.read_pickle('CURSADO HENRY DTS09\PI PT02 - Def\PI1_MLOps_Sistema_de_Recomendacion_Movies_ML\Datasets Cleaned & light\df_f2_movies_runtime.pkl')
df_f3_collection_name_returns = pd.read_pickle('CURSADO HENRY DTS09\PI PT02 - Def\PI1_MLOps_Sistema_de_Recomendacion_Movies_ML\Datasets Cleaned & light\df_f3_collection_name_returns.pkl')
df_f4_production_countrys = pd.read_pickle('CURSADO HENRY DTS09\PI PT02 - Def\PI1_MLOps_Sistema_de_Recomendacion_Movies_ML\Datasets Cleaned & light\df_f4_production_countrys.pkl')
df_f5_production_companies_return = pd.read_pickle('CURSADO HENRY DTS09\PI PT02 - Def\PI1_MLOps_Sistema_de_Recomendacion_Movies_ML\Datasets Cleaned & light\df_f5_production_companies_return.pkl')
df_f6_df_expanded = pd.read_pickle('CURSADO HENRY DTS09\PI PT02 - Def\PI1_MLOps_Sistema_de_Recomendacion_Movies_ML\Datasets Cleaned & light\df_f6_df_expanded.pkl')
df_f6_get_director = pd.read_pickle('CURSADO HENRY DTS09\PI PT02 - Def\PI1_MLOps_Sistema_de_Recomendacion_Movies_ML\Datasets Cleaned & light\df_f6_get_director.pkl')
df_f7_one_hot_genres = pd.read_pickle('CURSADO HENRY DTS09\PI PT02 - Def\PI1_MLOps_Sistema_de_Recomendacion_Movies_ML\Datasets Cleaned & light\df_f7_one_hot_genres.pkl')



@app.get('/peliculas_idioma/{idioma}')
def peliculas_idioma(idioma:str):
    '''Ingresas el idioma, retornando la cantidad de peliculas producidas en el mismo'''
    
    filtered_df = df_f1_lang_movie_count[df_f1_lang_movie_count['language_name'] == idioma]
    count = int()
    if not filtered_df.empty:
        # Obtener los valores del iso_language_code y el conteo
        iso_language_code = filtered_df['iso_language_code'].values[0]
        count = filtered_df['count'].values[0]
        
        # Imprimir los resultados
        print(f"Nombre del lenguaje: {idioma}")
        print(f"ISO Language Code: {iso_language_code}")
        print(f"Movies count: {count}")
    else:
        print(f"No se encontró el lenguaje: {idioma}")

    return {'idioma':idioma, 'cantidad':count}
    


@app.get('/peliculas_duracion/{movie_name}')
def peliculas_duracion(movie_name:str):
    '''Ingresas la pelicula, retornando la duracion y el año'''

    # Filtrar el DataFrame para obtener la fila que corresponde al nombre de la película proporcionado
    filtered_df = df_f2_movies_runtime[df_f2_movies_runtime['title'] == movie_name]
    
    if not filtered_df.empty:
        # Obtener el valor del runtime
        runtime = filtered_df['runtime'].values[0]
        year = filtered_df['release_year'].values[0]

        # Imprimir el resultado
        print(f"Nombre de la película: {movie_name}")
        print(f"Runtime: {runtime} minutos")
        print(f"Lanzada en el año {year}")
    else:
        print(f"No se encontró la película: {movie_name}")
    return {'pelicula':movie_name, 'duracion':runtime, 'anio':year}



@app.get('/franquicia/{franquicia}')
def franquicia(collection_name:str):
    '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio'''
    # Filtrar los datos en función del valor de la columna 'collection_name'
    df_return = df_f3_collection_name_returns[df_f3_collection_name_returns['collection_name'] == collection_name]

    # Verificar si la colección fue encontrada
    if df_return.empty:
        print(f"No se encontró la colección '{collection_name}' en el dataframe.")
        return

    # Calcular la cantidad de películas
    cantidad_peliculas = df_return['id_list'].apply(len).sum()

    # Calcular la ganancia total
    ganancia_total = df_return['return_sum'].sum()

    # Calcular la ganancia promedio
    ganancia_promedio = df_return['return_mean'].mean()

    # Imprimir el resultado
    print(f"La franquicia {collection_name} posee {cantidad_peliculas} películas, una ganancia total de {ganancia_total:.2f} y una ganancia promedio de {ganancia_promedio:.2f}, aproximadamente...")
    return {'franquicia':collection_name, 'cantidad':cantidad_peliculas, 'ganancia_total':ganancia_total, 'ganancia_promedio':ganancia_promedio}



@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais:str):
    '''Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo'''
    # Contar las películas producidas en el país proporcionado (teniendo en cuenta las listas de valores)
    cantidad_peliculas = df_f4_production_countrys.apply(lambda x: pais.lower() in x).sum()
    
    print(f"Se han producido {cantidad_peliculas} películas en {pais}.")
    return {'pais':pais, 'cantidad':cantidad_peliculas}



@app.get('/productoras_exitosas/{productora}')
def productoras_exitosas(productora:str):
    '''Ingresas la productora, entregandote el revunue total y la cantidad de peliculas que realizo '''
    # Filtrar el dataframe para obtener los datos de la productora deseada
    productora_data = df_f5_production_companies_return[df_f5_production_companies_return['production_companies_nombres'].str.contains(productora, case=False, na=False)]

    # Verificar si la productora existe en el dataframe
    if productora_data.empty:
        return f"La productora '{productora}' no fue encontrada en el dataframe."

    # Calcular el revenue total de la productora
    revenue_total = productora_data['return_per_company'].sum()
    cant_movies = productora_data['count_movies'].sum()
    print(f"La productora '{productora}' ha tenido un return de {round(revenue_total, 2)} aproximadamente, es decir, que ha multiplicado sus budget_totales unas {round(revenue_total, 0)} veces haciendo peliculas y ha realizado {cant_movies} peliculas...")
    return {'productora':productora, 'revenue_total': revenue_total,'cantidad':cant_movies}



@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma. En formato lista'''
    # Convertir el valor a minúsculas
    nombre_director = nombre_director.lower()
    if df_f6_get_director[df_f6_get_director['directors_names'] == nombre_director].empty:
        print('No encontramos el director en el set de datos...')
        return None
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
            print(f'Listado de info peliculas para el director {nombre_director}')
            print(f'retorno_total_director: {retorno_total_director}')
            print(f'Listado de peliculas: {flattened_titles}')
            print(f'Listado de fechas para las peliculas retornadas: {movies_release_date}')
            print(f'Listado de Returns para las peliculas retornadas: {retorno_total_movies}')
            print(f'Listado de Revenues para las peliculas retornadas: {revenue_pelicula}')
            print(f'Listado de Budgets para las peliculas retornadas: {budget_pelicula}')
            
        
        return {'director': nombre_director, 'retorno_total_director': retorno_total_director, 
                'peliculas': flattened_titles, 'fechas de lanzamiento': movies_release_date, 'retorno_peliculas': retorno_total_movies, 
                'budget_peliculas': budget_pelicula, 'revenue_peliculas': revenue_pelicula}


# ML
@app.get('/recomendacion/{reference_movie}')
def recomendacion(reference_movie:str, n=16, cutoff=0.5):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
    results = {'movie_reference': reference_movie}
    reference_movie =reference_movie.lower()
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
    
    # Impresión de resultados en forma de lista
    print("Película de referencia:", results['movie_reference'])
    if 'similar_movies' in results:
        print("Películas similares:")
        for movie in results['similar_movies']:
            print(movie)
    elif 'suggested_titles' in results:
        print(f"No se encontró la película '{results['movie_reference']}'. ¿Quizás quisiste decir alguna de estas?")
        print(results['suggested_titles'])
   
