from flask import Flask, render_template, request, redirect
import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('movie.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to load movies and calculate similarity
def calculate_similarity():
    conn = get_db_connection()
    movies = pd.read_sql("SELECT * FROM movies", conn)
    conn.close()
    if movies.empty:
        return None, None

    # Combine title and genre into a single feature
    movies['features'] = movies['title'] + " " + movies['genre']

    # Vectorize the features
    vectorizer = TfidfVectorizer(stop_words='english')
    feature_matrix = vectorizer.fit_transform(movies['features'])

    # Calculate similarity
    similarity_matrix = cosine_similarity(feature_matrix, feature_matrix)
    return movies, similarity_matrix

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Add movie
@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        rating = request.form['rating']
        conn = get_db_connection()
        conn.execute('INSERT INTO movies (title, genre, rating) VALUES (?, ?, ?)', (title, genre, rating))
        conn.commit()
        conn.close()
        return redirect('/movies')
    return render_template('add_movie.html')

# List all movies
@app.route('/movies')
def list_movies():
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM movies').fetchall()
    conn.close()
    return render_template('movies.html', movies=movies)

# Recommendations based on a selected movie
@app.route('/recommend/<movie_title>')
def recommend(movie_title):
    movies, similarity_matrix = calculate_similarity()
    if movies is None or similarity_matrix is None:
        return "No movies available for recommendations."

    try:
        movie_idx = movies[movies['title'] == movie_title].index[0]
    except IndexError:
        return "Movie not found."

    # Get similarity scores and sort them
    similarity_scores = list(enumerate(similarity_matrix[movie_idx]))
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Get the top 5 recommendations
    recommendations = [movies.iloc[i[0]]['title'] for i in sorted_scores[1:6]]
    return render_template('recommendations.html', movie_title=movie_title, recommendations=recommendations)

# Upload movies via CSV
@app.route('/upload', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            filepath = 'uploaded_movies.csv'
            file.save(filepath)
            conn = get_db_connection()
            movies = pd.read_csv(filepath)
            movies.to_sql('movies', conn, if_exists='append', index=False)
            conn.close()
            return redirect('/movies')
        else:
            return "Invalid file format. Please upload a CSV file."
    return render_template('upload_csv.html')

# Delete movie
@app.route('/delete/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
    conn.commit()
    conn.close()
    return redirect('/movies')

if __name__ == '__main__':
    app.run(debug=True)
