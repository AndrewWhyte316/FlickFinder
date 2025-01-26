import sqlite3



DATABASE = 'FlickFinder.db'

def initialize_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Create genres table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # Create movies table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre_id INTEGER NOT NULL,
            FOREIGN KEY (genre_id) REFERENCES genres (id)
        )
    ''')

    # Prepopulate genres
    genres = ['Action', 'Comedy', 'Sci-Fi', 'Superhero', 'Romance', 'Horror', 'Drama']
    for genre in genres:
        cursor.execute('INSERT OR IGNORE INTO genres (name) VALUES (?)', (genre,))

    connection.commit()
    connection.close()

if __name__ == '__main__':
    initialize_database()
    print("Database initialized successfully!")