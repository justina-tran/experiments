import pandas as pd
from seaborn.palettes import color_palette
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from scipy.spatial.distance import pdist, squareform
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import KNeighborsRegressor,NearestNeighbors
from scipy.sparse import csr_matrix

plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (10,6)

books = pd.read_csv('data/Books.csv')
users = pd.read_csv('data/Users.csv')
ratings = pd.read_csv('data/Ratings.csv')

user_id_loc = users[['User-ID', 'Location']]
book_details = ratings.merge(books, on='ISBN').iloc[:,:7]
user_book_count = book_details.groupby('User-ID')['Book-Title'].count().sort_values(ascending=False).reset_index()

# get users who has read/reviewed more than 20 books
user_count = book_details['User-ID'].value_counts() # how many books each user read/reviewed
user_list = user_count[user_count > 20].index
x_users_df = book_details[book_details['User-ID'].isin(user_list)]

# list of books that have more than 50 ratings
book_counts = x_users_df['Book-Title'].value_counts()
book_list = book_counts[book_counts>50].index
books_users_df = x_users_df[x_users_df['Book-Title'].isin(book_list)]

#remove duplicate before pivoting
books_users_df = books_users_df.drop_duplicates(['User-ID', 'Book-Title']) 

# create pivot table of all books, users, and the ratings
book_pivot_df = books_users_df.pivot_table(columns='User-ID', index='Book-Title', values="Book-Rating").fillna(0)

# normalize the values to deal with nulls
avg_ratings = book_pivot_df.mean(axis=1)
book_pivot_norm_df = book_pivot_df.sub(avg_ratings, axis=0)

# 1. cosine similarity 
# given a user book preferences, use cosine similarity to recommend books
# display the top 10 books and the score

# 2. KNN 
# use KNN to recommend similar books


def main():
    st.title('Hello')

    #select books
    with st.form(key='Selecting columns'):
        books_multi = st.multiselect(
            'Select your favorite book(s): ', (book_list)
            )
        st.text("Click Run:")
        submit_button = st.form_submit_button(label='Run') #will run selected results when users finish selecting and click run
if __name__ == "__main__":
  main()

