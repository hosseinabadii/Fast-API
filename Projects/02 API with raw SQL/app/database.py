from sqlite3 import Connection, Cursor


def create_posts_table(conn: Connection, cursor: Cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='posts'")
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute("""
            CREATE TABLE posts (
                id INTEGER PRIMARY KEY,
                title TEXT,
                content TEXT
            )
        """)
        print("Table 'posts' created.")
    conn.commit()
