import sqlite3


def init_db(DATABASE):
    """Initialize the database with necessary tables."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS links
                    (short_link TEXT PRIMARY KEY, 
                    original_url TEXT, 
                    image_url TEXT, 
                    og_title TEXT, 
                    og_description TEXT, 
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()