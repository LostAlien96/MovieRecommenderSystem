<<<<<<< HEAD
import streamlit as st
import pandas as pd
import pickle
import requests
import time
import os

# --------------------------
# TMDB API Fetch Function
# --------------------------
@st.cache_data
def fetch_movie_details(movie_id):
    """Fetch movie poster, rating, release date, and overview from TMDB API."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=2ff5c76fc5ae03868d5b884796e50406&language=en-US"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()

            poster_url = "https://image.tmdb.org/t/p/w500/" + data.get("poster_path", "")
            title = data.get("title", "Unknown Title")
            rating = data.get("vote_average", "N/A")
            year = data.get("release_date", "N/A")[:4]
            overview = data.get("overview", "No description available.")

            return {
                "poster": poster_url if data.get("poster_path") else "https://via.placeholder.com/500x750?text=No+Poster",
                "title": title,
                "rating": rating,
                "year": year,
                "overview": overview
            }

        except requests.exceptions.RequestException as e:
            if attempt < 2:
                time.sleep(1)
                continue
            else:
                st.warning(f"⚠️ Failed to fetch details for movie ID {movie_id}: {e}")
                return {
                    "poster": "https://via.placeholder.com/500x750?text=Poster+Not+Available",
                    "title": "Unknown",
                    "rating": "N/A",
                    "year": "N/A",
                    "overview": "No details available."
                }

# --------------------------
# Recommendation Logic
# --------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_details = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        details = fetch_movie_details(movie_id)
        recommended_details.append(details)

    return recommended_details

# --------------------------
# Load Data
# --------------------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --------------------------
# Streamlit UI
# --------------------------
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

st.title("🎥 Movie Recommender System")
st.markdown("Get top 5 similar movies based on your selected choice!")

selected_movie_name = st.selectbox(
    "🔍 Search for a Movie",
    movies['title'].values
)

if st.button("🎯 Recommend"):
    with st.spinner("Fetching recommendations..."):
        recommendations = recommend(selected_movie_name)

    st.subheader("✨ Recommended Movies:")

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            movie = recommendations[idx]
            st.image(movie["poster"], use_container_width=True)
            st.markdown(f"**{movie['title']} ({movie['year']})**")
            st.markdown(f"⭐ **Rating:** {movie['rating']}")
            st.caption(movie["overview"][:120] + "...")
=======
import streamlit as st
import pandas as pd
import pickle
import requests
import time

# --------------------------
# TMDB API Fetch Function
# --------------------------
@st.cache_data
def fetch_movie_details(movie_id):
    """Fetch movie poster, rating, release date, and overview from TMDB API."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=2ff5c76fc5ae03868d5b884796e50406&language=en-US"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()

            poster_url = "https://image.tmdb.org/t/p/w500/" + data.get("poster_path", "")
            title = data.get("title", "Unknown Title")
            rating = data.get("vote_average", "N/A")
            year = data.get("release_date", "N/A")[:4]
            overview = data.get("overview", "No description available.")

            return {
                "poster": poster_url if data.get("poster_path") else "https://via.placeholder.com/500x750?text=No+Poster",
                "title": title,
                "rating": rating,
                "year": year,
                "overview": overview
            }

        except requests.exceptions.RequestException as e:
            if attempt < 2:
                time.sleep(1)
                continue
            else:
                st.warning(f"⚠️ Failed to fetch details for movie ID {movie_id}: {e}")
                return {
                    "poster": "https://via.placeholder.com/500x750?text=Poster+Not+Available",
                    "title": "Unknown",
                    "rating": "N/A",
                    "year": "N/A",
                    "overview": "No details available."
                }

# --------------------------
# Recommendation Logic
# --------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_details = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        details = fetch_movie_details(movie_id)
        recommended_details.append(details)

    return recommended_details

# --------------------------
# Load Data
# --------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


movies_dict = pickle.load(open(os.path.join(BASE_DIR, 'movie_dict.pkl'), 'rb'))
similarity = pickle.load(open(os.path.join(BASE_DIR, 'similarity.pkl'), 'rb'))
movies = pd.DataFrame(movies_dict)

# --------------------------
# Streamlit UI
# --------------------------
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

st.title("🎥 Movie Recommender System")
st.markdown("Get top 5 similar movies based on your selected choice!")

selected_movie_name = st.selectbox(
    "🔍 Search for a Movie",
    movies['title'].values
)

if st.button("🎯 Recommend"):
    with st.spinner("Fetching recommendations..."):
        recommendations = recommend(selected_movie_name)

    st.subheader("✨ Recommended Movies:")

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            movie = recommendations[idx]
            st.image(movie["poster"], use_container_width=True)
            st.markdown(f"**{movie['title']} ({movie['year']})**")
            st.markdown(f"⭐ **Rating:** {movie['rating']}")
            st.caption(movie["overview"][:120] + "...")
>>>>>>> 03bb0e88bcddde825b639366871c1e6fd9335c64
