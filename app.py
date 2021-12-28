import streamlit as st
import pandas as pd
import numpy as np
import requests
import pickle

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="bird.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

api_key = '8658a3ba2d4031e31df56936ab285d15'
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies =[]
    recommended_movies_posters =[]

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        # fetch posters from api
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movies_dict.pkl','rb'))

movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))



st.title('Movies Recommender system')


 
selected_movie_name= st.selectbox(
'How would you like to be contacted?',
movies['title'].values)

# if st.button('Recommend'):
names,posters = recommend(selected_movie_name)

rows = 1
row_value = round(len(names)/rows)

for i in range(rows):
    for index,col in enumerate(st.columns(row_value)):
        with col:
            st.text(names[index + (row_value*i)-1])
            st.image(posters[index + (row_value*i)-1])




