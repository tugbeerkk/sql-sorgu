import sqlite3
from config import DATABASE
import random

class DB_Manager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS countries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    continent TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS special_days (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    description TEXT,
                    country_id INTEGER,
                    is_global BOOLEAN DEFAULT 0,
                    FOREIGN KEY (country_id) REFERENCES countries(id)
                )
            ''')
            conn.commit()
    

    def specialcountry(self, country_name):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT sd.name, sd.date
            FROM special_days sd
            JOIN countries c ON sd.country_id = c.id
            WHERE c.name = ?
        ''', (country_name,))
        
        return cursor.fetchall()
    
    def randomday(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM special_days')
        total = cursor.fetchone()[0]

        random_index = random.randint(0, total - 1)

        cursor.execute('''
            SELECT sd.name, sd.date, c.name
            FROM special_days sd
            LEFT JOIN countries c ON sd.country_id = c.id
            LIMIT 1 OFFSET ?
        ''', (random_index,))

        return cursor.fetchone()

if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()
