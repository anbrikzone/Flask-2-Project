import sqlite3
from models.basemodel import BaseModel

class Tasks(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.table = "tasks"

    def create(self, **kwargs):
        try:
            self.cursor.execute(f"INSERT INTO {self.table} ({', '.join(kwargs.keys())}) VALUES({', '.join(['?'] * len(kwargs.values()))})", list(kwargs.values()))
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return 0
        
    def update(self, id, user_id, **kwargs):
        try:
            self.cursor.execute(f"UPDATE {self.table} SET title = ?, status = ? WHERE id = ? AND user_id = ?", (list(kwargs.values()), id, user_id))
            self.connection.commit()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return 0
    
    def done(self, id, user_id):
        try:
            self.cursor.execute(f"UPDATE {self.table} SET status = 1 WHERE id = ? AND user_id = ?", (id, user_id))
            self.connection.commit()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return 0

    def remove(self, id):
        try:
            self.cursor.execute(f"DELETE FROM {self.table} WHERE id = {id}")
            self.connection.commit()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return 0
    
    def get_all(self, user_id):
        try:
            result = self.cursor.execute(f"SELECT * FROM {self.table} WHERE user_id = ? ORDER BY status ASC, id DESC", (user_id,)).fetchall()
            self.connection.commit()
            return result
        except sqlite3.Error as er:
            print('SQLite error in get_all() method: %s' % (' '.join(er.args)))
            return 0
        
    def get_by_id(self, id):
        try:
            result = self.cursor.execute(f"SELECT * FROM {self.table} WHERE id = {id}").fetchone()
            self.connection.commit()
            return result
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return 0
