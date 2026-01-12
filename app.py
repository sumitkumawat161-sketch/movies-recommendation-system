import pickle
import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": "c3b9f433cf9d1e8003c2a3eafa94390b",
    }

    try:
        response = requests.get(url, params=params, timeout=3)
        response.raise_for_status()  
        data = response.json()

        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except requests.exceptions.RequestException as e:
        print("TMDB Error:", e)
        return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.markdown(
    "<h1 style='text-align: center;'>🎬 Movie Recommender System</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>Get movie recommendations based on your favorite movie</p>",
    unsafe_allow_html=True
)

selected_movie = st.selectbox(
    "🎥 Select a movie",
    movies['title'].values
)

if st.button("✨ Recommend Movies"):
    with st.spinner("Finding best recommendations..."):
        names, posters = recommend(selected_movie)

    if names:
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.image(posters[i], use_container_width=True)
                st.markdown(
                    f"<p style='text-align:center; font-weight:bold;'>{names[i]}</p>",
                    unsafe_allow_html=True
                )
    else:
        st.warning("No recommendations found.")

