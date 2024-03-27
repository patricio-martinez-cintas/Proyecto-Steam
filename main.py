from fastapi import FastAPI
import pandas as pd
import random

app = FastAPI()

user_items_final = pd.read_parquet("./Datasets_final/user_items_final.parquet.gz")
steam_games_final = pd.read_parquet("./Datasets_final/steam_games_final.parquet.gz")
user_reviews_final = pd.read_parquet("./Datasets_final/user_reviews_final.parquet.gz")


@app.get("/Función developer")
def developer2(desarrollador: str):
    """Esta función devuelve un diccionario con la cantidad de items por año y el porcentaje de juegos free que hay en cada año. Recibe como parámetro el desarrollador en formato str."""
    unique_developers = steam_games_final['developer'].dropna().unique()

    if desarrollador in unique_developers:
        df_selected = steam_games_final.loc[steam_games_final["developer"] == desarrollador, ["release_year", "price"]].dropna(subset=["price"])
        df_summary = df_selected.assign(free_items=(df_selected['price'] == 0.00).astype(int)).groupby('release_year').agg(quantity_total=('price', 'count'), free_items=('free_items', 'sum')).reset_index()
        df_summary['free_per_year'] = (df_summary['free_items'] * 100 / df_summary['quantity_total']).round(2).astype(str) + '%'
        resultado_df = df_summary.sort_values(by='release_year').reset_index(drop=True)[["release_year", "quantity_total", "free_per_year"]].rename(columns={"release_year": "Año", "quantity_total": "Cantidad de items", "free_per_year": "Contenido free"})
        resultado_dict = resultado_df.to_dict(orient='records')
        return resultado_dict
    else:
        return f"El valor del parámetro debe ser str y el desarrollador debe ser alguno de los desarrolladores disponibles en Steam. Las desarrolladoras disponibles son: {', '.join(unique_developers)}"



@app.get("/Función UserForGenre")    
def UserForGenre(genero: str):
    if genero not in steam_games_final['genres'].unique():
        return "El género ingresado no está disponible en Steam."
    
    df_merge = pd.merge(user_items_final, steam_games_final, on="item_id", how="inner")
    df_filtered = df_merge[(df_merge['genres'] == genero) & (df_merge['release_year'] != 'Unknown')]
    if df_filtered.empty:
        return f"No hay datos para el género {genero} en los años disponibles."
    df_filtered["playtime_hours"] = (df_filtered["playtime_forever"] / 3600).round(2)
    df_grouped = df_filtered.groupby("user_id")['playtime_hours'].sum().reset_index()
    max_hours_user = df_grouped.loc[df_grouped['playtime_hours'].idxmax(), 'user_id']
    df_grouped_years = df_filtered.groupby("release_year")["playtime_hours"].sum().reset_index()
    list_of_dictionary = df_grouped_years.to_dict(orient="records")
    return {f"Usuario con más horas jugadas para Género {genero}": max_hours_user, "Horas jugadas por año": list_of_dictionary}



@app.get("/Función best_developer_year")
def best_developer_year(año: str):

    """Esta funcion devuelve el top 3 de desarrolladoras con juegos mas recomendados por usuarios para el año dado. Recibe como parametro el año en string"""

    if año not in steam_games_final['release_year'].unique():
        return f"El año {año} no está disponible en Steam o no es válido."
    df_merge = pd.merge(user_reviews_final, steam_games_final, on="item_id", how="inner")
    df_merge = df_merge.drop_duplicates(subset=['user_id', 'item_id'], keep='first')
    df_filtered = df_merge[(df_merge["release_year"] == año) & (df_merge["recommend"] == True) & (df_merge["sentiment_analysis"] == 2)]
    if df_filtered.empty:
        return f"No hay datos para el año {año} con las condiciones especificadas."
    df_size_rows = df_filtered.groupby('developer').size().nlargest(3).reset_index(name='number_rows')
    result = [{"Puesto " + str(i + 1): row["developer"]} for i, row in df_size_rows.iterrows()]
    return result

    
        
@app.get("/Función sentiment_analysis")
def sentiment_analysis(empresa_desarrolladora: str):
    """Devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento positivo o negativo como valor. Recibe como parametro la empresa desarrolladora de tipo str"""
    unique_developers = steam_games_final['developer'].dropna().unique()
    if isinstance(empresa_desarrolladora, str) and empresa_desarrolladora in unique_developers:
        df_filtered = user_reviews_final[user_reviews_final['item_id'].isin(steam_games_final.loc[steam_games_final['developer'] == empresa_desarrolladora, 'item_id'])]
        sentiment_counts = df_filtered['sentiment_analysis'].value_counts().to_dict()

        positive_count = sentiment_counts.get(2)
        negative_count = sentiment_counts.get(0)

        result = {empresa_desarrolladora: [f"Negative: {negative_count}", f"Positive: {positive_count}"]}
        return result
    else:
        return f"El valor del parámetro debe ser str y el desarrollador debe ser alguno de los desarrolladores disponibles en Steam. Los desarrolladores disponibles son: {', '.join(unique_developers)}"



@app.get("/Función game_recommendation")
def game_recommendation(id_producto: int):
    """Esta función recibe como parámetro la ID de un juego y devuelve 5 juegos aleatorios recomendables si encuentra la ID en el sistema, y 5 juegos aleatorios si no la encuentra. Recibe un valor entero."""
    if isinstance(id_producto, int):
        df_merge = pd.merge(user_reviews_final, steam_games_final, on="item_id", how="inner")
        df_merge["is_recommend"] = ((df_merge["recommend"]) & (df_merge["sentiment_analysis"] == 2))        
        df_recommend = df_merge[(df_merge["item_id"] != id_producto) & (df_merge['genres'].isin(df_merge['genres'][df_merge['item_id'] == id_producto])) & (df_merge["is_recommend"] == 1)]        
        if not df_recommend.empty:
            sampled_recommend = random.sample(df_recommend["item_name"].tolist(), min(5, len(df_recommend)))
            return {"Los juegos recomendados son": sampled_recommend}
        
        else:
            games = df_merge["item_name"].unique()
            sampled_games = random.sample(games.tolist(), min(5, len(games)))
            return {"El item_id del juego no se encuentra en la base de datos o no hay juegos recomendados. Se mostrarán juegos aleatorios": sampled_games}    

    else:
        return "El ID debe ser un tipo de dato entero."
