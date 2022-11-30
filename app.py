import streamlit as st
import pickle
import pandas as pd
import requests

moviesDict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(moviesDict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?'
                            'api_key=9bb0e107ab403bd2696986ceb80a7dc1&language=en-US'.format(movie_id))
    movie_data = response.json()
    image_path = 'https://image.tmdb.org/t/p/w500'
    return image_path + movie_data['poster_path']


st.title('Movie Recommender System')

selectedMovie = st.selectbox(
    'Select Movie', movies['title'].values
)

if st.button('Recommend'):
    recommended_movies_names, recommended_movies_posters = recommend(selectedMovie)

    col1, col2, col3, col4, col5 = st.columns(3)

    with col1:
        st.text(recommended_movies_names[0])
        st.image(recommended_movies_posters[0])

    with col2:
        st.text(recommended_movies_names[1])
        st.image(recommended_movies_posters[1])

    with col3:
        st.text(recommended_movies_names[2])
        st.image(recommended_movies_posters[2])

    with col4:
        st.text(recommended_movies_names[3])
        st.image(recommended_movies_posters[3])

    with col5:
        st.text(recommended_movies_names[4])
        st.image(recommended_movies_posters[4])


