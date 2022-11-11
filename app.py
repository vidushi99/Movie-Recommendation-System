import pickle
import requests
import pandas as pd
import streamlit as st
df = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
hollywood_df = pickle.load(open('hollywood_movies.pkl','rb'))
similarity1 = pickle.load(open('similarity1.pkl','rb'))
movie_list = df['title'].values
hollywood_movies = hollywood_df['original_title'].values

def fetch_hollywood_poster(id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=554ea29ab95145cde55cd8339423e8d4&language=en-US'.format(id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
def fetch_poster(imdb_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=554ea29ab95145cde55cd8339423e8d4&language=en-US'.format(imdb_id))
    data = response.json()
    try:
        try:
            path = data['poster_path']
        except KeyError:
            path =  ''
        return 'https://image.tmdb.org/t/p/w500/'+ path
    except TypeError:
        return ''

def recommed(movie):
    movie_index = df[df['title']==movie].index[0]
    distance = similarity[movie_index]
    movie_lists = sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
    recommed_movies = []
    poster_paths = []
    for i in movie_lists:
        recommed_movies.append(df['title'].iloc[i[0]])
        poster_paths.append(fetch_poster(df['imdb_id'].iloc[i[0]]))
    try:
       return recommed_movies,poster_paths
    except TypeError:
        return 'image not availabe'

def reccomed_hollywood(movie):
    movie_index = hollywood_df[hollywood_df['original_title'] == movie].index[0]
    distance = similarity1[movie_index]
    movie_lists = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recommed_movies = []
    poster_paths = []
    for i in movie_lists:
        recommed_movies.append(hollywood_df['original_title'].iloc[i[0]])
        poster_paths.append(fetch_hollywood_poster(hollywood_df['id'].iloc[i[0]]))
    return recommed_movies,poster_paths

st.header('Welcome To Movie Recommendation System')
is_bollywood = st.selectbox('',('select','Bollywood','Hollywood'))
if is_bollywood=='Bollywood':
     selected_movie = st.selectbox(
          'Select Movie',movie_list)

     if st.button('Recommend'):
          recommedations,paths = recommed(selected_movie)
          col1,col2,col3,col4,col5 = st.columns(5)
          with col1:
                 st.text(recommedations[0])
                 try:
                     st.image(paths[0])
                 except:
                     st.text('poster not avalaible')
          with col2:
                 st.text(recommedations[1])
                 try:
                     st.image(paths[1])
                 except:
                     st.text('poster not available')
          with col3:
                 st.text(recommedations[2])
                 try:
                    st.image(paths[2])
                 except:
                     st.text('poster not availabe')
          with col4:
                 st.text(recommedations[3])
                 try:
                    st.image(paths[3])
                 except:
                     st.text('poster not available')
          with col5:
                 st.text(recommedations[4])
                 try:
                     st.image(paths[4])
                 except:
                     st.text('poster not available')

elif is_bollywood=='Hollywood':

    selected_movie = st.selectbox(
        'Select Movie', hollywood_movies)

    if st.button('Recommend'):
        recommedations, paths = reccomed_hollywood(selected_movie)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommedations[0])
            st.image(paths[0])

        with col2:
            st.text(recommedations[1])
            st.image(paths[1])
        with col3:
            st.text(recommedations[2])
            st.image(paths[2])
        with col4:
            st.text(recommedations[3])
            st.image(paths[3])
        with col5:
            st.text(recommedations[4])
            st.image(paths[4])
