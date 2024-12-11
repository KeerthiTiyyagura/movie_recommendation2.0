import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('movie.db')
cursor = conn.cursor()

# Create the 'movies' table with id, title, genre, and rating
cursor.execute('''
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    rating REAL NOT NULL
)
''')

# Optional: Insert sample data
sample_data = [
    ('The Shawshank Redemption', 'Drama', 9.3),
    ('The Godfather', 'Crime', 9.2),
    ('The Dark Knight', 'Action', 9.0),
    ('Pulp Fiction', 'Crime', 8.9),
    ('Schindler\'s List', 'Drama', 8.9),
    ('Inception', 'Sci-Fi', 8.8),
    ('Fight Club', 'Drama', 8.8),
    ('Forrest Gump', 'Drama', 8.8),
    ('The Matrix', 'Sci-Fi', 8.7),
    ('The Lord of the Rings: The Return of the King', 'Fantasy', 8.9),
    ('The Empire Strikes Back', 'Sci-Fi', 8.7),
    ('Interstellar', 'Sci-Fi', 8.6),
    ('The Green Mile', 'Drama', 8.6),
    ('The Lion King', 'Animation', 8.5),
    ('Avengers: Endgame', 'Action', 8.4)
]

cursor.executemany('INSERT INTO movies (title, genre, rating) VALUES (?, ?, ?)', sample_data)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database created and populated with sample data!")
