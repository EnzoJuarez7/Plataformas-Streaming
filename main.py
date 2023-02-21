from fastapi import FastAPI
import pandas as pd



# Creacion de una aplicación FastAPI.

app = FastAPI(title='Consultas Plataformas')



@app.get ("/")
async def read_root():
    return {"Hello":
            "World!"}

#Consultas

'''
1. Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN. 
La función debe llamarse get_max_duration(year, platform, duration_type)
'''

@app.get ("/get_max_duration")
def get_max_duration(year:int=None, platform:str=None, duration_type:str=None) -> str:
    # Cargar el dataframe
    df = pd.read_csv('Data_final_plataformas.csv')
    
    # Filtrar el dataframe según los filtros opcionales especificados
    if year is not None:
        df = df[df['release_year'] == year]
    if platform is not None:
        df = df[df['platform'] == platform]
    if duration_type is not None:
        df = df[df['duration_type'] == duration_type]
    
    # Obtener la película con mayor duración
    max_duration = df['duration_int'].max()
    movie_title = df[df['duration_int'] == max_duration]['title'].iloc[0]
    
    return f'La película con mayor duración en el año {year} en {platform} es: {movie_title}'

'''
2. Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año 
La función debe llamarse get_score_count(platform, scored, year)
'''

@app.get ("/get_score_count")
def get_score_count(platform: str, scored: float, year: int) -> int:
    # Carga el dataframe con las columnas score, type, release_year y platform
    df = pd.read_csv('Data_final_plataformas.csv')
    
    # Filtra el dataframe por la plataforma, el puntaje y el año especificados
    df_filtrado = df[(df['platform'] == platform) & (df['score'] > scored) & (df['release_year'] == year) & (df['type'] == 'movie')]
    
    # Cuenta la cantidad de películas en el dataframe filtrado
    cantidad_peliculas = df_filtrado['type'].count()
    
    # Retorna la cantidad de películas como un entero
    return f'Hay {cantidad_peliculas} películas con un puntaje mayor a {scored} en {platform}'

'''
3. Cantidad de películas por plataforma con filtro de PLATAFORMA. 
La función debe llamarse get_count_platform(platform)
'''

@app.get ("/get_count_platform")
def get_count_platform(platform:str) -> int:
    # Cargar el dataframe
    df = pd.read_csv('Data_final_plataformas.csv')
    
    # Filtrar el dataframe según la plataforma y el tipo de película especificados
    df = df[(df['platform'] == platform) & (df['type'] == 'movie')]
    
    # Contar el número de películas que pertenecen a la plataforma y son películas
    count = df['type'].count()
    
    return f'Hay {count} películas en {platform}'

'''
4. Actor que más se repite según plataforma y año. 
La función debe llamarse get_actor(platform, year)
'''

@app.get ("/get_actor")
def get_actor(platform: str, year: int) -> tuple:
    # Carga el dataframe con las columnas cast, release_year y platform
    df = pd.read_csv('Data_final_plataformas.csv')
    
    # Filtra el dataframe por la plataforma y el año especificados
    df_filtrado = df[(df['platform'] == platform) & (df['release_year'] == year)]
    
    # Cuenta la frecuencia de los actores y selecciona el actor que más se repite
    actor_mas_repetido = df_filtrado['cast'].str.split(',', expand=True).stack().value_counts().index[0]
    cantidad_apariciones = df_filtrado['cast'].str.contains(actor_mas_repetido).sum()
    
    # Retorna los resultados como una tupla
    return f'El actor{actor_mas_repetido} es el más repetido en {platform} y se encuentra {cantidad_apariciones} veces'
