import pickle
import streamlit as st
import numpy as np

# import data
st.header('Book Recommender System')
model = pickle.load(open('artifacts/model.pkl','rb'))
books_name = pickle.load(open('artifacts/books_name.pkl','rb'))
data = pickle.load(open('artifacts/data.pkl','rb'))
pivot_data = pickle.load(open('artifacts/pivot_data.pkl','rb'))


def fetch_poster(suggestion):
    # Chargement des données
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(pivot_data.index[book_id])

    for name in book_name[0]: 
        ids = np.where(data['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = data.iloc[idx]['img_url']
        poster_url.append(url)

    return poster_url



def recommend_book(book_name):
    # Recommandation des 6 livres les plus proches
    books_list = []
    book_id = np.where(pivot_data.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(pivot_data.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6 )

    poster_url = fetch_poster(suggestion)
    
    for i in range(len(suggestion)):
            books = pivot_data.index[suggestion[i]]
            for j in books:
                books_list.append(j)
    return books_list , poster_url       



selected_books = st.selectbox(
    "Type or select a book from the dropdown",
    books_name
)

if st.button('Show Recommendation'):
    recommended_books,poster_url = recommend_book(selected_books)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_books[1])
        st.image(poster_url[1])
    with col2:
        st.text(recommended_books[2])
        st.image(poster_url[2])

    with col3:
        st.text(recommended_books[3])
        st.image(poster_url[3])
    with col4:
        st.text(recommended_books[4])
        st.image(poster_url[4])
    with col5:
        st.text(recommended_books[5])
        st.image(poster_url[5])